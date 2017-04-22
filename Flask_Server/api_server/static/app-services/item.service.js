/**
 * Created by you on 2017/3/19.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('ItemService', ItemService);

    ItemService.$inject = ['$http'];
    function ItemService($http) {
        var service = {};

        service.SearchItem = SearchItem;
        service.History = History;
        service.removeHistory = removeHistory;
        service.sortPhys = sortPhys;
        service.sortArmour = sortArmour;

        return service;

        function SearchItem(item) {
            console.log(item.Mods_content);
            return $http.post('/api/item', item).then(handleSuccess, handleError('Error updating user'));
        }

        function History() {
            return $http({
                url: '/api/user/search',
                method: 'GET',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error seeking history'));
        }

        function removeHistory(sid) {
            return $http.delete('/api/user/search/' + sid).then(handleSuccess, handleError('Error creating user'));
        }

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return {success: false, message: error};
            };
        }

        function sortPhys(a, b) {
            if (a.properties['Physical Damage'] < b.properties['Physical Damage'] ||
                typeof(a.properties['Physical Damage']) == "undefined")
                return 1;
            else if (a.properties['Physical Damage'] > b.properties['Physical Damage'] ||
                typeof(b.properties['Physical Damage']) == "undefined")
                return -1;
            else
                return 0;
        }

        function sortArmour(a, b) {
            if (a.properties.Armour < b.properties.Armour ||
                typeof(a.properties.Armour) == "undefined")
                return 1;
            else if (a.properties.Armour > b.properties.Armour ||
                typeof(b.properties.Armour) == "undefined")
                return -1;
            else
                return 0;
        }
    }

})();
