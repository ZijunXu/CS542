/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('MyPostController', MyPostController);

    MyPostController.$inject = ['$rootScope','$location'];
    function MyPostController($rootScope, $location) {
        var vm = this;

    }

})();