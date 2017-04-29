/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['$rootScope', '$location', 'CurrencyService', 'FlashService', 'AuthenticationService', 'ItemService'];
    function CurrencyPostController($rootScope, $location, CurrencyService, FlashService, AuthenticationService, ItemService) {
        var vm = this;

        vm.isAdmin = AuthenticationService.isAdmin;

        vm.list1 = ["Legacy", "Hardcore Legacy", "Standard", "Hardcore"];
        vm.list4 = ["Select", "Blessed Orb", "Cartographer's Chisel", "Chaos Orb", "Chromatic Orb", "Divine Orb", "Exalted Orb", "Gemcutter's Prism", "Jeweller's Orb",
            "Orb of Alchemy", "Orb of Alteration", "Orb of Chance", "Orb of Fusing", "Orb of Regret", "Orb of Scouring", "Regal Orb", "Vaal Orb", "Perandus Coin", "Silver Coin"];

        vm.my_post = my_post;
        vm.post = post;
        vm.logout = logout;
        vm.history = history;
        vm.sidsort = sidsort;

        vm.reloadRoute = function () {
            vm.cup = {};
            vm.cup.league = 'Legacy';
            vm.cup.c1_item = 'Select';
            vm.cup.c2_item = 'Select';
        };

        function post() {
            CurrencyService.PostCurrency(vm.cup)
                .then(function (response) {
                    //use response to update page
                    if (response.post_status) {
                        vm.reloadRoute();
                        FlashService.Success('Post successful', true);
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
                        $rootScope.myposts = response;
                        $location.path('/my_post');
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