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

        function search() {
            ItemService.SearchItem(vm.name)
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        console.log(response.data);
                        ItemResultService.SetItem(response.data);
                        $location.path('/item_result');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function history() {
            ItemService.History()
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        console.log(response.data);
                        HistoryService.SetHistory(response.data);
                        $location.path('/history');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();