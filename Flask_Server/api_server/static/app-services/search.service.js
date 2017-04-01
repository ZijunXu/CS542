/**
 * Created by you on 2017/3/19.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('SearchService', SearchService);

    SearchService.$inject = ['$http'];
    function SearchService($http) {
        var service = {};

        service.SearchItem = SearchItem;
        service.SearchCurrency = SearchCurrency;
        service.PostCurrency = PostCurrency;

        return service;

        // function GetItem() {
        //     return $http.get('/api/*******/').then(handleSuccess, handleError('Error getting item back'));
        // }

        function SearchItem(item) {
            return $http.post('/api/item', item).then(handleSuccess, handleError('Error posting item by content'));
        }

        function SearchCurrency(currency) {
            return $http.post('/api/*****', currency).then(handleSuccess, handleError('Error posting item by content'));
        }

        function PostCurrency(currency) {
            return $http.post('/api/*****', currency).then(handleSuccess, handleError('Error posting item by content'));
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
