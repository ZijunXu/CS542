/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('ManagePostController', ManagePostController);

    ManagePostController.$inject = ['$rootScope', '$location', 'CurrencyService'];
    function ManagePostController(CurrencyService, $rootScope, $location) {
        var vm = this;

        vm.b = "钻石王";
        vm.item = "hhhhhhhhhhh";
        vm.what = "hhhhhhhhhhh";
        vm.update = update;
        vm.Delete = Delete;

        function Delete() {
            CurrencyService.Delete(vm.what)
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        alert("success!");
                        $location.path('/manage_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }

        function update() {
            CurrencyService.Update(vm.what)
                .then(function (response) {
                    if (response.data != null) {
                        //use response to update page
                        alert("success!");
                        $location.path('/manage_post');
                    } else {
                        FlashService.Error(response.message);
                        vm.dataLoading = false;
                    }
                });
        }
    }

})();