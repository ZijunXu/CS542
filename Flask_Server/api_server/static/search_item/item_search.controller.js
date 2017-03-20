(function () {
    'use strict';

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['SearchService', '$rootScope'];
    function itemController(SearchService, $rootScope) {
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