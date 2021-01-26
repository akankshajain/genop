// Given an ISO date time object, return just the date portion
function dateOnly(dt) {
	return moment(dt).format('YYYY-MM-DD')
}

//Render flash message on successful completion of a request
function renderSuccessMessage(message){
	$('#message_div').removeClass("alert-success alert-danger alert-info");
	$('#message_div').addClass("alert alert-success");
	$('#message_div').html("<a href=\"#\" class=\"close\" aria-label=\"close\">&times;</a><strong>Success. </strong>" + message);
	$('#message_div').show();
	$('#message_div .close').click(function() {
		$(this).parent().hide();
	});

}

//Render flash message on successful completion of a request
function renderSuccessMessage2(message){
	$('#message_div2').removeClass("alert-success alert-danger alert-info");
	$('#message_div2').addClass("alert alert-success");
	$('#message_div2').html("<a href=\"#\" class=\"close\" aria-label=\"close\">&times;</a><strong>Success. </strong>" + message);
	$('#message_div2').show();
	$('#message_div2 .close').click(function() {
		$(this).parent().hide();
	});

}

//Render flash message on unsuccessful completion of a request
function renderErrorMessage(message){
	$('#message_div').removeClass("alert-success alert-danger alert-info");
	$('#message_div').addClass("alert alert-danger");
	$('#message_div').html("<a href=\"#\" class=\"close\" aria-label=\"close\">&times;</a><strong>Error. </strong>" + message);
	$('#message_div').show();
	$('#message_div .close').click(function() {
		$(this).parent().hide();
	});
}

//Render flash message of information type
function renderInformationMessage(message){
	$('#message_div').removeClass("alert-success alert-danger alert-info");
	$('#message_div').addClass("alert alert-info");
	$('#message_div').html("<a href=\"#\" class=\"close\" aria-label=\"close\">&times;</a><strong>Info. </strong>" + message);
	$('#message_div').show();
	$('#message_div .close').click(function() {
		$(this).parent().hide();
	});
}

//Get all the API URLs required by js files
function loadUrls(callback) {
	var url = "/api/v1.0/urls";
	$.ajax({
		type: 'GET',
		dataType: "json",
		contentType: 'application/json; charset=utf-8',
		url: url,
		success: function (urls) {
			callback(urls);
		 }
	});
}

// Format currency in dollar format
function formatCurrency(amount){
	return numeral(amount).format('$0,0.00');
}

/*
 * Fade in and temporarily highlight a table row using css.  Call from the
 * DataTable 'createdRow()' callback
 */
function flashRow( row ) {
$ ( row )
	.addClass( 'highlight' )
	.fadeIn( 1000, function() {
		setTimeout(function(){
			$( this ).removeClass( 'highlight' );
		}.bind(row), 5000);
	});
}

// Replaces the url variables with actual values
function getURL(string, args){
       for (var i = 1 ; i<arguments.length ; ++i ){
		elementToBeReplaced = "[" + i.toString() + "]";
		string = string.replace(elementToBeReplaced , arguments[i]);
	}
	return string;
}


// Print console messages for developers to inspect
function displayConsoleMessages(jqXHR, textStatus, errorThrown) {
	console.log(jqXHR.status + " " + jqXHR.statusText);
	console.log(textStatus);
	console.log(errorThrown);
}

