/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('MyPostService', MyPostService);

    MyPostService.$inject = ['$rootScope'];
    function MyPostService($rootScope) {
        var service = {};

        service.mypost=null;
        service.SetPost = SetPost;
        service.GetPost = GetPost;

        return service;

        function GetPost() {
            return service.mypost;
        }

        function SetPost(post) {
            service.mypost=post;
        }

    }

})();
