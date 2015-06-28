'use strict';

// Setting up route
angular.module('core').config(['$stateProvider', '$urlRouterProvider',
	function($stateProvider, $urlRouterProvider) {
		// Redirect to home view when route not found
		$urlRouterProvider.otherwise('/');

		// Home state routing
		$stateProvider.
		state('home', {
			url: '/',
			templateUrl: 'modules/core/views/home.client.view.html'
		})
		.state('donate', {
			url: '/donate',
			templateUrl: 'modules/core/views/donate.client.view.html'
		})
		.state('slides', {
			url: '/slides',
			templateUrl:  'modules/core/views/slides.client.view.html'
		});
	}
]);
