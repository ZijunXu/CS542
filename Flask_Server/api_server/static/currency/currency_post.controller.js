/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['$rootScope', '$location', 'CurrencyService', '$window', 'FlashService', 'AuthenticationService'];
    function CurrencyPostController($rootScope, $location, CurrencyService, $window, FlashService, AuthenticationService) {
        var vm = this;
        vm.isAdmin=AuthenticationService.isAdmin;
        vm.list1 = ["Legacy", "Hardcore Legacy", "Standard", "Hardcore"];
        vm.my_post = my_post;
        vm.post = post;
        vm.logout = logout;
        vm.tidsort = tidsort;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function post() {
            CurrencyService.PostCurrency(vm.cup)
                .then(function (response) {
                    //use response to update page
                    if (response.post_status) {
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

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }
    }

})();