(function () {
    'use strict';

    angular
        .module('app')
        .factory('UserService', UserService);

    UserService.$inject = ['$http'];
    function UserService($http) {
        var service = {};

        service.Create = Create;
        service.Update = Update;

        return service;

        function Create(user) {
            return $http.post('/api/reg', user).then(handleSuccess, handleError('Error creating user'));
        }

        function Update(update) {
            return $http.put('/api/user/update', update).then(handleSuccess, handleError('Error updating user'));
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
