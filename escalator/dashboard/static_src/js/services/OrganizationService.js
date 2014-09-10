var OrganizationService = function($http, $q) {

    return {
        get: function(id) {
            var defer = $q.defer();

            $http.get('/api/v1/organizations/' + id)
            .success(function(data){
                defer.resolve(data);
            })
            .error(function(){
                defer.reject(data);
            });

            return defer.promise;
        },

        invite: function(organizationId, email) {
            var defer = $q.defer();
            var data = {email:email};

            $http.post('/api/v1/organizations/' + organizationId + '/invites', data)
            .success(function(data){
                defer.resolve(data);
            })
            .error(function(){
                defer.reject(data);
            });

            return defer.promise;
        },

        call: function(organizationId, users) {
            var defer = $q.defer();
            var data = {};
            data['user_set'] = _.map(users, function(user){
                return user.id;
            });

            $http.post('/api/v1/organizations/' + organizationId + '/conferences', data)
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

angular.module('escalator.services.organization', [])
.factory('OrganizationService', ['$http', '$q', OrganizationService])
