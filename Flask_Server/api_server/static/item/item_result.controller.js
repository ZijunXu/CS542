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
        vm.sortByQuality = sortByQuality;
        vm.sortByArmour = sortByArmour;
        vm.sortByLevel = sortByLevel;
        vm.sortByEvasion = sortByEvasion;
        vm.sortByIlvl = sortByIlvl;
        vm.sortByShield = sortByShield;
        vm.sortByAPS = sortByAPS;
        vm.sortByBlock = sortByBlock;
        vm.sortByDPS = sortByDPS;
        vm.sortByCrit = sortByCrit;
        vm.sortByeDPS = sortByeDPS;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }


        function sortByQuality() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties.Quality) == "undefined")
                    return 1;
                if (typeof(b.properties.Quality) == "undefined")
                    return -1;

                if (a.properties.Quality < b.properties.Quality)
                    return 1;
                else if (a.properties.Quality > b.properties.Quality)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByLevel() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties.Level) == "undefined")
                    return 1;
                if (typeof(b.properties.Level) == "undefined")
                    return -1;

                if (a.properties.Level < b.properties.Level)
                    return 1;
                else if (a.properties.Level > b.properties.Level)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByEvasion() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Evasion Rating']) == "undefined")
                    return 1;
                if (typeof(b.properties['Evasion Rating']) == "undefined")
                    return -1;

                if (a.properties['Evasion Rating'] < b.properties['Evasion Rating'])
                    return 1;
                else if (a.properties['Evasion Rating'] > b.properties['Evasion Rating'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByIlvl() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.ilvl) == "undefined")
                    return 1;
                if (typeof(b.ilvl) == "undefined")
                    return -1;

                if (a.ilvl < b.ilvl)
                    return 1;
                else if (a.ilvl > b.ilvl)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByShield() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Energy Shield']) == "undefined")
                    return 1;
                if (typeof(b.properties['Energy Shield']) == "undefined")
                    return -1;

                if (a.properties['Energy Shield'] < b.properties['Energy Shield'])
                    return 1;
                else if (a.properties['Energy Shield'] > b.properties['Energy Shield'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByAPS() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Attacks per Second']) == "undefined")
                    return 1;
                if (typeof(b.properties['Attacks per Second']) == "undefined")
                    return -1;

                if (a.properties['Attacks per Second'] < b.properties['Attacks per Second'])
                    return 1;
                else if (a.properties['Attacks per Second'] > b.properties['Attacks per Second'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByBlock() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Chance to Block']) == "undefined")
                    return 1;
                if (typeof(b.properties['Chance to Block']) == "undefined")
                    return -1;

                if (a.properties.Armour < b.properties.Armour)
                    return 1;
                else if (a.properties['Chance to Block'] > b.properties['Chance to Block'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByDPS() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Physical Damage']) == "undefined")
                    return 1;
                if (typeof(b.properties['Physical Damage']) == "undefined")
                    return -1;

                if (a.properties['Physical Damage'] < b.properties['Physical Damage'])
                    return 1;
                else if (a.properties['Physical Damage'] > b.properties['Physical Damage'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByCrit() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Critical Strike Chance']) == "undefined")
                    return 1;
                if (typeof(b.properties['Critical Strike Chance']) == "undefined")
                    return -1;

                if (a.properties['Critical Strike Chance'] < b.properties['Critical Strike Chance'])
                    return 1;
                else if (a.properties['Critical Strike Chance'] > b.properties['Critical Strike Chance'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByeDPS() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties['Elemental Damage']) == "undefined")
                    return 1;
                if (typeof(b.properties['Elemental Damage']) == "undefined")
                    return -1;

                if (a.properties['Elemental Damage'] < b.properties['Elemental Damage'])
                    return 1;
                else if (a.properties['Elemental Damage'] > b.properties['Elemental Damage'])
                    return -1;
                else
                    return 0;
            });
        }

        function sortByArmour() {
            $rootScope.itemsresult.sort(function (a, b) {
                if (typeof(a.properties) == "undefined")
                    return 1;
                if (typeof(b.properties) == "undefined")
                    return -1;
                if (typeof(a.properties.Armour) == "undefined")
                    return 1;
                if (typeof(b.properties.Armour) == "undefined")
                    return -1;

                if (a.properties.Armour < b.properties.Armour)
                    return 1;
                else if (a.properties.Armour > b.properties.Armour)
                    return -1;
                else
                    return 0;
            });
        }


    }

})();