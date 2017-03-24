/**
 * Created by you on 2017/3/21.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['SearchService', '$rootScope'];
    function HomeController(SearchService,$rootScope,$location) {
        var vm = this;

        vm.search = search();

        function search() {
            SearchService.PostItem(vm.search)
                .then(function (response) {
                    if (response.search_status) {
                        //use response to update page
                        $location.path('/login');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();