/**
 * Created by you on 2017/3/26.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencySearchController', CurrencySearchController);

    CurrencySearchController.$inject = ['CurrencyService', '$rootScope', '$location', '$window', 'AuthenticationService'];
    function CurrencySearchController(CurrencyService, $rootScope, $location, $window, AuthenticationService) {
        var vm = this;
        vm.isAdmin = AuthenticationService.isAdmin;
        vm.list1 = ["Legacy", "Hardcore Legacy", "Standard", "Hardcore"];
        vm.list4 = ["Select", "Blessed Orb", "Cartographer's Chisel", "Chaos Orb", "Chromatic Orb", "Divine Orb", "Exalted Orb", "Gemcutter's Prism", "Jeweller's Orb",
            "Orb of Alchemy", "Orb of Alteration", "Orb of Chance", "Orb of Fusing", "Orb of Regret", "Orb of Scouring", "Regal Orb", "Vaal Orb", "Perandus Coin", "Silver Coin"];
        vm.my_post = my_post;
        vm.search = search;
        vm.logout = logout;
        vm.tidsort = tidsort;
        vm.pricesort = pricesort;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function search() {
            console.log(vm.cs);
            CurrencyService.SearchCurrency(vm.cs)
                .then(function (response) {
                    if (response != null) {
                        //use response to update page
                        response.sort(pricesort);
                        $rootScope.posts = response;
                        $location.path('/currency_result');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function my_post() {
            CurrencyService.MyPost()
                .then(function (response) {
                    if (typeof(response.retrieve_post_status) == "undefined") {
                        //use response to update page
                        response.sort(tidsort);
                        $rootScope.myposts = response;
                        $location.path('/my_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function tidsort(a, b) {
            if (a.tid < b.tid)
                return 1;
            else if (a.tid > b.tid)
                return -1;
            else
                return 0;
        }

        function pricesort(a, b) {
            if (a.c1_number / a.c2_number < b.c1_number / b.c2_number)
                return 1;
            else if (a.c1_number / a.c2_number > b.c1_number / b.c2_number)
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
    }

})();