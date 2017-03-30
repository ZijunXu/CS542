/**
 * Created by you on 2017/3/21.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['SearchService', '$rootScope','$location','ItemResultService'];
    function HomeController(SearchService, $rootScope, $location, ItemResultService) {
        var vm = this;
        vm.search = search;

        function search() {
            SearchService.PostItem(vm.name)
                .then(function (response) {
                    if (response.data!=null) {
                        //use response to update page
                         console.log(response.data);
                         ItemResultService.SetItem(response.data);
                        $location.path('/item');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();