/**
 * Created by you on 2017/3/23.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('ItemResultController', ItemResultController);

    ItemResultController.$inject = ['$location', '$rootScope','ItemResultService'];
    function ItemResultController($rootScope, ItemResultService) {
        var vm = this;

        vm.item=ItemResultService.GetItem();

        // vm.result = result;
        //
        // function result(item) {
        //
        //     SearchService.PostItem(vm.name)
        //         .then(function (response) {
        //             if (response.data!=null) {
        //                 //use response to update page
        //                  console.log(response.data);
        //                 $location.path('/user');
        //             } else {
        //                 FlashService.Error(response.message);
        //                 vm.dataLoading = false;
        //             }
        //         });
        //
        // }
    }

})();