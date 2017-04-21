/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('ManagePostController', ManagePostController);

    ManagePostController.$inject = ['CurrencyService','$window', 'FlashService'];
    function ManagePostController(CurrencyService, $window, FlashService) {
        var vm = this;

        vm.update = update;
        vm.Delete = Delete;

        function Delete() {
            CurrencyService.Delete(vm.deleteid)
                .then(function (response) {
                        if (response.delete_post_status=="Success") {
                        FlashService.Success('Delete successful', true);
                        //use response to update page
                       $window.location.reload();
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function update() {
            CurrencyService.Update(vm.updater,vm.tid)
                .then(function (response) {
                    if (response.post_update_status) {
                        FlashService.Success('Update successful', true);
                        //use response to update page
                       $window.location.reload();
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();