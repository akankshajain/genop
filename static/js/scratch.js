$(document).ready(function() {
    var Secret = {}
    var ConfigMap = {}
    var PersistentVolumeClaim = {}
    var Service = {}
    var Pod = {}
    var Deployment = {}
    var StatefulSet = {}
    var Job = {}
    var Cronjob = {}
    var Route = {}
    var NetworkPolicy = {}
    var resourcenames = []
    var kinds = []


    $("#full_kind").keyup(function () {
        //Reference the Button.
        var btnAddRes = $("#full_addResource");
        var btnCreateKind = $("#full_createkind");
        if ($(this).val().trim() != "") {
            btnCreateKind.removeAttr("disabled");
            btnAddRes.removeAttr("disabled");
        } else {
            btnCreateKind.attr("disabled", "disabled");
            btnAddRes.attr("disabled", "disabled");
        }
    });

    $("#full_operator_name").keyup(function () {
        //Reference the Button.
        var btnCreateOP = $("#full_createop");
        if ($(this).val().trim() != "") {
            btnCreateOP.removeAttr("disabled");
        } else {
            btnCreateOP.attr("disabled", "disabled");
        }
    });


    $('#full_createkind').click(function   (event) {
        var kindVal = $('#full_kind').val();
        var kind = "{\"name\":\"" +  kindVal + "\"," +
            "\"resourcenames\":[" + resourcenames + "]}"
        kinds.push(kind)
        resourcenames = []
        $('#full_bar').append('&nbsp;&nbsp;<button class="btn-styled" type="button">' + kindVal + '</button>');
        $('#message_div2').removeClass("alert-success alert-danger alert-info");
        $('#message_div2').hide();
    });

    $('#full_createop').click(function   (event) {
        $('#loadingmessage').show();
        var grpName = $('#full_gname').val();
        var domainName = $('#full_dname').val();
        var version = $('#full_vname').val();
        var operatorName = $('#full_operator_name').val();

        var requestBody = "{\"groupname\" : \"" + grpName +
                          "\",\"domainname\" : \"" + domainName +
                          "\",\"operatorname\" : \"" + operatorName +
                          "\",\"version\" : \"" + version +
                          "\" ,\"kinds\" : [" +  kinds + "]}";
        console.log(requestBody);
    	$.ajax({
    		type : 'POST',
    		url :  'http://9.30.199.16:5000/ansibleoperatorscratch',
    		data : requestBody,
    		headers: {
    			'Content-Type':'application/json'
    		},
    		dataType : "json",
    		success : function(data) {
    		    $('#loadingmessage').hide();
    	        renderSuccessMessage(" Operator added successfully at /root/operators/" + operatorName);
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

    });

    // display modal
    $('#full_addResource').click(function   (event) {
        var resource = $('#full_resourceType').val();
        $("#"+resource+"").modal("show");
    });

    // process add resource button and create
    $('#dep_add').click(function   (event) {
        Deployment = JSON.stringify({
            type: "Deployment",
            name : $('#dname').val(),
            port : parseFloat($('#port').val()),
            image : $('#image').val(),
            label : $('#label').val(),
            replicas: parseFloat($('#replica').val())

        });
        $('.deployment').val("");
        resourcenames.push(Deployment);
        var kindVal = $('#full_kind').val();
        renderSuccessMessage2("Added deployment resource to kind " + kindVal + ".");
    });

    $('#service_add').click(function   (event) {
        Service = JSON.stringify({
            type: "Service",
            name : $('#sname').val(),
            sourceport : parseFloat($('#sport').val()),
            targetport : parseFloat($('#tport').val()),
            podselectorlabel : $('#slabel').val()

        });
        $('.service').val("");
        resourcenames.push(Service);
        var kindVal = $('#full_kind').val();
        renderSuccessMessage2("Added Service resource to kind " + kindVal + ".");
    });

    $('#route_add').click(function   (event) {
        Route = JSON.stringify({
            type: "Route",
            name : $('#rname').val(),
            servicename : $('#servicename').val(),
            targetport : parseFloat($('#targetport').val())
        });
        $('.route').val("");
        resourcenames.push(Route);
        var kindVal = $('#full_kind').val();
        renderSuccessMessage2("Added Route resource to kind " + kindVal + ".");
    });

    $('#Secret_Add').click(function   (event) {
        Secret = {
            name : $('#Secret_Name').val()
        }
        $('#Secret_Name').val('');
    });

    $('#ConfigMap_Add').click(function   (event) {
        ConfigMap = {
            name : $('#ConfigMap_Name').val()
        }
        $('#ConfigMap_Name').val('');
    });

    $('#PersistentVolumeClaim_Add').click(function   (event) {
        PersistentVolumeClaim = {
            name : $('#PersistentVolumeClaim_Name').val(),
            storageClassName :$('#PersistentVolumeClaim_SCName').val(),
            accessModes :$('#PersistentVolumeClaim_AModes').val(),
            storage : $('#PersistentVolumeClaim_Storage').val()
        }
        $('.pvc').val('');
        resourcenames.push(PersistentVolumeClaim);
        var kindVal = $('#full_kind').val();
        renderSuccessMessage2("Added Route resource to kind " + kindVal + ".");
    });

    $('#Pod_Add').click(function   (event) {
        Pod = {
            name : $('#Pod_Name').val(),
            memory : $('#Pod_Memory').val(),
            cpu: $('#Pod_CPU').val(),
            volumename: $('#Pod_VolName').val(),
            claimname: $('#Pod_ClaimName').val(),
            containername: $('#Pod_ConName').val(),
            image: $('#Pod_Image').val(),
            portname: $('#Pod_PortName').val(),
            portvalue: $('#Pod_PortVal').val(),
            volumemountname : $('#Pod_MountName').val(),
            mountPath: $('#Pod_MountPath').val(),
        }
        $('.pod-data').val('');
        resourcenames.push(Pod);
        var kindVal = $('#full_kind').val();
        renderSuccessMessage2("Added Route resource to kind " + kindVal + ".");
    });


});
