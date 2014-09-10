var ManageUsersController = function($scope, $rootScope, $location, OrganizationService) {
    var self = this;
    $scope.manageUserData = {
        organization: false
    };

    $rootScope.appstate = 'manageUsers';

    this.inviteUser = function(email) {
        OrganizationService.invite($scope.manageUserData.organization.id, email)
        .then(function(data){
            $scope.manageUserData.inviteEmail = '';
        });
    };

    $scope.$watch('appData.organization', function(newValue, oldValue, scope){
        if(newValue != false) {
            $scope.manageUserData.organization = newValue;
        }
    });
};

angular.module('escalator.controllers.manageusers', [])
.controller('ManageUsersController', ['$scope', '$rootScope', '$location', 'OrganizationService', ManageUsersController]);
