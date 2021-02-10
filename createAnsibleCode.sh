#!/bin/bash
#This script gets the list of k8s resource and creates ansible code in the operator
resource=$1
namespace=$2
IFS=$'\n';
rm -rf temp.yml
kubectl get "$resource" -n "$namespace" > /dev/null 2>&1
kubectl-neat get "$resource" -n "$namespace" -o yaml > temp.yaml

