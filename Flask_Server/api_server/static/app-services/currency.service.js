/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('CurrencyService', CurrencyService);

    CurrencyService.$inject = ['$http','$httpParamSerializerJQLike'];
    function CurrencyService($http,$httpParamSerializerJQLike) {
        var service = {};

        service.SearchCurrency = SearchCurrency;
        service.PostCurrency = PostCurrency;
        service.MyPost = MyPost;
        service.Update = Update;
        service.Delete = Delete;

        return service;

         function SearchCurrency(currency) {
            return $http({
                url: '/api/currency',
                method: 'GET',
                data: $httpParamSerializerJQLike(currency),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error searching currency'));
        }

        function PostCurrency(currency) {
            return $http({
                url: '/api/*****',
                method: 'POST',
                data: $httpParamSerializerJQLike(currency),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error posting currency'));
        }

         function MyPost() {
            return $http({
                url: '/api/user/post',
                method: 'GET',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error seeking mypost'));
        }

          function Update(post) {
            return $http({
                url: '/api/*****',
                method: 'POST',
                data: $httpParamSerializerJQLike(post),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error updating your post'));
        }

        function Delete(id) {
            return $http({
                url: '/api/*****',
                method: 'DELETE',
                data: $httpParamSerializerJQLike(id),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(handleSuccess, handleError('Error deleting your post'));
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
