/**
 * Created by you on 2017/3/21.
 */
(function () {

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['ItemService', '$rootScope','$location','$window'];
    function HomeController(ItemService, $rootScope, $location, $window) {
        var vm = this;
        vm.corrupted="either";
        vm.lists=["either","Yes","No"];
        vm.item={name:vm.name, corrupted:vm.corrupted};

        vm.search = search;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function search() {
            ItemService.SearchItem(vm.item)
                .then(function (response) {
                    if (response!=null) {
                        //use response to update page
                        $rootScope.itemsresult=response;
                        alert($rootScope.itemsresult);
                        $location.path('/item_result');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();