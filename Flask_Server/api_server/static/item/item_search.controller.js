(function () {
    'use strict';

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['ItemService', '$location', 'ItemResultService', 'HistoryService','$window'];
    function itemController(ItemService, $location, ItemResultService, HistoryService,$window) {
        var vm = this;

        vm.test2="呵呵";

        vm.history = history;
        vm.search = search;

        vm.reloadRoute = function () {
            $window.location.reload();
        };
    }

})();