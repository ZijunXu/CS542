/**
 * Created by you on 2017/3/23.
 */
(function () {
    //'use strict';

    angular
        .module('app')
        .controller('ItemResultController', ItemResultController);

    ItemResultController.$inject = [ '$scope', '$timeout','$rootScope'];
    function ItemResultController( $timeout, $scope,$rootScope) {
        var vm = this;

    }

})();