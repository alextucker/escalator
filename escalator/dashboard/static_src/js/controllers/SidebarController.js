var SidebarController = function($scope, $rootScope) {
    $scope.sidebarData = {
        currentState: ''
    };

    $rootScope.$watch('appstate', function(newValue, oldValue, scope){
        if(newValue) {
            console.log(newValue);
            $scope.sidebarData.currentState = newValue;
        }
    });
};

angular.module('escalator.controllers.sidebar', [])
.controller('SidebarController', ['$scope', '$rootScope', SidebarController]);
