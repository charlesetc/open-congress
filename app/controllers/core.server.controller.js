'use strict';
var congress = require('../../python_congress_finder/node-congress.js');

/**
 * Module dependencies.
 */
exports.index = function(req, res) {
	res.render('index', {
		user: req.user || null,
		request: req
	});
};


exports.official_profile = function(req, res) {
	var id = req.params.id;
	congress.finder('getRepByID', id, function (result) {
		console.log(JSON.stringify(result));
		var official = result.results[0];
		var color;
		if (official.party === 'R') {
			color = 'red';
		} else if (official.party === 'D') {
			color = 'blue';
		} else {
			color = 'gray';
		}
		res.render('official_profile', {
			user: req.user || null,
			official: official,
			color: color,
			request: req,
			id: id
		});
	});
};


exports.donate = function (req, res) {
	res.render('donate', {
		user: req.user || null,
		request: req
	});
};

// exports.official_profile = function(req, res) {
//
// 	var id = req.params.id;
// 	congress.finder("getRepByID", req.params.id, function (result) {
// 		var official = result.results[0];
// 		res.render('official_profile', {
// 			user: req.user || null,
// 			official_name: official.first_name + " " + official.last_name,
// 			request: req
// 		});
// 	}
// )};
