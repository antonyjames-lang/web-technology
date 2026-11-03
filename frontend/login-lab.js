(function () {
  'use strict';

  var app = angular.module('loginLabApp', []);

  app.factory('AuthService', ['$http', function ($http) {
    var apiUrl = window.location.port === '8000' ? '/api' : 'http://localhost:8000/api';

    return {
      requestCode: function (email) {
        return $http.post(apiUrl + '/auth/request-otp', { email: email });
      },
      verifyCode: function (email, code) {
        return $http.post(apiUrl + '/auth/verify-otp', { email: email, code: code });
      }
    };
  }]);

  app.controller('LoginCtrl', ['$scope', 'AuthService', function ($scope, AuthService) {
    var savedUser = null;
    try {
      savedUser = JSON.parse(localStorage.getItem('ym_user') || 'null');
    } catch (error) {
      savedUser = null;
    }

    $scope.gmailPattern = /^[A-Za-z0-9._%+-]+@gmail\.com$/i;
    $scope.codePattern = /^\d{6}$/;
    $scope.login = {
      email: savedUser && savedUser.email || '',
      code: '',
      otpRequested: false,
      devOtp: null,
      loading: false,
      error: '',
      message: '',
      signedIn: Boolean(localStorage.getItem('ym_token'))
    };

    $scope.requestOtp = function (form, resend) {
      if (form && !resend && form.$invalid) {
        form.$setSubmitted();
        return;
      }

      $scope.login.loading = true;
      $scope.login.error = '';
      $scope.login.message = '';

      AuthService.requestCode($scope.login.email.trim().toLowerCase()).then(function (response) {
        $scope.login.otpRequested = true;
        $scope.login.devOtp = response.data.dev_otp || null;
        $scope.login.message = response.data.message || 'A sign-in code has been sent.';
      }).catch(function (response) {
        $scope.login.error = response.data && response.data.message || 'Could not send a sign-in code. Try again.';
      }).finally(function () {
        $scope.login.loading = false;
      });
    };

    $scope.verifyOtp = function (form) {
      if (form.$invalid) {
        form.$setSubmitted();
        return;
      }

      $scope.login.loading = true;
      $scope.login.error = '';
      $scope.login.message = '';

      AuthService.verifyCode($scope.login.email.trim().toLowerCase(), $scope.login.code).then(function (response) {
        localStorage.setItem('ym_token', response.data.token);
        localStorage.setItem('ym_user', JSON.stringify(response.data.user));
        $scope.login.signedIn = true;
      }).catch(function (response) {
        $scope.login.error = response.data && response.data.message || 'That code could not be verified. Try again.';
      }).finally(function () {
        $scope.login.loading = false;
      });
    };

    $scope.fillDevOtp = function () {
      $scope.login.code = $scope.login.devOtp;
    };

    $scope.changeEmail = function () {
      $scope.login.otpRequested = false;
      $scope.login.code = '';
      $scope.login.devOtp = null;
      $scope.login.error = '';
      $scope.login.message = '';
    };

    $scope.signOut = function () {
      localStorage.removeItem('ym_token');
      localStorage.removeItem('ym_user');
      $scope.login.signedIn = false;
      $scope.login.code = '';
      $scope.changeEmail();
    };
  }]);
}());