"""
A script for importing database content and media from apps.hel.fi.
"""
import re
from collections import namedtuple
from datetime import datetime
import logging
from optparse import make_option
import tempfile
from bs4 import BeautifulSoup
from django.core.files import File
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from modeltranslation.utils import auto_populate
from django.utils.translation.trans_real import activate, deactivate
import requests
from apps.models import (
    Application,
    Platform,
    Category,
    ApplicationPlatformSupport,
    ApplicationScreenshot,
    ApplicationLanguageSupport,
)

class active_language:
    def __init__(self, language):
        self.language = language
    def __enter__(self):
        activate(self.language)
        return self.language
    def __exit__(self, type, value, traceback):
        deactivate()

SUPPORTED_LANGUAGES = map(lambda x: x[0], settings.LANGUAGES)

BASE_URL = "http://apps.hel.fi/hel.fi"
# The page displays different content for different user agents.
PLATFORMS = (
    ("android",       "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L "
                      "Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) "
                      "Version/4.0 Mobile Safari/534.30"),
    ("windows-phone", "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS "
                      "7.5; Trident/5.0; IEMobile/9.0)"),
    ("ios",           "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) "
                      "AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 "
                      "Mobile/9A334 Safari/7534.48.3"),
)


logger = logging.getLogger(__name__)


# This contains data from an application as parsed from the apps.hel.fi
# application detail pages.  The actual Application objects are generated from
# these.
RawApplicationRecord = namedtuple("RawApplicationRecord", [
    "name",
    "category_name",
    "platform_slug",
    "thumbnail_url",
    "description",
    "store_url",
    "screenshot_urls",
    "publisher_name",
    "publish_date",
    "support_url",
    "contact_email",
])


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--delete",
            action="store_true",
            default=False,
            help="Delete all data from DB before importing",
        ),
        make_option(
            "--cache",
            action="store_true",
            default=False,
            help="Use a download cache (not recommended - "
                "user agents might mess things up)",
        ),
    )

    def handle(self, *args, **options):
        logger.addHandler(logging.StreamHandler(self.stdout))
        logger.setLevel(logging.DEBUG)

        if options["delete"]:
            logger.info("Deleting data from DB")
            for model in [Application, Platform, Category, ApplicationPlatformSupport,
                          ApplicationLanguageSupport, ApplicationScreenshot]:
                model.objects.all().delete()

        if options["cache"]:
            logger.info("Installing download cache")
            import requests_cache
            requests_cache.install_cache("legacy_import")

        logger.info("Importing legacy data")
        with auto_populate("default"):
            import_legacy_data()

        logger.info("All done")

def multilingual_set(src, src_field, dest, dest_field, process=None):
    for lang in SUPPORTED_LANGUAGES:
        with active_language(lang):
            val = getattr(src[lang], src_field, None)
            if process:
                val = process(val)
            setattr(dest, dest_field, val)

def import_legacy_data():
    # Get / create platforms
    platforms_by_slug = {}
    for slug, _ in PLATFORMS:
        try:
            platform = Platform.objects.get(slug=slug)
        except Platform.DoesNotExist:
            platform = Platform.objects.create(name=slug, slug=slug)
        platforms_by_slug[slug] = platform

    for raw_application_data in fetch_raw_applications():
        # The English values are used as the default, for
        # example for the category slug.
        raw_application = raw_application_data['en']
        slug = slugify(raw_application.name)
        platform = platforms_by_slug[raw_application.platform_slug]

        # Get / create category
        category_slug = slugify(raw_application.category_name)
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            category = Category.objects.create(slug=category_slug)
            multilingual_set(raw_application_data, 'category_name',
                             category, 'name')
            category.save()
        # Get / create application
        try:
            application = Application.objects.get(slug=slug)
        except Application.DoesNotExist:
            # This data is only saved once
            application = Application.objects.create(
                slug=slug,
                vendor=raw_application.publisher_name,
                publish_date=raw_application.publish_date,
                rating=0.0,
                support_url=raw_application.support_url,
                contact_email=raw_application.contact_email,
            )
            image = fetch_file(raw_application.thumbnail_url)
            application.image.save("icon.{0}".format(image.file_ext), image)
            application.categories.add(category)

        multilingual_set(
            raw_application_data, 'name',
            application, 'name'
        )
        multilingual_set(
            raw_application_data, 'description',
            application, 'description'
        )
        multilingual_set(
            raw_application_data, 'description',
            application, 'short_description',
            process=lambda x: " ".join(x.split()[:25]) + "..."
        )
        application.save()

        # Get / create platform support
        supports_with_same_app = ApplicationPlatformSupport.objects.filter(
            platform=platform,
            application=application
        )[:1]
        supports_with_same_link = ApplicationPlatformSupport.objects.filter(
            platform=platform,
            store_url=raw_application.store_url,
        )[:1]

        if supports_with_same_app:
            pass
        elif supports_with_same_link:
            existing = supports_with_same_link[0]
            logger.error(
                "Error creating application support for {0} on "
                "{1}: Another application ({2}) already has the platform url "
                "{3} ".format(application, platform, existing,
                              raw_application.store_url)
            )
        else:
            ApplicationPlatformSupport.objects.create(
                platform=platform,
                application=application,
                store_url=raw_application.store_url,
                rating=0.0,
                nr_reviews=0,
                last_updated=timezone.now(),
            )

        # Get / create screenshots
        for index, url in enumerate(raw_application.screenshot_urls, start=1):
            # dumb heuristic -- doesn't actually check that the
            # screenshot is there
            if ApplicationScreenshot.objects.filter(platform=platform,
                                                    application=application,
                                                    index=index):
                continue
            screenshot = ApplicationScreenshot.objects.create(
                application=application,
                platform=platform,
                index=index,
            )
            image = fetch_file(url)
            filename = "{0}-screenshot-{1}.{2}".format(platform.slug,
                                                       index,
                                                       image.file_ext)
            screenshot.image.save(filename, image)

        # Get / create language support
        ApplicationLanguageSupport.objects.get_or_create(
            language="en",
            application=application
        )


