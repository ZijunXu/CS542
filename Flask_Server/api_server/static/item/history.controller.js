/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HistoryController', HistoryController);

    HistoryController.$inject = ['$rootScope', 'ItemService', 'FlashService', 'AuthenticationService', '$location'];
    function HistoryController($rootScope, ItemService, FlashService, AuthenticationService, $location) {
        var vm = this;
        vm.isAdmin=AuthenticationService.isAdmin;

        vm.remove = remove;
        vm.logout = logout;

        function logout() {
            AuthenticationService.isLogged = false;
            AuthenticationService.isAdmin = false;
            delete localStorage.token;
            $location.path("/");
        }

        function remove(index) {
            var sid = $rootScope.history[index].sid;
            ItemService.removeHistory(sid)
                .then(function (response) {
                    if (response.delete_history_status == "Success") {
                        //use response to update page
                        FlashService.Success('Delete successful', true);
                        $rootScope.history.splice(index, 1);
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

    }

})();
