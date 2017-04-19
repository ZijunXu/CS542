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
    function AdmanageController($rootScope, AdminService, $window) {
        var vm = this;

        vm.get = get;
        vm.Deleteuser = Deleteuser;
        vm.createuser = createuser;

        function Deleteuser() {
            CurrencyService.Deleteid(vm.deletename)
                .then(function (response) {
                    if (response.delete_status=="Success") {
                        FlashService.Success('Delete successful', true);
                        //use response to update page
                        $window.location.reload();
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function createuser() {
            CurrencyService.Update(vm.user)
                .then(function (response) {
                    if (response.register_status) {
                        FlashService.Success('Create successful', true);
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