/**
 * Created by you on 2017/3/26.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencySearchController', CurrencySearchController);

    CurrencySearchController.$inject = ['SearchService', '$rootScope','$location','CurrencyResultService'];
    function CurrencySearchController(SearchService, $rootScope, $location, CurrencyResultService) {
        var vm = this;
        vm.search = search;

        function search() {
            SearchService.SearchCurrency(vm.what)
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
    }

})();