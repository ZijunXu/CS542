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
        service.Create = Create;
        service.Deletename = Deletename;

        return service;

        function GetAll() {
            return $http.get('/api/admin').then(handleSuccess, handleError('Error getting all users'));
        }

        function Create(user) {
            return $http.post('/api/admin', user).then(handleSuccess, handleError('Error creating user'));
        }

        function Deletename(name) {
            return $http.delete('/api/admin/' + name).then(handleSuccess, handleError('Error deleting user'));
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
