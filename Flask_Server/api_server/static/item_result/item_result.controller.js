/**
 * Created by you on 2017/3/23.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('ItemResultController', ItemResultController);

    ItemResultController.$inject = ['$location', '$rootScope'];
    function ItemResultController($rootScope) {
        var vm = this;
        vm.result = result;

        function result(item) {

            // SearchService.PostItem(vm.name)
            //     .then(function (response) {
            //         if (response.data!=null) {
            //             //use response to update page
            //              console.log(response.data);
            //             $location.path('/login');
            //         } else {
            //             FlashService.Error(response.message);
            //             vm.dataLoading = false;
            //         }
            //     });

        }
    }

})();