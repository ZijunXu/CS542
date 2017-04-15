/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HistoryController', HistoryController);

    HistoryController.$inject = ['$rootScope', '$scope'];
    function HistoryController($rootScope, $scope) {
        var vm = this;
    }

})();
