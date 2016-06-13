$( document ).ready(function() {

    // Set selector variables
	var button = $('#input_submit');
	var input_url = $('#input_url');
	var input_status_code = $('#input_status_code');
	var selector = $('.select_status');
	
	// COMMENT THIS IF YOU CHOOSE TO BATCH UPDATE
	// When dropdown values changes, click submit button to update db
	selector.change(function () {
		input_url.attr('value', $( this ).attr( "id" ));
		input_status_code.attr('value', $( this ).val());
		button.click();
	});

});