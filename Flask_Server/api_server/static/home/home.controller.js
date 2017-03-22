/**
 * Created by you on 2017/3/21.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['SearchService', '$rootScope'];
    function HomeController(SearchService, $rootScope) {
        var vm = this;

        vm.item = null;
        //vm.allUsers = [];
        //vm.deleteUser = deleteUser;

        initController();

        function initController() {
            loadCurrentUser();
            loadAllUsers();
        }

        // function loadCurrentUser() {
        //     UserService.GetByUsername($rootScope.globals.currentUser.username)
        //         .then(function (user) {
        //             vm.user = user;
        //         });
        // }
        //
        // function loadAllUsers() {
        //     UserService.GetAll()
        //         .then(function (users) {
        //             vm.allUsers = users;
        //         });
        // }
        //
        // function deleteUser(username) {
        //     UserService.Delete(username)
        //     .then(function () {
        //         loadAllUsers();
        //     });
        // }
    }

})();