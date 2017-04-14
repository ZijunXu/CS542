(function () {

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['ItemService', '$location', '$window','$rootScope','AuthenticationService'];
    function itemController(ItemService, $location, $window, $rootScope, AuthenticationService) {
        var vm = this;

        vm.history = history;
        vm.search = search;
        vm.logout = logout;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function search() {
            ItemService.SearchItem(vm.name)
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        $rootScope.itemsresult=response;
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
                    if (response != null) {
                        //use response to update page
                        $rootScope.history=response;
                        $location.path('/history');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function logout() {
            if (AuthenticationService.isLogged) {
                AuthenticationService.isLogged = false;
                delete localStorage.token;
                $location.path("/");
            }
        }

    }

})();