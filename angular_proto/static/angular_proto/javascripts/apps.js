angular.module("apps", ["ngRoute", "ngResource"])
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
