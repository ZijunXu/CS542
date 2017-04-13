/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', '$location', 'FlashService'];
    function UpdateController(UserService, $location, FlashService) {
        var vm = this;
        vm.update_info={};
        vm.updateinfo = updateinfo;

        function updateinfo() {
            vm.dataLoading = true;
            UserService.Update(vm.update_info)
                .then(function (response) {
                    if (response.register_status) {
                        FlashService.Success('Update successful', true);
                        $location.path('/item_search');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();
