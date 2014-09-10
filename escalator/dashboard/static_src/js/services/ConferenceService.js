var ConferenceService = function($http, $q) {

    return {
        get: function(id) {
            var defer = $q.defer();

            $http.get('/api/v1/conferences/' + id)
            .success(function(data){
                defer.resolve(data);
            })
            .error(function(){
                defer.reject(data);
            });

            return defer.promise;
        }
    }
};

angular.module('escalator.services.conference', [])
.factory('ConferenceService', ['$http', '$q', ConferenceService])
