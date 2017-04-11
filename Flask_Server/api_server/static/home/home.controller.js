/**
 * Created by you on 2017/3/21.
 */
(function () {

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['ItemService', '$rootScope','$location','ItemResultService'];
    function HomeController(ItemService, $rootScope, $location, ItemResultService) {
        var vm = this;
        // vm.lists=["either","Yes","No"];
        // vm.item={name:vm.name};

        vm.search = search;

        function search() {
            ItemService.SearchItem(vm.item)
                .then(function (response) {
                    if (response!=null) {
                        //use response to update page
                         //$location.path('/item_result');
                         alert(response[1]._id);
                         vm.items=response;
                         console(items[1]._id);
                        //ItemResultService.SetItem(response);
                        //$location.path('/item_result');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();