/**
 * Created by you on 2017/3/23.
 */
(function () {
    //'use strict';

    angular
        .module('app')
        .controller('ItemResultController', ItemResultController);

    ItemResultController.$inject = ['$location', '$scope', 'ItemResultService', '$timeout','$rootScope'];
    function ItemResultController(ItemResultService, $timeout, $scope,$rootScope) {
        // $scope.user = {name: "Fox"};
        //
        // $scope.updated = -1;
        //
        // var watch = $scope.$watch('user', function (newValue, oldValue) {
        //     if (newValue === oldValue) {
        //         return;
        //     }
        //     $scope.updated++;
        //
        //     $scope.$broadcast('userUpdate', newValue.name);
        // });
        //
        // //watch();
        // var i = 0;
        //
        // $scope.$on('userUpdate', function (d, data) {
        //     console.info(data);
        // })
        //
        // $scope.getScope = function () {
        //     // console.info(this);
        //     var obj = $("#btnTest");
        //     i++;
        //     angular.element(obj).scope().user.name = "hello" + i;
        // }
        var vm = this;
        vm.test="title";
        // $timeout(function () {
        //         vm.items = ItemResultService.items;
        //     },
        //     1000);
        // setTimeout(function () {
        //     //vm.test = ItemResultService;
        //     alert($rootScope.it);
        // }, 2000);
        // $scope.$watch('vm.test', function (newValue, oldValue) {
        //     if (newValue != oldValue) {
        //         vm.items = newValue;
        //     }
        // }, true);


        // alert(vm.items);
        // vm.items = ItemResultService.items;
        //
        // vm.result = result;
        //
        // function result(item) {
        //
        //     SearchService.PostItem(vm.name)
        //         .then(function (response) {
        //             if (response.data != null) {
        //                 //use response to update page
        //                 console.log(response.data);
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