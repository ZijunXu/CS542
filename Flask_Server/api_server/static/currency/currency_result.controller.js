/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('CurrencyResultController', CurrencyResultController);

    CurrencyResultController.$inject = ['$location', '$rootScope'];
    function CurrencyResultController($rootScope) {
        var vm = this;

    }

})();