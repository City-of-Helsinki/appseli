angular.module("apps", ["ngRoute", "ngResource", "config"])
.filter("truncate", function () {
    return function (text, length, end) {
        if (isNaN(length))
            length = 10;

        if (end === undefined)
            end = "...";

        if (text.length <= length || text.length - end.length <= length) {
            return text;
        } else {
            return String(text).substring(0, length-end.length) + end;
        }
    };
})
.factory("languageService", ["$locale", function($locale) {
    var language = $locale.id.split("-")[0];
    return {
        getLanguage: function () {
            return language;
        },
        setLanguage: function (language) {
            language = language_;
        }
    };
}])
.filter("translate", ["languageService", function (languageService) {
    return function (field) {
        var lang = languageService.getLanguage();
        return field[lang] || field["en"];
    }
}])
.factory("Applications", ["$resource", "API_ROOT", function($resource, API_ROOT) {
    return $resource(API_ROOT + "application/:id/");
}])
.factory("Categories", ["$resource", "API_ROOT", function($resource, API_ROOT) {
    var Categories = $resource(API_ROOT + "category/:id/");
    var glyphicons = {
        "travel-local": "glyphicon-camera",
        "food-drink": "glyphicon-glass",
        "culture": "glyphicon-picture",
        "transportation": "glyphicon-plane",
        "nature": "glyphicon-tree-conifer",
        "tools": "glyphicon-wrench",
        "social": "glyphicon-comment",
        "communications": "glyphicon-cloud",
        "lifestyle": "glyphicon-star",
    };

    Categories.prototype.getGlyphiconClass = function() {
        return glyphicons[this.slug] || "glyphicon-th-large";
    };
    return Categories;

}])
.config(function($locationProvider) {
    // Remove '#' from urls and use html5 pushstate instead
    $locationProvider.html5Mode(true);
})
.config(["$routeProvider", "STATIC_URL", function($routeProvider, STATIC_URL) {
    $routeProvider
        .when("/", {
            templateUrl: STATIC_URL + "front.html"
        })
        .when("/list/", {
            controller: "ApplicationListCtrl",
            templateUrl: STATIC_URL + "list.html"
        })
        .when("/application/:applicationId/", {
            controller: "ApplicationCtrl",
            templateUrl: STATIC_URL + "application.html"
        })
        .when("/categories/", {
            controller: "CategoryListCtrl",
            templateUrl: STATIC_URL + "categories.html"
        })
        .when("/info/", {
            controller: "InfoCtrl",
            templateUrl: STATIC_URL + "info.html"
        })
        .otherwise({
            redirectTo: "/"
        });
}])
.controller("ApplicationListCtrl", ["$scope", "Applications", function($scope, Applications) {
    $scope.applications = Applications.query();
}])
.controller("ApplicationCtrl", ["$scope", "$routeParams", "Applications", function($scope, $routeParams, Applications) {
    var application = Applications.get({id:$routeParams.applicationId});
    application.$promise.then(function() {
        $scope.application = application;
    });
}])
.controller("CategoryListCtrl", ["$scope", "Categories", function($scope, Categories) {
    $scope.categories = Categories.query();
}])
.controller("InfoCtrl", function() {
});

// TODO: this doesn't seem to work -- fix it
/*
$(document).ready(function() {
    var imageHeight, wrapperHeight, overlap, container = $('.image--responsive');

    function centerImage() {
        imageHeight = container.find('img').height();
        wrapperHeight = container.height();
        overlap = (wrapperHeight - imageHeight) / 2;
        container.find('img').css('margin-top', overlap);
    }

    $(window).on("load resize", centerImage);

    var el = document.getElementById('wrapper');
    if (el && el.addEventListener) {
        el.addEventListener("webkitTransitionEnd", centerImage, false); // Webkit event
        el.addEventListener("transitionend", centerImage, false); // FF event
        el.addEventListener("oTransitionEnd", centerImage, false); // Opera event
    }
});
*/
