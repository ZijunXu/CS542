/**
 * Created by youzhou on 4/22/17.
 */
(function () {
    //'use strict';

    angular
        .module('app')
        .controller('ItemResultLogController', ItemResultLogController);

    ItemResultLogController.$inject = ['$location', 'AuthenticationService', '$rootScope', 'ItemService'];
    function ItemResultLogController($location, AuthenticationService, $rootScope, ItemService) {
        var vm = this;
        vm.logout = logout;
        vm.history = history;
        vm.sidsort = sidsort;
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
        vm.sortByLevel1 = sortByLevel1;
        vm.sortByStrength = sortByStrength;
        vm.sortByIntelligence = sortByIntelligence;
        vm.sortByDexterity = sortByDexterity;
        vm.isAdmin = AuthenticationService.isAdmin;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function sidsort(a, b) {
            if (a.sid < b.sid)
                return 1;
            else if (a.sid > b.sid)
                return -1;
            else
                return 0;
        }

        function history() {
            ItemService.History1()
                .then(function (response) {
                    if (typeof(response.retrieve_search_status) == "undefined") {
                        //use response to update page
                        response.sort(sidsort);
                        $rootScope.history = response;
                        $location.path('/history');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function sortByStrength() {
            $rootScope.itemsresultlog.sort(function (a, b) {
                if (typeof(a.requirements) == "undefined")
                    return 1;
                if (typeof(b.requirements) == "undefined")
                    return -1;
                if (typeof(a.requirements.Str) == "undefined")
                    return 1;
                if (typeof(b.requirements.Str) == "undefined")
                    return -1;

                if (a.requirements.Str < b.requirements.Str)
                    return 1;
                else if (a.requirements.Str > b.requirements.Str)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByLevel1() {
            $rootScope.itemsresultlog.sort(function (a, b) {
                if (typeof(a.requirements) == "undefined")
                    return 1;
                if (typeof(b.requirements) == "undefined")
                    return -1;
                if (typeof(a.requirements.Level) == "undefined")
                    return 1;
                if (typeof(b.requirements.Level) == "undefined")
                    return -1;

                if (a.requirements.Level < b.requirements.Level)
                    return 1;
                else if (a.requirements.Level > b.requirements.Level)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByIntelligence() {
            $rootScope.itemsresultlog.sort(function (a, b) {
                if (typeof(a.requirements) == "undefined")
                    return 1;
                if (typeof(b.requirements) == "undefined")
                    return -1;
                if (typeof(a.requirements.Int) == "undefined")
                    return 1;
                if (typeof(b.requirements.Int) == "undefined")
                    return -1;

                if (a.requirements.Int < b.requirements.Int)
                    return 1;
                else if (a.requirements.Int > b.requirements.Int)
                    return -1;
                else
                    return 0;
            });
        }

        function sortByDexterity() {
            $rootScope.itemsresultlog.sort(function (a, b) {
                if (typeof(a.requirements) == "undefined")
                    return 1;
                if (typeof(b.requirements) == "undefined")
                    return -1;
                if (typeof(a.requirements.Dex) == "undefined")
                    return 1;
                if (typeof(b.requirements.Dex) == "undefined")
                    return -1;

                if (a.requirements.Dex < b.requirements.Dex)
                    return 1;
                else if (a.requirements.Dex > b.requirements.Dex)
                    return -1;
                else
                    return 0;
            });
        }


        function sortByQuality() {
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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
            $rootScope.itemsresultlog.sort(function (a, b) {
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