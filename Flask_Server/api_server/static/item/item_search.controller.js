(function () {
    'use strict';

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['ItemService', '$rootScope','$location','ItemResultService','HistoryService'];
    function itemController(ItemService, $rootScope, $location, ItemResultService, HistoryService) {
        var vm = this;

        vm.history=history;
        vm.search = search;

        function search() {
            ItemService.SearchItem(vm.name)
                .then(function (response) {
                    if (response.data!=null) {
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
                    if (response.data!=null) {
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