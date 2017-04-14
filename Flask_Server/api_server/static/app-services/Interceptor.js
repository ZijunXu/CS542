/**
 * Created by you on 2017/4/14.
 */
(function () {
    'use strict';

     angular
        .module('app')
        .config(['$httpProvider', function ($httpProvider) {
            $httpProvider.interceptors.push(HttpInterceptor);
        }]);

    angular
        .module('app')
        .factory('HttpInterceptor', ['$q', HttpInterceptor]);

    function HttpInterceptor($q) {
        return {
            // 请求发出之前，可以用于添加各种身份验证信息
            request: function (config) {
                if (localStorage.token) {
                    config.headers.token = localStorage.token;
                    console.log(config.headers.token);
                }
                return config;
            },
            // 请求发出时出错
            requestError: function (err) {
                return $q.reject(err);
            },
            // 成功返回了响应
            response: function (res) {
                return res;
            },
            // 返回的响应出错，包括后端返回响应时，设置了非 200 的 http 状态码
            responseError: function (err) {
                if (-1 === err.status) {
                    // 远程服务器无响应
                } else if (401 === err.status) {
                    // 401 错误一般是用于身份验证失败，具体要看后端对身份验证失败时抛出的错误
                } else if (404 === err.status) {
                    // 服务器返回了 404
                }
                return $q.reject(err);
            }
        };
    }

})();