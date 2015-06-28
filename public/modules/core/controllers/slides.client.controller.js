'use strict';

var times = 0;

function shuffle(o) {
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
}


// Random Jquery function
angular.module('core').controller('SlidesController', ['$scope', '$document', '$http', '$mdToast', 'Authentication',
	function($scope, $document, $http, $mdToast, Authentication) {
		$scope.authentication = Authentication;

		$scope.question = 'Are you ready to play?';

		user = $scope.authentication.user;

		console.log(user);


		var address = user.address + " " + user.city + ", " + user.state + " " + user.zip;

		$scope.choices = ['Yes', 'No'];
    $scope.pics = []
		$scope.other_choices = $scope.choices.slice(0);

    $scope.toastPosition = {
      bottom: true,
      top: false,
      left: false,
      right: true
    };

      $scope.getToastPosition = function() {
        return Object.keys($scope.toastPosition)
          .filter(function(pos) { return $scope.toastPosition[pos]; })
          .join(' ');
      };

    $scope.correctToast = function() {
  $mdToast.show(
    $mdToast.simple()
      .content('Correct!')
      .position($scope.getToastPosition())
      .hideDelay(3000)
    );
  };

  $scope.wrongToast = function() {
  $mdToast.show(
  $mdToast.simple()
    .content('Wrong :(')
    .position($scope.getToastPosition())
    .hideDelay(3000)
  );
  };

		$scope.checkCorrect = function() {
      $scope.no_name = false;
			if ('0' === $scope.choice) {
        $scope.correctToast();
				times++;
        $scope.color = "true";
        setTimeout((function () { $scope.color = null }), 300)

				$http.get('/congress/getBasicQuestion/' + address)
				.success(function (data,status,headers,config) {
					console.log(JSON.stringify(data));
					// shuffle($scope.choices);s
          $scope.question = data.question_name;
					$scope.choices = data.choice_list.slice(0,5);
          var pics = _.map(data.options, (function (item) {
            var output = {};
            output.name = item.first_name + ' ' + item.last_name;
            output.image = item.image;
            return output;
          })).slice(0,5);
          if (data.question_name === 'Which congressman is this?') {
            pics = pics.slice(0,1);
            $scope.no_name = true;
          }
          $scope.pics = pics;

					$scope.other_choices = $scope.choices.slice(0);

					shuffle($scope.choices);
				})
				.error(function (data,status,headers,config) {
					console.log("ERROR");
					console.log(JSON.stringify(data));
				});


			} else {
          $scope.wrongToast();
			}
		}
	}
]);
