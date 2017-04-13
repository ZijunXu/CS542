(function () {
    'use strict';

    angular
        .module('app')
        .factory('UserService', UserService);

    UserService.$inject = ['$http', '$httpParamSerializerJQLike'];
    function UserService($http, $httpParamSerializerJQLike) {
        var service = {};

        service.Create = Create;
        service.Update = Update;

        return service;

        function Create(user) {
            return $http.post('/api/reg', user).then(handleSuccess, handleError('Error creating user'));
        }

        // function Update(user) {
        //     return $http.put('/api/users/' + user.id, user).then(handleSuccess, handleError('Error updating user'));
        // }

        function Update(update) {
            //alert(item);
            return $http({
                url: '/api/update',
                method: 'PUT',
                data: $httpParamSerializerJQLike(update),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error updating user info'));
        }

        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return {success: false, message: error};
            };
        }
    }

})();
