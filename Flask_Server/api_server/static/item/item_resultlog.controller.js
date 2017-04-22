/**
 * Created by youzhou on 4/22/17.
 */
(function () {
    //'use strict';

    angular
        .module('app')
        .controller('ItemResultLogController', ItemResultLogController);

    ItemResultLogController.$inject = ['$location', 'AuthenticationService'];
    function ItemResultLogController($location, AuthenticationService) {
        var vm = this;
        vm.logout = logout;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }
    }

})();