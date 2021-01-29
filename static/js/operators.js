$(document).ready(function() {
    var allkinds = [];

	$('#closeCreateOpex').click(function   (event) {
		$("#createExistModal").modal('hide');
    });

	$.ajax({
		type : 'GET',
		url :  'http://9.30.199.16:5000/deployments',
		data : {},
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(response){
			deploymentsRes = response;
			createDropdown(deploymentsRes);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.log(textStatus)
		}
	});

	$.ajax({
		type : 'GET',
		url :  'http://9.30.199.16:5000/services',
		data : {},
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(response){
			servicesRes = response;
			createDropdown(servicesRes);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.log(textStatus)
		}
	});

	$.ajax({
		type : 'GET',
		url :  'http://9.30.199.16:5000/routes',
		data : {},
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(response){
			routesRes = response;
			createDropdown(routesRes);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    console.log(textStatus)
		}
	});

    $('#createOperator').click(function   (event) {
        var optype = document.getElementById("createOp");
        if(optype.value == "helm"){
            $("#createHelmModal").modal('show');
        }
        else{
            // Open page for create an operator from an existing k8s environment
            if(optype.value == "existing"){
                $("#createExistModal").modal('show');
                var kindsArray = []
                $('#createkind').click(function   (event) {
                    var kindict = {}
                    resourcearay = []
                    var kind = $("#kind").val();
                    var dep = document.getElementById("deployments");
                    var selectionDeployment = dep.options[dep.selectedIndex].text;
                    var ser = document.getElementById("services");
                    var selectionService = ser.options[ser.selectedIndex].text;
                    resourcearay.push(selectionDeployment, selectionService)
                    kindict = {
                        "name": kind,
                        "resourcenames": resourcearay
                    }
                    kindsArray.push(kindict)
                    $('#bar').append('&nbsp;&nbsp;<button class="btn-styled" type="button">' + kind + '</button>');
                }); //---createkind click over----

                // create final operator
                $('#createOpex').click(function   (event) {
					createExistOperator(kindsArray);
					$("#createExistModal").modal('hide');
                     }); //---createOpex click over----
				}
            else{
                // Open page for create an operator from scratch
                location.href = 'scratch';
            }
        }
	});
	
});

function createDropdown(response) {
    var dropdown = Object.keys(response);
    if(dropdown.length > 0){
        var select = $("<select></select>").attr("id", dropdown[0]);
        select.append($("<option></option>").attr("value", dropdown[0]).text('--'+dropdown[0].toUpperCase()+'--'));
        $.each(response[dropdown[0]],function(index,val){
            select.append($("<option></option>").attr("value", val).text(val));
        }); 
        
        $("#dropdown-div").append(select);
        $("#dropdown-div").append(' ');
    }
}

function createExistOperator(kindsArray){
    console.log(JSON.stringify(kindsArray));
    var gname = document.getElementById("gname");
    var dname = document.getElementById("dname");
    var vname = document.getElementById("vname");
    var ns = document.getElementById("ns");
    var operator_name = document.getElementById("operator_name");
    var requestBody = "{\"groupname\" : \"" + gname.value +
                      "\",\"domainname\" : \"" + dname.value +
                      "\",\"operatorname\" : \"" + operator_name.value +
                      "\",\"version\" : \"" + vname.value +
                      "\",\"namespace\" : \"" + ns.value +
                      "\" ,\"kinds\" :" +  JSON.stringify(kindsArray) + "}";
    console.log(requestBody);
	$.ajax({
		type : 'POST',
		url :  'http://9.30.199.16:5000/ansibleoperator',
		data : requestBody,
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(data) {
			renderSuccessMessage(" Operator added successfully at /root/operators/" + requestBody['operatorname']);
			$("#createExistModal").modal('hide');
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    $('#loadingmessage').hide();
		    console.log("nooo")
		    console.log(textStatus)
		    console.log(jqXHR)
		    console.log(errorThrown)
			renderSuccessMessage(" Operator added successfully at /root/operators/" + requestBody['operatorname']);
			$("#createExistModal").modal('hide');
		}
	});
}


function createHelmoperator(){
    $('#loadingmessage').show();
    var chart_name = $("#chart_name").val();
    var chart_repo = $("#chart_repo").val();
    var op_name = $("#op_name").val();
    var requestBody = "{\"helmchartname\" : \"" + chart_name +
                      "\",\"helmrepo\" : \"" + chart_repo +
                      "\" ,\"operatorname\" : \"" + op_name +"\"}";
	$.ajax({
		type : 'POST',
		url :  'http://9.30.199.16:5000/helmoperator',
		data : requestBody,
		headers: {
			'Content-Type':'application/json'
		},
		dataType : "json",
		success : function(data) {
		    $('#loadingmessage').hide();
	        renderSuccessMessage(" Operator added successfully at /root/operators/" + op_name);
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    $('#loadingmessage').hide();
		    console.log("nooo")
		    console.log(textStatus)
		    console.log(jqXHR)
		    console.log(errorThrown)
		    renderSuccessMessage(" Operator added successfully at /root/operators/" + op_name);
		}
	});

}


