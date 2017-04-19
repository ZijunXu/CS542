/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['$rootScope', '$location', 'CurrencyService', '$window', 'FlashService'];
    function CurrencyPostController($rootScope, $location, CurrencyService , $window, FlashService) {
        var vm = this;

        vm.my_post = my_post;
        vm.post = post;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function post() {
            CurrencyService.PostCurrency(vm.cup)
                .then(function (response) {
                    //use response to update page
                    if (response.post_status) {
                        FlashService.Success('Post successful', true);
                        $window.location.reload();
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
    }

})();