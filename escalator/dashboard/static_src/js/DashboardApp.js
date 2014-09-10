angular.module('DashboardApp',[
    'Templates',
    'ngRoute',
    'ngCookies',
    'escalator.controllers.dashboardapp',
    'escalator.controllers.topbar',
    'escalator.controllers.sidebar',
    'escalator.controllers.startcall',
    'escalator.controllers.manageusers',
    'escalator.services.organization',
    'escalator.services.conference',
    'escalator.services.user'
])
.config(['$routeProvider', function($routeProvider){
    $routeProvider
    .when('/call', {
        controller: 'StartCallController',
        controllerAs: 'StartCall',
        templateUrl: 'startCall.html'
    })
    .when('/manage/users', {
        controller: 'ManageUsersController',
        controllerAs: 'ManageUsers',
        templateUrl: 'managerUsers.html'
    })
    .when('/incident/:incidentId', {
        controller: 'IncidentController',
        controllerAs: 'Incident',
        templateUrl: 'incident.html'
    })
    .otherwise({
        redirectTo:'/call'
    });
}])
.run(['$route', '$cookies', '$http', function($route, $cookies, $http){
    $http.defaults.headers.common["X-CSRFToken"] = $cookies.csrftoken;
    $route.reload();
}]);
