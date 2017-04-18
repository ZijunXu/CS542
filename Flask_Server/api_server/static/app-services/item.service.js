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
        service.removeHistory = removeHistory;

        return service;

        function SearchItem(item) {
            console.log(item);
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

         function removeHistory(sid) {
            return $http.delete('/api/user/search/'+sid).then(handleSuccess, handleError('Error creating user'));
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
