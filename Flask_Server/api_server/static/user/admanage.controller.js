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

    AdmanageController.$inject = ['FlashService', 'AdminService', '$window'];
    function AdmanageController(FlashService, AdminService, $window) {
        var vm = this;
        vm.present=true;

        vm.get = get;
        vm.Deleteuser = Deleteuser;
        vm.createuser = createuser;

        function Deleteuser() {
            AdminService.Deletename(vm.deletename)
                .then(function (response) {
                    if (response.delete_status=="Success") {
                        FlashService.Success('Delete successful', true);
                         $window.location.reload();
                        //use response to update page
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function createuser() {
            AdminService.Create(vm.user)
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
                        vm.present=false;
                        vm.users = response;
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();