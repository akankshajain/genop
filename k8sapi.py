# *******************************************************
# (C) Copyright IBM Corp. 2020. All rights reserved.
# *******************************************************
"""
Kubectl bindings using K8S APIs
"""
import datetime
import os
import json
import logging
from kubernetes import client
from kubernetes import config as kube_configuration
from kubernetes.client import configuration
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


class AttrDict(dict):
    """
    A small wrapper to allow dictionary's keys to be referred as attributes

    e.g.
        pods = Kubectl().get('pods')
        print pods['items'][0].spec.volumes[0].persistentVolumeClaim.claimName

        dashmpp-head
    """

    @staticmethod
    def object_hook(obj):
        """
        Method to make json.loads return an AttrDict instead of a built-in dict.

        :param obj a dictionary
        :type dict
        :return an instance of AttrDict
        :rtype AttrDict
        """
        if isinstance(obj, dict):
            return AttrDict(obj)
        return obj

    def __init__(self, *args, **kw):
        super(AttrDict, self).__init__(*args, **kw)

    def __getattr__(self, attr):
        """
        Called when an attribute lookup has not found the attribute in the
        usual places (i.e. it is not an instance attribute nor is it found in
        the class tree for self). Raises AttributeError if the key is not found
        in the dictionary, which is a known incongruence with __setattr__
        for performance's sake.

        :returns: the value from the dictionary if defined
        :rtype: obj
        :raises: AttributeError
        """
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("{attr} not found".format(attr=attr))

    def __setattr__(self, attr, value):
        """
        Called when an attribute assignment is attempted.
        """
        if attr in self:
            self[attr] = value
        else:
            super(AttrDict, self).__setattr__(attr, value)

