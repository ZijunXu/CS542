/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('MyPostController', MyPostController);

    MyPostController.$inject = ['$rootScope','$location','MyPostService'];
    function MyPostController($rootScope, $location, MyPostService) {
        var vm = this;

        vm.posts=MyPostService.GetPost();  //需监听
    }

})();