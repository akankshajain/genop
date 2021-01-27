$(document).ready(function() {
    var allkinds = [];

    var deploymentsRes = {
        "deployments": [
        "deployment.apps/zookeper",
        "deployment.apps/example",
        "deployment.apps/kafka"
        ]
    };
    var routesRes = {
        "routes": [
          "route.route.openshift.io/example",
          "route.route.openshift.io/kafka"
        ]
    };
    var servicesRes = {
        "services": [
          "service/example",
          "service/kafka"
        ]
    }


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
                    var dep = document.getElementById("deployment");
                    var selectionDeployment = dep.options[dep.selectedIndex].text;
                    var ser = document.getElementById("service");
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
                     }); //---createOpex click over----
                }
            else{
                // Open page for create an operator from scratch
                location.href = 'scratch';
            }
        }
    });
    createDropdown(deploymentsRes);
    createDropdown(routesRes);
    createDropdown(servicesRes);
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
		},
		error: function(jqXHR, textStatus, errorThrown) {
		    $('#loadingmessage').hide();
		    console.log("nooo")
		    console.log(textStatus)
		    console.log(jqXHR)
		    console.log(errorThrown)
		    renderSuccessMessage(" Operator added successfully at /root/operators/" + requestBody['operatorname']);
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


