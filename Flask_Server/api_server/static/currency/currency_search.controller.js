/**
 * Created by you on 2017/3/26.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencySearchController', CurrencySearchController);

    CurrencySearchController.$inject = ['CurrencyService', '$rootScope', '$location', '$window'];
    function CurrencySearchController(CurrencyService, $rootScope, $location, $window) {
        var vm = this;

        vm.my_post = my_post;
        vm.search = search;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function search() {
            console.log(vm.cs);
            CurrencyService.SearchCurrency(vm.cs)
                .then(function (response) {
                    if (response != null) {
                        //use response to update page
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
                    if (response != null) {
                        //use response to update page
                        $rootScope.myposts = response;
                        $location.path('/my_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();