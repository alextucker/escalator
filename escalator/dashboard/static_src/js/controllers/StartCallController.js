var StartCallController = function($scope, $rootScope, $location, OrganizationService) {
    var self = this;
    $scope.startCallData = {
        userList: false,
        callList: []
    };

    $rootScope.appstate = 'initiate';

    this.addToCallList = function(user) {
        $scope.startCallData.callList.push(user);
        self.removeFromList($scope.startCallData.userList, user)
        if(mixpanel) {
            mixpanel.track("Initiate:AddToCallList");
        }
    };

    this.removeFromCallList = function(user) {
        $scope.startCallData.userList.push(user);
        self.removeFromList($scope.startCallData.callList, user)
    };

    this.removeFromList = function(list, item) {
        var index = list.indexOf(item);
        list.splice(index, 1);
    };

    this.startCall = function(users) {
        console.log('Starting call');
        OrganizationService.call($scope.startCallData.organization.id, users)
        .then(function(data){
            console.log('Call Started');
            console.log(data);
            $location.path('/incident/' + data.id);
        });
    };

    this.getInitials = function(user) {
        var initials = "";
        if (user.first_name) initials += user.first_name[0];
        if (user.last_name) initials += user.last_name[0];
        return initials;
    }

    $scope.$watch('appData.organization', function(newValue, oldValue, scope){
        if(newValue != false) {
            $scope.startCallData.userList = newValue.user_set;
            $scope.startCallData.organization = newValue;
            for(var i=0; i < $scope.startCallData.userList.length; i++) {
                var initials = self.getInitials($scope.startCallData.userList[i]);
                $scope.startCallData.userList[i].initials = initials;
            }
        }
    });
};

angular.module('escalator.controllers.startcall', [])
.controller('StartCallController', ['$scope', '$rootScope', '$location', 'OrganizationService', StartCallController]);
