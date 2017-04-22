/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', 'FlashService'];
    function UpdateController(UserService, FlashService) {
        var vm = this;

        vm.updateinfo = updateinfo;

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
