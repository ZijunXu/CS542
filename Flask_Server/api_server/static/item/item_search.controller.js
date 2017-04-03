(function () {
    'use strict';

    angular
        .module('app')
        .controller('itemController', itemController);

    itemController.$inject = ['UserService', '$rootScope','SearchService','$location'];
    function itemController(UserService, $rootScope, SearchService, $location) {
        var vm = this;
        //vm.user = null;
        vm.item={};
        vm.allUsers = [];
        vm.search = search;
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

        function search() {
            SearchService.SearchItem(vm.name)
                .then(function (response) {
                    if (response.data!=null) {
                        //use response to update page
                         console.log(response.data)
                        $location.path('/login');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();