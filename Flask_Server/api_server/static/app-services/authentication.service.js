(function () {
    'use strict';

    angular
        .module('app')
        .factory('AuthenticationService', AuthenticationService);

    AuthenticationService.$inject = ['$http', '$rootScope'];
    function AuthenticationService($http, $rootScope) {
        var service = {};
        service.isLogged = false;
        service.Login = Login;

        return service;

        function Login(username, password, callback) {

            /* Use this for real authentication
             ----------------------------------------------*/
            $http.post('/api/authenticate', {username: username, password: password})
                .then(function successCallback(response) {
                        console.log(response.data);
                        callback(response.data);
                    },
                    function errorCallback(response) {
                        console.log(response.data);
                    });
        }

    };

})();