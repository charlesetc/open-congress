'use strict';


angular.module('core').controller('SlidesController', ['$scope', '$document', '$http', 'Authentication',
	function($scope, $document, $http, Authentication) {
		$scope.authentication = Authentication;

		$scope.choice = '';

		var correct = '2';

		$scope.checkCorrect = function () {
			if (correct === $scope.choice) {
				alert("Well Done");
			}
		}
	}
]);
