angular.module("apps", ["ngRoute", "ngResource"])
.filter('truncate', function () {
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
.factory("Applications", ["$resource", function($resource) {
    return $resource("/v1/application/:id");
}])
.config(function($routeProvider) {
    $routeProvider
        .when("/", {
            controller: "FrontCtrl",
            templateUrl: "front.html"
        })
        .when("/list", {
            controller: "ListCtrl",
            templateUrl: "list.html"
        });
})
.controller("FrontCtrl", function($scope) {
    // just show the template
})
.controller("ListCtrl", ["$scope", "Applications", function($scope, Applications) {
    $scope.applications = Applications.query();
}]);