"""
Usage:
from k8sapi import *
k = Kubectl()
# Sample invocations
k.get("secrets", "builder-token-cjhxv")
k.get("pods")
k.get("deployment")

k = Kubectl(ns='test-operator')
k.get("deployment","test")

"""
class Kubectl(object):
    """
    A utility wrapper around kubectl

    :param config:
    :type config: path to kubernetes configuration file.
    :param ns: namespace
    :type ns: str
    """

    def __init__(self, config='~/.kube/config', ns='test-operator', exe=None):
        """
        :param config str: The kubeconfig to be used with this, defaults to [$HOME/.kube/config]
        :param ns str: The namespace to be used with this, defaults to [default]
        :param exe str: The kubectl binary to be used; defaults to kubectl found in PATH
        """
        self._ns = []
        self.namespace = ns

        kube_configuration.load_kube_config(config)
        configuration.assert_hostname = False
        self.api = client.CoreV1Api()
        self.appapi = client.AppsV1Api()


    def get(self, resource, object=None, field_selector="", label_selector=""):
        """
        kubectl wrapper to make a get on a given namespace. The way this has been designed is:
        gets can either be get all resources of a type on a namespaces or details of one particular
        resource of a type. (GET APIs)

        :param resource: Kubectl resource we are trying to read
        :type resource: string
        :param object: object name of a particular resource type
        :type object: str
        :returns: the output of the given wrapped command.
        :rtype: `dict` Raises Exception if fails.
        """
        result = None
        try:
            if resource.startswith("pod"):
                if object:
                    # Read details of a single pod
                    result = json.loads(self.api.read_namespaced_pod(object, self.namespace,
                                                                     _preload_content=False).data,
                                        object_hook=AttrDict.object_hook)
                else:
                    # Read all pods from a ns
                    result = json.loads(self.api.list_namespaced_pod(self.namespace,
                                                                     field_selector=field_selector,
                                                                     label_selector=label_selector,
                                                                     _preload_content=False).data,
                                        object_hook=AttrDict.object_hook)

            elif resource == "ns":
                    # Read details of a single namespace
                    result = json.loads(self.api.read_namespace(self.namespace,
                                                                _preload_content=False).data)
            elif resource == "pvc":
                if object:
                    # Return raw data for single pvcs of a namespace
                    result = json.loads(self.api.read_namespaced_persistent_volume_claim(self.namespace,
                                                                                         _preload_content=False).data)
                else:
                    # Return raw data for all pvcs of a namespace
                    result = json.loads(self.api.list_namespaced_persistent_volume_claim(self.namespace,
                                                                                         field_selector=field_selector,
                                                                                         label_selector=label_selector,
                                                                                         _preload_content=False).data)
            elif resource == "statefulsets":
                # List all statefulsets of a namespace
                result = json.loads(
                    self.appapi.list_namespaced_stateful_set(self.namespace, _preload_content=False).data,
                    object_hook=AttrDict.object_hook)
            elif resource == "secrets":
                if object:
                    # Read one secret from a namespace
                    result = json.loads(self.api.read_namespaced_secret(object, self.namespace,
                                                                        _preload_content=False).data,
                                        object_hook=AttrDict.object_hook)
                else:
                    # Read all secrets from a namespace
                    result = json.loads(
                        self.api.list_namespaced_secret(self.namespace, field_selector=field_selector,
                                                        label_selector=label_selector,
                                                        _preload_content=False).data,
                        object_hook=AttrDict.object_hook)
            elif resource == "configmap":
                # Return details of the provided config map
                if object:
                    config_map = json.loads(
                        self.api.read_namespaced_config_map(object, self.namespace,
                                                            _preload_content=False).data)
                    result = config_map["data"]
                else:
                    # All config maps of a namespaces
                    result = json.loads(
                        self.api.list_namespaced_config_map(self.namespace, field_selector=field_selector,
                                                            label_selector=label_selector,
                                                            _preload_content=False).data)
            elif resource == "nodes":
                # Return details of the provided node
                if object:
                    result = json.loads(self.api.read_node(object, _preload_content=False).data)

                else:
                    # List all nodes
                    result = json.loads(self.api.list_node(field_selector=field_selector,
                                                           label_selector=label_selector, _preload_content=False).data)
            elif resource == "deployment":
                if object:
                    # Read one secret from a namespace
                    result = json.loads(self.appapi.read_namespaced_deployment(object, self.namespace,
                                                                        _preload_content=False).data,
                                        object_hook=AttrDict.object_hook)
                else:
                    # Read all secrets from a namespace
                    result = json.loads(
                        self.appapi.list_namespaced_deployment(self.namespace, field_selector=field_selector,
                                                        label_selector=label_selector,
                                                        _preload_content=False).data,
                        object_hook=AttrDict.object_hook)
            else:
                raise RuntimeError("Invalid kubectl resource/wrapper not implemented")
        except ApiException as e:
            raise RuntimeError("ApiException: Exception when calling k8sapi get: %s\n" % e)
        except Exception as e:
            raise RuntimeError("Exception when calling k8sapi get: %s\n" % e)
        return result

    def create(self, resource, body=None):
        """
        Kubernetes Wrapper to create kubernetes resources.(POST APIs)
        :param resource: Kubernetes resource to create
        :rtype resource: string
        :param body: Json body for creating a resource
        :rtype body: dict
        :return: dict. Raises Exception if fails.
        """
        result = None
        try:
            if not body or not isinstance(body, dict):
                raise ValueError("Not a valid json body")

            if resource == "configmap":
                result = json.loads(self.api.create_namespaced_config_map(self.namespace, body,
                                                                          _preload_content=False).data)
            else:
                raise RuntimeError("Invalid kubectl resource/wrapper not implemented")
        except ValueError as val_ex:
            raise ValueError("Exception when calling k8sapi create: %s\n" % val_ex)
        except ApiException as e:
            raise RuntimeError("ApiException: Exception when calling k8sapi create: %s\n" % e)
        except Exception as e:
            raise RuntimeError("Exception when calling k8sapi create: %s\n" % e)
        return result

    def patch(self, resource, object=None, body=None):
        """
        Kubernetes Wrapper to patch kubernetes resources.(PATCH APIs)
        :param resource: Kubernetes resource to create
        :rtype resource: string
        :param body: Json body for creating a resource
        :rtype body: dict
        :param object: object name of a particular resource type
        :type object: str
        :return: dict. Raises Exception if fails.
        """
        result = None
        try:
            if not body or not isinstance(body, dict):
                raise ValueError("Not a valid json body")
            if not object:
                raise ValueError("Not a valid object to patch!")
            if resource == "statefulset":
                result = json.loads(self.appapi.patch_namespaced_stateful_set(object, self.namespace, body,
                                                                              _preload_content=False).data)
            else:
                raise RuntimeError("Invalid kubectl resource/wrapper not implemented")
        except ValueError as val_ex:
            raise ValueError("Exception when calling k8sapi patch: %s\n" % val_ex)
        except ApiException as e:
            raise RuntimeError("ApiException: Exception when calling k8sapi patch: %s\n" % e)
        except Exception as e:
            raise RuntimeError("Exception when calling k8sapi patch: %s\n" % e)
        return result

    """
    def delete(self, resource, object=None):
        result = None
        if not object:
            raise ApiException("Object to be deleted not specified")
        try:
            if resource == "pod":
                result = self.api.delete_namespaced_pod(object, self.namespace)
        except ApiException as e:
            raise RuntimeError("ApiException: Exception when calling k8sapi get: %s\n" % e)
        except Exception as e:
            raise RuntimeError("Exception when calling k8sapi get: %s\n" % e)
        return result
    """
    @property
    def namespace(self):
        """
        :returns: last namespace in the _ns class member.
        :rtype: str
        """
        return self._ns[-1] if self._ns else None

    @namespace.setter
    def namespace(self, namespace=None):
        """
        Sets a given namespace.

        :param namespace: namespace of a given kubernetes environment to set.
        :type namespace: str
        """
        if namespace:
            self._ns = [namespace]
        else:
            self._ns = []


    @property
    def pods(self):
        """
        Getter for all pods of namespace

        :returns: set of all pod names.
        :rtype: `set`
        """
        try:
            pods = json.loads(self.api.list_namespaced_pod(self.namespace, _preload_content=False).data)
        except ApiException as e:
            raise RuntimeError("ApiException: Exception while getting pods on the namespace: %s\n" % e)

        return {pod["metadata"]["name"] for pod in pods["items"]} if pods else set()


    def add_config_map_key(self, map_name, key, value, patch=False):
        """
        Sets/adds a config map value ( PATCH API )

        :param map_name: Name of the config map to retrieve
        :type(map_name): str
        :param key: the key to search for
        :type(key): str
        :param value: the value to set
        :type(value): str
        :param patch: True if key already exists and we are trying to patch,
                      False(Default) if adding a new key value pair
        :type(value): Boolean
        :returns: True on success; False on failure
        :rtype: boolean
        :raises ValueError: if the config_map of the given name does not exist
        """
        success = False
        try:
            try:
                config_map_dict = self.get("configmap", map_name)
            except:
                raise ValueError("Failed to read config map!")

            if key in config_map_dict:
                if not patch:
                    # Not adding config map key as it already exists
                    return False
                old_value = config_map_dict[key]
            elif key not in config_map_dict and patch:
                # if its a patch call the config map must have the key before hand
                raise KeyError("Key not defined: {0} in config map {1}".format(key, map_name))
            patch_data = {"data": {key: value}}
            self.api.patch_namespaced_config_map(map_name, self.namespace, patch_data, _preload_content=False).data
            success = True
        except ValueError:
            raise ValueError("Failed to read config map!")
        except KeyError:
            raise KeyError("Key not defined: {0} in config map {1}".format(key, map_name))
        except ApiException as e:
            raise RuntimeError("ApiException: Exception while patching config map of a namespace: %s\n" % e)
        except Exception as e:
            raise RuntimeError("Exception while patching config map of a namespace: %s\n" % e)

        if patch:
            return old_value
        return success


