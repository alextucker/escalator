var TopbarController = function($scope) {
    $scope.topbarData = {
        user: false,
        loading: true
    };

    $scope.$watch('appData.loggedInUser', function(newValue, oldValue, scope){
        if(newValue != false) {
            $scope.topbarData.user = newValue;

            $scope.topbarData.loading = false;
        }
    });
};

angular.module('escalator.controllers.topbar', [])
.controller('TopbarController', ['$scope', TopbarController]);
