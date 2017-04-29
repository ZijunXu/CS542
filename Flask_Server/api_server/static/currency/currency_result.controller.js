/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyResultController', CurrencyResultController);

    CurrencyResultController.$inject = ['$location', 'AuthenticationService', '$rootScope', 'ItemService'];
    function CurrencyResultController($location, AuthenticationService, $rootScope, ItemService) {
        var vm = this;

        vm.isAdmin = AuthenticationService.isAdmin;

        vm.logout = logout;
        vm.amountsort = amountsort;
        vm.history = history;
        vm.sidsort = sidsort;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function amountsort() {
            $rootScope.posts.sort(pricesort);
        }

        function pricesort(a, b) {
            if (a.c1_number / a.c2_number < b.c1_number / b.c2_number)
                return 1;
            else if (a.c1_number / a.c2_number > b.c1_number / b.c2_number)
                return -1;
            else
                return 0;
        }

        function history() {
            ItemService.History()
                .then(function (response) {
                    if (typeof(response.retrieve_search_status) == "undefined") {
                        //use response to update page
                        response.sort(sidsort);
                        $rootScope.history = response;
                        $location.path('/history');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function sidsort(a, b) {
            if (a.sid < b.sid)
                return 1;
            else if (a.sid > b.sid)
                return -1;
            else
                return 0;
        }

    }

})();