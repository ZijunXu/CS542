(function () {
    'use strict';

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['UserService', '$rootScope','SearchService'];
    function itemController(UserService, $rootScope, SearchService, $location) {
        var vm = this;
        vm.user = null;
        vm.item = null;
        vm.allUsers = [];
        //vm.deleteUser = deleteUser;

        initController();

        function initController() {
            loadCurrentUser();
            loadAllUsers();
        }

         function loadCurrentUser() {
             UserService.GetByUsername($rootScope.globals.currentUser.username)
                 .then(function (user) {
                     vm.user = user;
                 });
         }

         function loadAllUsers() {
             UserService.GetAll()
                 .then(function (users) {
                     vm.allUsers = users;
                 });
         }
        //
        // function deleteUser(username) {
        //     UserService.Delete(username)
        //     .then(function () {
        //         loadAllUsers();
        //     });
        // }
    }

})();