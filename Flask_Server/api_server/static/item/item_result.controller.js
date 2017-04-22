/**
 * Created by you on 2017/3/23.
 */
(function () {
    //'use strict';

    angular
        .module('app')
        .controller('ItemResultController', ItemResultController);

    ItemResultController.$inject = ['$location', 'AuthenticationService', '$rootScope', 'ItemService'];
    function ItemResultController($location, AuthenticationService, $rootScope, ItemService) {
        var vm = this;
        vm.logout = logout;
        vm.sortByPhys = sortByPhys;
        vm.sortByArmour = sortByArmour;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function sortByPhys() {
            $rootScope.itemsresult.sort(ItemService.sortPhys);
        }

        function sortByArmour() {
            $rootScope.itemsresult.sort(ItemService.sortArmour);
        }


    }

})();