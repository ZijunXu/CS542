/**
 * Created by you on 2017/4/14.
 */
/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('AdmanageController', AdmanageController);

    AdmanageController.$inject = ['$rootScope', 'AdminService', '$window'];
    function AdmanageController(AdminService, $rootScope, $window) {
        var vm = this;
        vm.did = {id: vm.deleteid};
        vm.dpo = {id: vm.deletepost};

        vm.get = get;
        vm.Deleteid = Deleteid;
        vm.Deletepost = Deletepost;

        function Deleteid() {
            CurrencyService.Deleteid(vm.did)
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

        function Deletepost() {
            CurrencyService.Deletepost(vm.dpo)
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

        function get() {
            AdminService.GetAll()
                .then(function (response) {
                    if (response != null) {
                        vm.users = response;
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();