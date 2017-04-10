/**
 * Created by you on 2017/3/19.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('ItemService', ItemService);

    ItemService.$inject = ['$http', '$httpParamSerializerJQLike'];
    function ItemService($http, $httpParamSerializerJQLike) {
        var service = {};

        service.SearchItem = SearchItem;
        service.History = History;

        return service;

        // function GetItem() {
        //     return $http.get('/api/*******/').then(handleSuccess, handleError('Error getting item back'));
        // }

        function SearchItem(item) {
            alert(item);
            return $http({
                url: '/api/item',
                method: 'POST',
                data: $httpParamSerializerJQLike({owner: item}),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error posting item by content'));
            //$http.post('/api/item', {owner: item})
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
