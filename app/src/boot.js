'use strict';


import angular from 'angular';
import ngroute from 'angular-route'
import material from 'angular-material'
import jquery from 'jquery'
import _ from 'underscore'

// import main from 'app/main'
// import ctrl from 'app/controller'

// System.import('app/controller');
// System.import('app/main');
var qhackApp = angular.module('qhackApp', [
  'ngRoute',
  'ngMaterial'
]);

qhackApp.controller('HomeCtrl', ['$scope','$location',function($scope, $location) {
    $scope.Play = function(){
        $location.path("/quiz");
    }
}]);

qhackApp.controller('QuizCtrl', ['$scope','$location','$http',function($scope,$location, $http) {

    $scope.radioData = {
        choice: ''
      };
      var id = null;
    $http.get("http://192.168.50.64:80/api/questions")
    .success(function(data) {id = data[0]; $scope.question = data[1];$scope.choices = data[2];});

    $scope.submit = function() {
      alert('submit');
    };
    //console.log($scope.radioData.id);
    //
    // $scope.Submit = function() {
    //   var r = Math.ceil(Math.random() * 1000);
    //   $scope.radioData.push({ label: r, value: r });
    // };

    $scope.Confirm = function() {
        var message = {
            'id': id,
            'answer': $scope.radioData.choice
        }

      $http.post('http://192.168.50.64:80/api/questions',message)
      .success(function(data) {
          if (data === "CORRECT") {
              $location.path("/success");
          }else{
              $location.path("/failed");
          }

      });
    };
}]);


// qhackApp.factory('quizService', ['$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {
//     var promise;
//     var service = {
//         getQuiz: function($scope, $http) {
//             if ( !promise ) {
//                 promise = $http.get('http://localhost:80/api/questions').then(function (response) {
//                     return response.data;
//                     });
//                 }
//                 return promise;
//         }
//         };
//     return service;
// }]);

qhackApp.config(['$mdThemingProvider',function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .primaryPalette('indigo')
        .accentPalette('blue');
}]);

qhackApp.config(['$routeProvider', '$locationProvider',
  function($routeProvider,$locationProvider) {

    //$locationProvider.html5Mode(true);

    $routeProvider
    .when('/home', {
        templateUrl: '/views/content.html',
        controller: 'HomeCtrl'
    })
    .when('/quiz', {
        templateUrl: '/views/quiz.html',
        controller: 'QuizCtrl'
    })
    .when('/failed', {
        templateUrl: '/views/failed.html',
        //controller: 'QuizCtrl'
    })
    .when('/success', {
        templateUrl: '/views/success.html',
        //controller: 'QuizCtrl'
    })
    .otherwise({ redirectTo: '/home' });

  }]);


//Refer to http://stackoverflow.com/questions/16674279/how-to-nest-ng-view-inside-ng-include
qhackApp.run(['$route', function($route)  {
  $route.reload();
}]);
