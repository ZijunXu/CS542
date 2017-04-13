/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['$rootScope', '$location', 'MyPostService', 'CurrencyService', '$window', 'FlashService'];
    function CurrencyPostController(CurrencyService, $rootScope, $location, MyPostService, $window, FlashService) {
        var vm = this;
        vm.cpost = {gameid: vm.gameid, have: vm.have, price1: vm.price1, want: vm.want, price2: vm.price2}
        vm.my_post = my_post;
        vm.post = post;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function post() {
            CurrencyService.PostCurrency(vm.cpost)
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