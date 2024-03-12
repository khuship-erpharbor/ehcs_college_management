function handle(files) {
	var result = []
	var file_name = []
	for (var i = 0; i < files.length; i++) {
		var file = files[i];

		if (file) {
			file_name.push(file.name)
			var reader = new FileReader();
			reader.onload = function (readerEvt) {
				var binaryString = readerEvt.target.result;
				result.push(btoa(binaryString))
				document.getElementById("image_src").value = result
			};
			reader.readAsBinaryString(file);
		}
	}
	document.getElementById("file_name").value = file_name
}


odoo.define('ehcs_theme.ehcs_quote', function (require) {
	"use strict";

	var ajax = require('web.ajax');

	/*---------------- Request Quote ---------------*/
	$(".req_name").change(function () {
		var req_id = []
		$(".req_name").each(function () {
			if ($(this).is(':checked')) {
				req_id.push(parseInt($(this).val()))
			}
		});
		$('.quote_form').find('.req_ids').val(req_id)
	})

	$('.quote_create').click(function (e) {
		console.log("Request Quote")

		var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
		var error = 0
		var name = $('.quote_form').find('.contact_name')
		var email = $('.quote_form').find('.email_from')
		var skype = $('.quote_form').find('.skype')
		var msg = $('.quote_form').find('.description')
		var list = $('.quote_form').find('.req_ids').val().length

		if (list != 0) {
			list = [$('.quote_form').find('.req_ids').val()]
		}
		var value = {
				'name': 'Project Quotation',
				'contact_name': name.val(),
				'phone': $('.quote_form').find('.phone').val(),
				'email_from': email.val(),
				'skype': skype.val(),
				'company_name': $('.quote_form').find('.company_name').val(),
				'company_website': $('.quote_form').find('.website').val(),
				'budjet_id': $('.quote_form').find('.budget').val(),
				'description': msg.val(),
				'requirement_ids': list,
				'fileupload': $('.quote_form').find('.file_name').val(),
				'image': $('.quote_form').find('.image_src').val(),
		}
		if ((name.val()) == '') {
			name.addClass('has_error_val');
			error++;
		} else {
			name.removeClass('has_error_val');
		}
		if ((msg.val()) == '') {
			msg.addClass('has_error_val');
			error++;
		} else {
			msg.removeClass('has_error_val');
		}
		if ((email.val()) == '') {
			email.addClass('has_error_val');
			error++;
		} else if (!filter.test(email.val())) {
			email.addClass('has_error_val');
			error++
		} else {
			email.removeClass('has_error_val');
		}
		if (error > 0) {
			console.log("error")
			swal({
				text: "Please check and try again or send your requirements at contact@erpharbor.com.",
				icon: "error",
			});
			return false;
		} else {
			console.log("success")
			e.preventDefault();
			$.blockUI({ overlayCSS: {backgroundColor: '#E5E0DF'}});
			ajax.jsonRpc("/request_quote", 'call', value).then(function (data) {
				$.unblockUI();
				$('.quote_form').trigger("reset");
				swal({
					title: "Thank you.!!",
					text: "We've received your inquiry. We will reach you soon.",
					icon: "success",
				});
			})
		}
	});
});
