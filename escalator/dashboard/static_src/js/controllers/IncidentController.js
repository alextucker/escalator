var IncidentController = function($scope, $rootScope, $location, $interval, $routeParams, OrganizationService, ConferenceService) {
    var self = this;
    $scope.incidentData = {
        organization: false,
        conference: false
    };

    $rootScope.appstate = 'incident';

    this.getConferenceDetails = function(id) {
        ConferenceService.get(id)
        .then(function(data){
            $scope.incidentData.conference = data;
            if( ! data.has_active_calls) {
                $interval.cancel(intervalPromise);
            }
        });
    };

    $scope.$watch('appData.organization', function(newValue, oldValue, scope){
        if(newValue != false) {
            $scope.incidentData.organization = newValue;
        }
    });

    $scope.$on('$destroy', function(){
        if (intervalPromise) {
            $interval.cancel(intervalPromise);
        }
    });

    var intervalPromise = $interval(function(){
        self.getConferenceDetails($routeParams.incidentId);
        console.log('starting');
    }, 900);
};

angular.module('escalator.controllers.incident', [])
.controller('IncidentController', ['$scope', '$rootScope', '$location', '$interval', '$routeParams', 'OrganizationService', 'ConferenceService', IncidentController]);
