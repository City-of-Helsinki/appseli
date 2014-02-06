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
.filter('translatex', function () {
    return function (field) {
        // TODO
        return field.en;
    }
})
.factory("Applications", ["$resource", function($resource) {
    return $resource("/v1/application/:id");
}])
.factory("Categories", ["$resource", function($resource) {
    return $resource("/v1/category/:id");
}])
.config(function($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "front.html"
        })
        .when("/list", {
            controller: "ApplicationListCtrl",
            templateUrl: "list.html"
        })
        .when("/application/:applicationId", {
            controller: "ApplicationCtrl",
            templateUrl: "application.html"
        })
        .when("/categories", {
            controller: "CategoryListCtrl",
            templateUrl: "categories.html"
        })
        .when("/info", {
            templateUrl: "info.html"
        });
})
.controller("ApplicationListCtrl", ["$scope", "Applications", function($scope, Applications) {
    $scope.applications = Applications.query();
}])
.controller("ApplicationCtrl", ["$scope", "$routeParams", "Applications", function($scope, $routeParams, Applications) {
    $scope.application = Applications.get({id:$routeParams.applicationId});
}])
.controller("CategoryListCtrl", ["$scope", "Categories", function($scope, Categories) {
    $scope.categories = Categories.query();
}]);
