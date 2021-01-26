$(document).ready(function() {
        listOperators();
});

function listOperators(){
  var requestBody="{}";
	$.ajax({
		type : 'GET',
		url :  'http://9.30.199.16:5000/list_opers',
		data : requestBody,
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(response){
			operators = response.operators;
			var trHTML = '';
        $.each(operators, function (i, item) {
               trHTML += '<tr><td><input name=\"\" value=\"\" type=\"checkbox\"></td><td>' + item.oper_name +
                '</td><td>' + item.oper_path + '</td><td>' + item.oper_source + '</td><td>' + item.create_time +
                '</td><td><button class=\"btn btn-sm\"><span class=\"glyphicon glyphicon-edit\"></span></button>&ensp;' +
                '<button class=\"btn btn-sm\" value=\"' + item.oper_name + '\" onclick=\"download(this)\"><span class=\"glyphicon glyphicon-download-alt\"></span></button>&ensp;' +
                '<button class=\"btn btn-sm\"><span class=\"glyphicon glyphicon-cloud-upload\">' +
                '</span></button></td></tr>';
        });
               $('#opsTable').append(trHTML);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.log(textStatus)
		    console.log(jqXHR)
		    console.log(errorThrown)
			//displayConsoleMessages(jqXHR, textStatus, errorThrown);
			//renderErrorMessage("There was some error fetching devices.");
		}
	});
}

function download(objButton){
   $("#downloadModal").modal('show');
   var op_name = objButton.value;
   $('#downloadbutton').click(function (event) {
        var path = document.getElementById("dpath");
        var requestBody = "{\"operator\" : \"" + op_name +
                          "\" ,\"path\" : \"" + path.value +"\"}";
        console.log(requestBody);
	    $.ajax({
		    type : 'POST',
		    url :  'http://localhost:5000/download',
		    data : requestBody,
		    headers: {
			    'Content-Type':'application/json'
		    },
		    dataType : "json",
		    success : function(data) {
	            renderSuccessMessage(" Operator downloaded successfully at " + path);
		    },
		    error: function(jqXHR, textStatus, errorThrown) {

		        console.log("nooo")
		        console.log(textStatus)
		        console.log(jqXHR)
		        console.log(errorThrown)
		        renderSuccessMessage(" Operator added successfully at " + path);
		}
	});
   });

}