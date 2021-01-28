import datetime;
import subprocess;
import yaml;

def helmoperator(helmrepo, helmchart, operatorname):
    result = subprocess.run(["helm", "repo", "add", "bitnami", helmrepo], stdout=subprocess.PIPE)
    print("output %s" % result)
    operatorDirectory = "/root/operators/" + operatorname

    result = subprocess.run(["mkdir", operatorDirectory], stdout=subprocess.PIPE)
    print("output %s" % result)
    result = subprocess.run(["operator-sdk", "init", "--plugins=helm", "--helm-chart", helmchart],
                            cwd=operatorDirectory, stdout=subprocess.PIPE)
    print("output %s" % result)
    ct = datetime.datetime.now()
    date_time = ct.strftime("%m/%d/%Y %H:%M:%S")
    with open('database/operators.csv', 'a') as f:
        f.write(operatorname + ",helm," + date_time + "," + operatorDirectory + "\n")
    return


def ansibleoperatorfromk8s(groupname, domainname, operatorname, version, kinds, namespace):
    operatorDirectory = "/root/operators/" + operatorname

    result = subprocess.run(["mkdir", operatorDirectory], stdout=subprocess.PIPE)
    print("output %s" % result)
    result = subprocess.run(["operator-sdk", "init", "--plugins=ansible", "--domain", domainname],
                            cwd=operatorDirectory, stdout=subprocess.PIPE)
    print("output %s" % result)
    # print(kinds)
    # Create each kind given in "kinds" list
    for kind in kinds:
        # print(kind)
        result = subprocess.run(["operator-sdk", "create", "api", "--group", groupname, "--version", version, "--kind",
                                 kind['name'].capitalize(), "--generate-role"], cwd=operatorDirectory,
                                stdout=subprocess.PIPE)
        print("output %s" % result)
        
        path = operatorDirectory + "/roles/" + kind['name'].lower() + "/tasks/main.yml"
        maindocument = []
        for resource in kind['resourcenames']:
            print("Creating code for " + resource)
            #Execute the command to get a clean k8s resource -kubectl-neat get "$resource" -o yaml > temp.yml
            result = subprocess.run(["sh", "createAnsibleCode.sh", resource, namespace],stdout=subprocess.PIPE)
            
            with open('./temp.yaml') as file:
                document = yaml.safe_load(file)
                #Pre-fix the ansible task fields

            if "deployment" in resource:
                print("")
            elif "service" in resource:
                removed=document["spec"].pop("clusterIP")
                print("removed "+removed)
                addrbacpermissions("services", operatorDirectory)  
                
            elif "route" in resource:
                document["spec"].pop("host")
                addrbacpermissions("routes", operatorDirectory)
                
            ansibledocument={ "name": "Create "+resource,"k8s":{"definition":document}}
            #Add to main.yaml
            maindocument.append(ansibledocument)            
            
        with open(path, 'a') as f:
            yaml.safe_dump(maindocument, f, default_style=None,default_flow_style=False)
        

    ct = datetime.datetime.now()
    date_time = ct.strftime("%m/%d/%Y %H:%M:%S")
    with open('database/operators.csv', 'a') as f:
        f.write(operatorname + ",from kubernetes," + date_time + "," + operatorDirectory + "\n")
    return


def ansibleoperatorfromscratch(groupname, domainname, operatorname, version, kinds):
    operatorDirectory = "/root/operators/" + operatorname

    result = subprocess.run(["mkdir", operatorDirectory], stdout=subprocess.PIPE)
    print("output %s" % result)
    result = subprocess.run(["operator-sdk", "init", "--plugins=ansible", "--domain", domainname],
                            cwd=operatorDirectory, stdout=subprocess.PIPE)
    print("output %s" % result)

    # Create each kind given in "kinds" list
    for kind in kinds:
        print(kind)
        result = subprocess.run(["operator-sdk", "create", "api", "--group", groupname, "--version", version, "--kind",
                                 kind['name'].capitalize(), "--generate-role"], cwd=operatorDirectory,
                                stdout=subprocess.PIPE)
        print("output %s" % result)

        path = operatorDirectory + "/roles/" + kind['name'].lower() + "/tasks/main.yml"
        for resource in kind['resourcenames']:
            resourcetype = resource["type"]
            if "Deployment" == resourcetype:
                deployment(resource, path)
            elif "Service" == resourcetype:
                service(resource, path, operatorDirectory)
            elif "Route" == resourcetype:
                route(resource, path, operatorDirectory)

    ct = datetime.datetime.now()
    date_time = ct.strftime("%m/%d/%Y %H:%M:%S")
    with open('database/operators.csv', 'a') as f:
        f.write(operatorname + ",from scratch," + date_time + "," + operatorDirectory + "\n")
    return


