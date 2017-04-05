/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', '$location', '$rootScope', 'FlashService'];
    function UpdateController(UserService, $location, $rootScope, FlashService) {
        var vm = this;

        vm.updateinfo = updateinfo;

        function updateinfo() {
            vm.dataLoading = true;
            UserService.Update(vm.update_info)
                .then(function (response) {
                    if (response.register_status) {
                        FlashService.Success('Registration successful', true);
                        $location.path('/login');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();
