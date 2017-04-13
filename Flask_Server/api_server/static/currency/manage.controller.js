/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('ManagePostController', ManagePostController);

    ManagePostController.$inject = ['$rootScope', 'CurrencyService','$window'];
    function ManagePostController(CurrencyService, $rootScope, $window) {
        var vm = this;
        vm.down={id:vm.postid_d};
        vm.up = {id:vm.postid_u,have:vm.have, want:vm.want, price1:vm.price1,price2:vm.price2};
        vm.update = update;
        vm.Delete = Delete;

        function Delete() {
            CurrencyService.Delete(vm.down)
                .then(function (response) {
                        if (response.delete_status) {
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
            CurrencyService.Update(vm.up)
                .then(function (response) {
                    if (response.update_status) {
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