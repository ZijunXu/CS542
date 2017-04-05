/**
 * Created by you on 2017/3/26.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencySearchController', CurrencySearchController);

    CurrencySearchController.$inject = ['CurrencyService', '$rootScope','$location','CurrencyResultService','MyPostService'];
    function CurrencySearchController(CurrencyService, $rootScope, $location, CurrencyResultService, MyPostService) {
        var vm = this;
        vm.my_post=my_post;
        vm.search = search;

        function search() {
            CurrencyService.SearchCurrency(vm.what)
                .then(function (response) {
                    if (response.data!=null) {
                        //use response to update page
                         console.log(response.data);
                         CurrencyResultService.SetCurrency(response.data);
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
                    if (response.data!=null) {
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