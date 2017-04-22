/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyResultController', CurrencyResultController);

    CurrencyResultController.$inject = ['$location','AuthenticationService'];
    function CurrencyResultController($location,AuthenticationService) {
        var vm = this;
        vm.logout = logout;
        vm.isAdmin=AuthenticationService.isAdmin;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

    }

})();