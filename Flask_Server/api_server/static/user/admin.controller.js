/**
 * Created by you on 2017/4/14.
 */
(function () {

    angular
        .module('app')
        .controller('AdminController', AdminController);

    AdminController.$inject = ['ItemService', '$location', '$window', '$rootScope', 'AuthenticationService'];
    function AdminController(ItemService, $location, $window, $rootScope, AuthenticationService) {
        var vm = this;
        // vm.league = "Legacy";
        // vm.type = "any";
        // vm.base = "any";
        // vm.currency = "Select";
        // vm.rarity = "any";
        // vm.identified = "either";
        // vm.corrupted = "either";
        vm.list1 = ["Legacy", "Hardcore Legacy", "Standard", "Hardcore"];
        vm.list2 = ["any", "Generic One-Handed Weapon", "Generic Two-Handed Weapon", "Bow", "Claw", "Dagger", "One Hand Axe", "One Hand Mace", "One Hand Sword"
            , "Sceptre", "Staff", "Two Hand Axe", "Two Hand Mace", "Two Hand Sword", "Wand", "Body Armour", "Boots", "Gloves", "Helmet", "Shield", "Amulet", "Belt"
            , "Breach", "Currency", "Divination Card", "Essence", "Fishing Rods", "Flask", "Gem", "Jewel", "Leaguestone", "Map", "Prophecy", "Quiver", "Ring", "Map Fragments"];
        vm.list3 = ["any"];
        vm.list4 = ["Select", "Blessed Orb", "Cartographer's Chisel", "Chaos Orb", "Chromatic Orb", "Divine Orb", "Exalted Orb", "Gemcutter's Prism", "Jeweller's Orb",
            "Orb of Alchemy", "Orb of Alteration", "Orb of Chance", "Orb of Fusing", "Orb of Regret", "Orb of Scouring", "Regal Orb", "Vaal Orb", "Perandus Coin", "Silver Coin"];
        vm.list5 = ["any", "Normal", "Magic", "Rare", "Unique", "Relic"];
        vm.list6 = ["either", "Yes", "No"];
        vm.list7 = ["either", "Yes", "No"];

        vm.history = history;
        vm.search = search;
        vm.logout = logout;

        vm.reloadRoute = function () {
            $window.location.reload();
        };

        function search() {
            ItemService.SearchItem(vm.item)
                .then(function (response) {
                    if (response != null) {
                        //use response to update page
                        $rootScope.itemsresult = response;
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
                    if (typeof(response.retrieve_search_status) == "undefined") {
                        //use response to update page
                        $rootScope.history = response;
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