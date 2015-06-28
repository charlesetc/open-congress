'use strict';

var braintree = require('braintree');

module.exports = function(app) {
	// Root routing
	var core = require('../../app/controllers/core.server.controller');
	app.route('/').get(core.index);
	app.route('/donate').get(core.donate);
	app.route('/official/:id').get(core.official_profile);
	//app.route('/donate/').get(core.donation);


	// This is for braintree
	// var gateway = braintree.connect({
	// 	environment: braintree.Environment.Sandbox,
	// 	merchantId: 'yw9thzngsvr7qpv3',
	// 	publicKey: 't56855vng3ypjzyj',
	// 	priateKey: '374d70b0ed5262bb3c4da57f5f72c151'
	// });

	var gateway = braintree.connect({
    environment:  braintree.Environment.Sandbox,
    merchantId:   'yw9thzngsvr7qpv3',
    publicKey:    't56855vng3ypjzyj',
    privateKey:   '374d70b0ed5262bb3c4da57f5f72c151'
});

	app.route('/client_token').get(function (req, res) {
		gateway.clientToken.generate({}, function (err, response) {
			if (err !== null) {
				console.log(err);
			}
			res.send(response.clientToken);
		});
	});

	app.route('/payment-methods').post(function (req,res) {
		var nonce = req.body.payment_method_nonce;
		// am I supposed to save the nonce?

		gateway.transaction.sale({
			amount: '10.00',
			paymentMethodNonce: nonce,
		}, function (error, result) {
			if (error !== null) { // is this right?
				console.log(error);
			}

			// What to do with result?

		});
	});
};
