/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('AdminService', AdminService);

    AdminService.$inject = ['$http'];
    function AdminService($http) {
        var service = {};

        service.GetAll = GetAll;
        service.GetByUsername = GetByUsername;
        service.Update = Update;
        service.Deleteid = Deleteid;

        return service;

        function GetAll() {
            return $http.get('/api/admin').then(handleSuccess, handleError('Error getting all users'));
        }

        function GetByUsername(username) {
            return $http.get('/api/admin' + username).then(handleSuccess, handleError('Error getting user by username'));
        }

        function Update(user) {
            return $http.put('/api/admin' + user.id, user).then(handleSuccess, handleError('Error updating user'));
        }

        function Deleteid(name) {
            return $http.delete('/api/admin' + name).then(handleSuccess, handleError('Error deleting user'));
        }

        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return { success: false, message: error };
            };
        }
    }

})();
