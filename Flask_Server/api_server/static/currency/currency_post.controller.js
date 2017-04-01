/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyPostController', CurrencyPostController);

    CurrencyPostController.$inject = ['SearchService', '$rootScope','$location'];
    function CurrencyPostController(SearchService, $rootScope, $location) {
        var vm = this;
        vm.post = post;

        function post() {
            SearchService.PostCurrency(vm.what)
                .then(function (response) {
                    if (response.data!=null) {
                        //use response to update page
                         alert("success!");
                        $location.path('/currency_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();