(function () {

    angular
        .module('app', ['ngRoute', 'ngCookies'])
        .config(config)
        .run(run);

    config.$inject = ['$routeProvider', '$locationProvider'];
    function config($routeProvider, $location) {
        $routeProvider
            .when('/', {
                controller: 'HomeController',
                templateUrl: '/static/home/home.view.html',
                controllerAs: 'vm'
            })

            .when('/item_search', {
                controller: 'itemController',
                templateUrl: '/static/item/item_search.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/item_result', {
                controller: 'ItemResultController',
                templateUrl: '/static/item/item_result.view.html',
                controllerAs: 'vm'
            })

            .when('/item_resultlog', {
                controller: 'ItemResultLogController',
                templateUrl: '/static/item/item_resultlog.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/login', {
                controller: 'LoginController',
                templateUrl: '/static/user/login.view.html',
                controllerAs: 'vm'
            })

            .when('/register', {
                controller: 'RegisterController',
                templateUrl: '/static/user/register.view.html',
                controllerAs: 'vm'
            })
            .when('/currency_search', {
                controller: 'CurrencySearchController',
                templateUrl: '/static/currency/currency_search.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/currency_result', {
                controller: 'CurrencyResultController',
                templateUrl: '/static/currency/currency_result.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/currency_post', {
                controller: 'CurrencyPostController',
                templateUrl: '/static/currency/currency_post.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/history', {
                controller: 'HistoryController',
                templateUrl: '/static/item/history.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/my_post', {
                controller: 'MyPostController',
                templateUrl: '/static/currency/my_post.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/update_info', {
                controller: 'UpdateController',
                templateUrl: '/static/user/update.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .when('/admanage', {
                controller: 'AdmanageController',
                templateUrl: '/static/user/admanage.view.html',
                controllerAs: 'vm',
                access: {requiredLogin: true}
            })

            .otherwise({redirectTo: '/'});
    }

    run.$inject = ['$rootScope', '$location', 'AuthenticationService'];
    function run($rootScope, $location, AuthenticationService) {
        $rootScope.$on("$routeChangeStart", function (event, nextRoute, currentRoute) {
            //redirect only if both isLogged is false and no token is set
            if (nextRoute != null && nextRoute.access != null && nextRoute.access.requiredLogin
                && !AuthenticationService.isLogged && !localStorage.token) {
                $location.path("/");
            }
        });

        // $rootScope.globals = $cookies.getObject('globals') || {};
        // if ($rootScope.globals.currentUser) {
        //     $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata;
        // }

        // $rootScope.$on('$locationChangeStart', function (event, next, current) {
        //     // redirect to user page if not logged in and trying to access a restricted page
        //     var restrictedPage = $.inArray($location.path(), ['/login', '/register', '/history', '/item_result', '/item_search', '/','/update_info','/manage_post','/my_post','/currency_post','/currency_search']) === -1;
        //     var loggedIn = $rootScope.globals.currentUser;
        //     if (restrictedPage && !loggedIn) {
        //         $location.path('/');
        //     }
        // });
    }

})();