/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HistoryController', HistoryController);

    HistoryController.$inject = ['$rootScope', 'ItemService', 'FlashService'];
    function HistoryController($rootScope, ItemService, FlashService) {
        var vm = this;

        vm.remove = remove;

        function remove(index) {
            var sid = $rootScope.history[index].sid;
            ItemService.removeHistory(sid)
                .then(function (response) {
                    if (response.delete_history_status == "Success") {
                        //use response to update page
                        FlashService.Success('Delete successful', true);
                        $rootScope.history.splice(index,1);
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

    }

})();
