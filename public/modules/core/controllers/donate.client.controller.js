'use strict';



angular.module('core')
.controller('DonateController', ['$scope', '$http',
	function($scope, $http) {

    $scope.message = 'Please use the form below to pay:';
    $scope.showDropinContainer = true;
    $scope.isError = false;
    $scope.isPaid = false;

    $scope.getToken = function () {

      $http({
        method: 'GET',
        url: 'http://localhost:3000/client_token'
      }).success(function (data) {

        console.log(data);

        braintree.setup(data, 'dropin', {
          container: 'checkout',
          // Form is not submitted by default when paymentMethodNonceReceived is implemented
          paymentMethodNonceReceived: function (event, nonce) {

            $scope.message = 'Processing your payment...';
            $scope.showDropinContainer = false;

            $http({
              method: 'POST',
              url: 'http://localhost:3000/payment-methods',
              data: {
                amount: $scope.amount,
                payment_method_nonce: nonce
              }
            }).success(function (data) {

              console.log(data);

              if (data) {
                $scope.message = 'Payment authorized, thanks.';
                $scope.showDropinContainer = false;
                $scope.isError = false;
                $scope.isPaid = true;

              } else {
                // implement your solution to handle payment failures
                $scope.message = 'Payment failed: ' + data + ' Please refresh the page and try again.';
                $scope.isError = true;
              }

            }).error(function (error) {
              $scope.message = 'Error: cannot connect to server. Please make sure your server is running.';
              $scope.showDropinContainer = false;
              $scope.isError = true;
            });

          }
        });

      }).error(function (error) {
        $scope.message = 'Error: cannot connect to server. Please make sure your server is running.';
        $scope.showDropinContainer = false;
        $scope.isError = true;
      });

    };

    $scope.getToken();

  }]);
