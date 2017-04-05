/**
 * Created by you on 2017/4/4.
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('HistoryService', HistoryService);

    HistoryService.$inject = ['$rootScope'];
    function HistoryService($rootScope) {
        var service = {};

        service.history=null;
        service.SetHistory = SetHistory;
        service.GetHistory = GetHistory;

        return service;

        function GetHistory() {
            return service.history;
        }

        function SetHistory(history) {
            service.history=history;
        }

    }

})();
