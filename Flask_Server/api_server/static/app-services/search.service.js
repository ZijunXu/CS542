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

        service.PostItem = PostItem;
        // service.GetItem = GetItem;

        return service;

        // function GetItem() {
        //     return $http.get('/api/*******/').then(handleSuccess, handleError('Error getting item back'));
        // }

        function PostItem(item) {
            return $http.post('/api/item',item).then(handleSuccess, handleError('Error posting item by content'));
        }

        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return { success: false, message: error };
            };
        }
    }

})();
