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

    AdmanageController.$inject = ['FlashService', 'AdminService', '$location', 'AuthenticationService', 'ItemService'];
    function AdmanageController(FlashService, AdminService, $location, AuthenticationService, ItemService) {
        var vm = this;
        vm.present = true;
        vm.isAdmin = AuthenticationService.isAdmin;

        vm.get = get;
        vm.Deleteuser = Deleteuser;
        vm.createuser = createuser;
        vm.logout = logout;
        vm.sortid = sortid;
        vm.sortname = sortname;
        vm.history = history;
        vm.sidsort = sidsort;

        function sidsort(a, b) {
            if (a.sid < b.sid)
                return 1;
            else if (a.sid > b.sid)
                return -1;
            else
                return 0;
        }

        function history() {
            ItemService.History()
                .then(function (response) {
                    if (typeof(response.retrieve_search_status) == "undefined") {
                        //use response to update page
                        //console.log("adadfads");
                        response.sort(sidsort);
                        $rootScope.history = response;
                        $location.path('/history');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function Deleteuser() {
            if (typeof(vm.deletename) == "undefined" || vm.deletename == "")
                FlashService.Error('Please type the username', true);
            else {
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

        function sortid() {
            vm.users.sort(function (a, b) {
                return a.id > b.id ? 1 : -1;
            });
        }

        function sortname() {
            vm.users.sort(function (p1, p2) {
                return p1.name.localeCompare(p2.name)
            });
        }
    }

})();