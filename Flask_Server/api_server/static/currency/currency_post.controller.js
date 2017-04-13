/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['$rootScope', '$location', 'MyPostService', 'CurrencyService','$window'];
    function CurrencyPostController(CurrencyService, $rootScope, $location, MyPostService,$window) {
        var vm = this;

        vm.my_post = my_post;
        vm.post = post;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function post() {
            CurrencyService.PostCurrency(vm.what)
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        alert("success!");
                        $location.path('/currency_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function my_post() {
            CurrencyService.MyPost()
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        alert("success!");
                        MyPostService.SetPost(response.data);
                        $location.path('/my_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();