def deployment(deploymentresource, path):
    with open('./k8s_templates/deployment_template.yaml') as file:
        document = yaml.safe_load(file)
    for item in document:
        # print(item)
        labelslist = [x.strip() for x in deploymentresource["label"].split(':')]
        print(labelslist)
        container = {"name": deploymentresource["name"], "image": deploymentresource["image"],
                     "ports": [{"containerPort": deploymentresource["port"]}]}
        item["k8s"]["definition"]["metadata"]["name"] = deploymentresource["name"]
        item["k8s"]["definition"]["spec"]["replicas"] = deploymentresource["replicas"]
        item["k8s"]["definition"]["spec"]["selector"]["matchLabels"][labelslist[0]] = labelslist[1]
        item["k8s"]["definition"]["spec"]["template"]["metadata"]["labels"][labelslist[0]] = labelslist[1]
        item["k8s"]["definition"]["spec"]["template"]["spec"]["containers"].append(container)

    with open(path, 'a') as f:
        yaml.safe_dump(document, f, default_style=None,default_flow_style=False)
    return 0


def service(serviceresource, path, operatorDirectory):
    with open('./k8s_templates/service_template.yaml') as file:
        document = yaml.safe_load(file)
    for item in document:
        appselector = [x.strip() for x in serviceresource["podselectorlabel"].split(':')]
        ports={"protocol": "TCP", "port":serviceresource["sourceport"],"targetPort":serviceresource["targetport"]}
        item["k8s"]["definition"]["metadata"]["name"] = serviceresource["name"]
        item["k8s"]["definition"]["spec"]["selector"][appselector[0]] = appselector[1]
        item["k8s"]["definition"]["spec"]["ports"].append(ports)

    with open(path, 'a') as f:
        yaml.dump(document, f)
        
    addrbacpermissions("services", operatorDirectory)
    
    return 0


def route(routeresource, path, operatorDirectory):
    ##Add the ansible code in roles/
    with open('./k8s_templates/route_template.yaml') as file:
        document = yaml.safe_load(file)

    for item in document:
        item["k8s"]["definition"]["metadata"]["name"] = routeresource["name"]
        item["k8s"]["definition"]["spec"]["to"]["name"] = routeresource["servicename"]
        item["k8s"]["definition"]["spec"]["port"]["targetPort"] = routeresource["targetport"]

    with open(path, 'a') as f:
        yaml.dump(document, f)

    addrbacpermissions("routes", operatorDirectory)
      
    return 0

def addrbacpermissions(resourcetype, operatorDirectory):

    ## Add the rbac permissions in config/rbac/
    
    with open(operatorDirectory+'/config/rbac/role.yaml') as fileroles:
        documentroles = yaml.safe_load(fileroles)
    
    found=False
    ##Check if permission already there 
    for roles in documentroles["rules"]:
        for resourcelist in roles["resources"]:
           if resourcelist == resourcetype:
               found=True
               print("Found routes in config/rbac/roles.yaml. Not adding it again.")
               break
               
    if found==False:
        print("Adding permissions for "+resourcetype)
        with open('./rbac_templates/'+resourcetype+'_rbac.yaml') as filetemplate:
            documenttemplate = yaml.safe_load(filetemplate)
        documentroles["rules"].append(documenttemplate)
        with open(operatorDirectory+'/config/rbac/role.yaml', 'w') as fileroleswrite:
            yaml.dump(documentroles, fileroleswrite)
