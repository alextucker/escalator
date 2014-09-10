var UserSerivce = function($http, $q) {

    return {
        me: function() {
            var defer = $q.defer();

            $http.get('/api/v1/me/')
            .success(function(data){
                defer.resolve(data);
            })
            .error(function(){
                defer.reject();
            });

            return defer.promise;
        }
    }
};

angular.module('escalator.services.user', [])
.factory('UserSerivce', ['$http', '$q', UserSerivce])