def fetch_raw_applications():
    logger.info("Fetching application data")
    for platform, user_agent in PLATFORMS:
        response = fetch("list.jsf?category=ALL", ua=user_agent)
        for app_url in parse_application_urls(response.content):
            data = {}
            for lang in SUPPORTED_LANGUAGES:
                response = fetch(app_url, ua=user_agent,
                    headers= { 'Accept-Language': lang }
                )
                data[lang] = parse_application_data(
                    response.content,
                    platform_slug=platform)
            yield data


def parse_application_urls(html_content):
    logger.info("Parsing application links")
    soup = BeautifulSoup(html_content)
    list_ = soup.find(class_="listView")
    for li in list_.findAll("li"):
        yield li.find("a").attrs["href"]


def clean_text(text):
    # remove consecutive whitespaces
    text = re.sub(r'\s\s+', ' ', text, re.U)
    return text.strip()


def parse_application_data(html_content, platform_slug):
    logger.info("Parsing raw application data")
    soup = BeautifulSoup(html_content).find(id="single_page")

    _table_rows = soup.find("table").findAll("tr")
    _contact_elem = soup.find(**{"data-icon": "appstore-contact"})
    contact_email = ""
    if _contact_elem:
        contact_email = _contact_elem.attrs["href"]
        contact_email = contact_email.split(":", 1)[1]  # mailto:
        contact_email = contact_email.rsplit("?", 1)[0]  # ?subject=blahblah
    _support_elem = soup.find(**{"data-icon": "appstore-support"})
    support_url = _support_elem.attrs["href"] if _support_elem else ""

    # The download url is a local page that redirects to the actual app store /
    # etc page. Resolve it to the actual url (requires an HTTP request)
    _local_download_url = soup.find("a", rel="external").attrs["href"]
    _response = fetch(_local_download_url, func=requests.head)
    store_url = _response.headers["location"]

    _publish_date_str = clean_text(_table_rows[1].findAll("td")[1].text)
    publish_date = datetime.strptime(_publish_date_str, "%d.%m.%Y %H:%M")
    publish_date = publish_date.replace(tzinfo=timezone.utc)

    return RawApplicationRecord(
        name=clean_text(soup.find(id="apptitle").text),
        category_name=clean_text(soup.find(id="detail-b").find("p").text),
        platform_slug=platform_slug,
        thumbnail_url=soup.find(id="detail-a").find("img").attrs["src"],
        description=clean_text(soup.find(id="description").text),
        store_url=store_url,
        screenshot_urls=tuple(
            img.attrs["src"]
            for img in soup.findAll(class_="screenshotimage")
        ),
        publisher_name=clean_text(_table_rows[0].findAll("td")[1].text),
        publish_date=publish_date,
        contact_email=contact_email,
        support_url=support_url,
    )


def fetch_file(url):
    prefix = url.split("/")[-1]
    response = fetch(url)
    content_type = response.headers['content-type']
    assert content_type == 'image/jpeg'
    tmp = tempfile.NamedTemporaryFile(delete=True, prefix=prefix, suffix='.jpg')
    tmp.write(response.content)
    tmp.flush()
    f = File(tmp)
    f.file_ext = 'jpg'
    return f


def fetch(url, func=requests.get, ua=None, **kwargs):
    logger.info("Fetching {}".format(url))
    if ua:
        kwargs.setdefault("headers", {})
        kwargs["headers"]["User-Agent"] = ua
    if not "://" in url:
        url = "{}/{}".format(BASE_URL.rstrip("/"),
                             url.lstrip("/"))
    return func(url, **kwargs)
