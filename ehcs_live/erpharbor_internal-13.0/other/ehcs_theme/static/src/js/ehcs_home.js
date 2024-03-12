odoo.define('ehcs_theme.ehcs_home', function (require) {
	"use strict";
	
	var ajax = require('web.ajax');

	(function () {
		var words = [
			'Odoo',
			'ERP Next',
			'Python',
			'Android',
			'IOS',
			'Flectra',
			], i = 0;
		setInterval(function () {
			$('#changingword').fadeOut(function () {
				$(this).html(words[i = (i + 1) % words.length]).fadeIn();
			});
		}, 3000);
	})();
	
});