/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('CurrencyService', CurrencyService);

    CurrencyService.$inject = ['$http'];
    function CurrencyService($http) {
        var service = {};

        service.SearchCurrency = SearchCurrency;
        service.PostCurrency = PostCurrency;
        service.MyPost = MyPost;
        service.Update = Update;
        service.Delete = Delete;

        return service;

        function SearchCurrency(currency) {
            return $http.post('/api/*****', currency).then(handleSuccess, handleError('Error posting item by content'));
        }

        function PostCurrency(currency) {
            return $http.post('/api/*****', currency).then(handleSuccess, handleError('Error posting item by content'));
        }

        function MyPost() {
            return $http.get('/api/*****').then(handleSuccess, handleError('Error posting item by content'));
        }

         function Update(post) {
            return $http.put('/api/*****', post).then(handleSuccess, handleError('Error posting item by content'));
        }

        function Delete(id) {
            return $http.delete('/api/*****'+id).then(handleSuccess, handleError('Error posting item by content'));
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
