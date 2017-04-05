/**
 * Created by you on 2017/3/21.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['ItemService', '$rootScope','$location','ItemResultService'];
    function HomeController(ItemService, $rootScope, $location, ItemResultService) {
        var vm = this;
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
    }

})();