var DashboardAppController = function($scope, OrganizationService, UserSerivce) {
    $scope.name = 'Alex';
    $scope.appData = {
        loggedInUser: false,
        organization: false
    };

    UserSerivce.me()
    .then(function(data){
        $scope.appData.loggedInUser = data;

        OrganizationService.get(data.organization_id)
        .then(function(data){
            $scope.appData.organization = data;
        });
    });
};

angular.module('escalator.controllers.dashboardapp', [])
.controller('DashboardAppController', ['$scope', 'OrganizationService', 'UserSerivce', DashboardAppController]);
