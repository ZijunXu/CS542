/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('UpdateController', UpdateController);

    UpdateController.$inject = ['UserService', 'FlashService', '$location', 'AuthenticationService', '$window', 'ItemService'];
    function UpdateController(UserService, FlashService, $location, AuthenticationService, $window, ItemService) {
        var vm = this;
        vm.isAdmin = AuthenticationService.isAdmin;

        vm.history = history;
        vm.updateinfo = updateinfo;
        vm.logout = logout;
        vm.sidsort = sidsort;

        function sidsort(a, b) {
            if (a.sid < b.sid)
                return 1;
            else if (a.sid > b.sid)
                return -1;
            else
                return 0;
        }

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function updateinfo() {
            vm.dataLoading = true;
            UserService.Update(vm.update)
                .then(function (response) {
                    if (response.update_status) {
                        $window.location.reload();
                        FlashService.Success('Update successful', true);
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
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
    }

})();
