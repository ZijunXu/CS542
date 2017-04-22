/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', 'FlashService', '$location', 'AuthenticationService'];
    function UpdateController(UserService, FlashService, $location, AuthenticationService) {
        var vm = this;

        vm.updateinfo = updateinfo;
        vm.logout = logout;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function updateinfo() {
            vm.dataLoading = true;
            UserService.Update(vm.update)
                .then(function (response) {
                    if (response.update_status) {
                        FlashService.Success('Update successful', true);
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();
