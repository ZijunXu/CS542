/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyResultController', CurrencyResultController);

    CurrencyResultController.$inject = ['$location', '$rootScope','CurrencyResultService'];
    function CurrencyResultController($rootScope, CurrencyResultService) {
        var vm = this;

        vm.currency=CurrencyResultService.GetCurrency();

        // vm.result = result;
        //
        // function result(item) {
        //
        //     SearchService.PostItem(vm.name)
        //         .then(function (response) {
        //             if (response.data!=null) {
        //                 //use response to update page
        //                  console.log(response.data);
        //                 $location.path('/login');
        //             } else {
        //                 FlashService.Error(response.message);
        //                 vm.dataLoading = false;
        //             }
        //         });
        //
        // }
    }

})();