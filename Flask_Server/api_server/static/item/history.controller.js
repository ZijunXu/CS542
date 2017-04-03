/**
 * Created by you on 2017/3/31.
 */
// vm.contents = [
//     {time: 3.21, content: "sword"},
//     {time: 2.31, content: "sword"},
//     {time: 1.31, content: "helmet"}
// ];

// vm.time1 = 3.31;
// vm.time2 = 3.11;
// vm.content1 = "sword";
// vm.content2 = "helmet";
// vm.search = search;

// function search() {
//     SearchService.SearchItem(vm.name)
//         .then(function (response) {
//             if (response.data!=null) {
//                 //use response to update page
//                  console.log(response.data);
//                  ItemResultService.SetItem(response.data);
//                 $location.path('/item_result');
//             } else {
//                 FlashService.Error(response.message);
//                 vm.dataLoading = false;
//             }
//         });
// }

(function () {
    'use strict';

    angular
        .module('app')
        .controller('HistoryController', HistoryController);

    HistoryController.$inject = ['UserService', '$rootScope', '$scope'];
    function HistoryController(UserService, $rootScope, $scope) {
        var vm = this;
        vm.items = [
            {name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00},
            {name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00},
            {name: "AngularJS权威教程", quantity: 2, price: 84.20},

            {name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00},
            {name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00},
            {name: "AngularJS权威教程", quantity: 2, price: 84.20},

            {name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00},
            {name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00},
            {name: "AngularJS权威教程", quantity: 2, price: 84.20},

            {name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00},
            {name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00},
            {name: "AngularJS权威教程", quantity: 2, price: 84.20}
        ];
    }

})();
