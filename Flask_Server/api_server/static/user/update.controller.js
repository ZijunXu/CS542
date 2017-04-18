/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', 'FlashService', '$window'];
    function UpdateController(UserService, FlashService, $window) {
        var vm = this;

        vm.update_info = {password: vm.password, email: vm.email, confirm_password: vm.confirm};
        vm.updateinfo = updateinfo;

        function updateinfo() {
            vm.dataLoading = true;
            UserService.Update(vm.update)
                .then(function (response) {
                    if (response.update_status) {
                        FlashService.Success('Update successful', true);
                        $window.location.reload();
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();
