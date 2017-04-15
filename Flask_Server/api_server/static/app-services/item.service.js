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

        function SearchItem(item) {
            //alert(item);
            return $http({
                url: '/api/item',
                method: 'POST',
                data: $httpParamSerializerJQLike(item),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error searching item'));
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
