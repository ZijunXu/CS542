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

    AdmanageController.$inject = ['FlashService', 'AdminService', '$location', 'AuthenticationService'];
    function AdmanageController(FlashService, AdminService, $location, AuthenticationService) {
        var vm = this;
        vm.present = true;

        vm.get = get;
        vm.Deleteuser = Deleteuser;
        vm.createuser = createuser;
        vm.logout = logout;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function Deleteuser() {
            AdminService.Deletename(vm.deletename)
                .then(function (response) {
                    if (response.delete_status == "Success") {
                        FlashService.Success('Delete successful', true);
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
                        vm.present = false;
                        response.sort(function (p1, p2) {
                            return p1.name.localeCompare(p2.name)
                        });
                        vm.users = response;
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();