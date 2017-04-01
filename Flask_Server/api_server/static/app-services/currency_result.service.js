/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('CurrencyResultService', CurrencyResultService);

    CurrencyResultService.$inject = ['$rootScope'];
    function CurrencyResultService($rootScope) {
        var service = {};

        service.currency=null;
        service.SetCurrency = SetCurrency;
        service.GetCurrency = GetCurrency;

        return service;

        function GetCurrency() {
            return service.currency;
        }

        function SetCurrency(currency) {
            service.currency=currency;
        }

    }

})();
