(function () {
    'use strict';

    angular
        .module('app')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', 'AuthenticationService', 'FlashService'];
    function LoginController($location, AuthenticationService, FlashService) {
        var vm = this;

        vm.login = login;

        // (function initController() {
        //     // reset user status
        //     AuthenticationService.ClearCredentials();
        // })();

        function login() {
            vm.dataLoading = true;
            AuthenticationService.Login(vm.username, vm.password, function (response) {
                if (response.login_status) {
                    AuthenticationService.isLogged = true;
                    localStorage.token = response.token;
                    //AuthenticationService.SetCredentials(vm.username, vm.password);
                    $location.path('/item_search');
                } else {
                    FlashService.Error(response.message);
                    vm.dataLoading = false;
                }
            });
        };
    }

})();
