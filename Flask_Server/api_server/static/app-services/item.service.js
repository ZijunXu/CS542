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

        return service;

        // function GetItem() {
        //     return $http.get('/api/*******/').then(handleSuccess, handleError('Error getting item back'));
        // }

        function SearchItem(item) {
            return $http.post('/api/item', item).then(handleSuccess, handleError('Error posting item by content'));
        }

        function History() {
            return $http.get('/api/history').then(handleSuccess, handleError('Error creating user'));
        }

        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return {success: false, message: error};
            };
        }
    }

})();
