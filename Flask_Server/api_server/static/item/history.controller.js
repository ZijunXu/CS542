/**
 * Created by you on 2017/3/31.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .controller('HistoryController', HistoryController);

    HistoryController.$inject = ['$rootScope', '$scope'];
    function HistoryController($rootScope, $scope) {
        var vm = this;

        // vm.historys=HistoryService.GetHistory();  //需监听

         // vm.items = [
         //        { name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00 },
         //        { name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00 },
         //        { name: "AngularJS权威教程", quantity: 2, price: 84.20 },
         //
         //        { name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00 },
         //        { name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00 },
         //        { name: "AngularJS权威教程", quantity: 2, price: 84.20 },
         //
         //        { name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00 },
         //        { name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00 },
         //        { name: "AngularJS权威教程", quantity: 2, price: 84.20 },
         //
         //        { name: "雷柏（Rapoo） V500 机械游戏键盘 机械黄轴", quantity: 1, price: 199.00 },
         //        { name: "雷柏（Rapoo） V20 光学游戏鼠标 黑色烈焰版", quantity: 1, price: 139.00 },
         //        { name: "AngularJS权威教程", quantity: 2, price: 84.20 }
         //    ];
    }

})();
