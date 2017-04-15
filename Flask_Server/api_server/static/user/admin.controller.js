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
        vm.league = "Legacy";
        vm.type = "any";
        vm.base = "any";
        vm.currency = "Select";
        vm.rarity = "any";
        vm.identified = "either";
        vm.corrupted = "either";
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

        vm.item = {
            name: vm.name,
            physical_damage: (vm.damage_min + vm.damage_max) / 2,
            attacks_per_Second: (vm.APS_min + vm.APS_max) / 2,
            critical_strike_chance: (vm.crit_min + vm.crit_max) / 2,
            DPS: (vm.dps_min + vm.dps_max) / 2,
            eDPS: (vm.edps_min + vm.edps_max) / 2,
            min_armour: vm.armour_min,
            max_armour: vm.armour_max,
            min_evasion: vm.evasion_min,
            max_evasion: vm.evasion_max,
            min_shield: vm.shield_min,
            max_shield: vm.shield_max,
            block_min: vm.block_min,
            block_max: vm.block_max,
            min_socket_number: vm.sockets_min,
            max_socket_number: vm.sockets_min,
            min_link_number: vm.link_min,
            max_link_number: vm.link_max,
            CR: vm.CR,
            CG: vm.CG,
            CB: vm.CB,
            CW: vm.CW,
            LR: vm.LR,
            LG: vm.LG,
            LB: vm.LB,
            LW: vm.LW,
            min_requirements_lvl: vm.rlevel_min,
            max_requirements_lvl: vm.rlevel_max,
            min_requirements_str: vm.rstr_min,
            max_requirements_str: vm.rstr_min,
            min_requirements_dex: vm.rdex_min,
            max_requirements_dex: vm.rdex_max,
            min_requirements_int: vm.rint_min,
            max_requirements_int: vm.rint_max,
            seller: vm.seller,
            quality_min: vm.q_min,
            quality_max: vm.q_max,
            LT_min: vm.level_min,
            LT_max: vm.level_max,
            min_ilvl: vm.ilvl_min,
            max_ilvl: vm.ilvl_max,
            identified: vm.identified,
            corrupted: vm.corrupted,
            rarity: vm.rarity,
            currency: vm.currency,
            base: vm.base,
            typeLine: vm.type,
            league: vm.league
        };

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
                    if (response != null) {
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