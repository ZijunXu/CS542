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
        vm.lists=["either","Yes","No"];
        vm.item={name:vm.name,corrupted:vm.corrupted};

        vm.search = search;

        function search() {
            ItemService.SearchItem(vm.item)
                .then(function (response) {
                     alert(response);
                    if (response.data!=null) {
                        //use response to update page
                         alert(response.data);
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