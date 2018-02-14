#!/usr/bin/python

# *****************************************************************************
#
# Copyright (c) 2016, EPAM SYSTEMS INC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ******************************************************************************

import logging
import json
import sys
from dlab.fab import *
from dlab.meta_lib import *
from dlab.actions_lib import *
import os
from Crypto.PublicKey import RSA


if __name__ == "__main__":
    instance_class = 'notebook'
    local_log_filename = "{}_{}_{}.log".format(os.environ['conf_resource'], os.environ['edge_user_name'],
                                               os.environ['request_id'])
    local_log_filepath = "/logs/" + os.environ['conf_resource'] + "/" + local_log_filename
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG,
                        filename=local_log_filepath)

    # generating variables dictionary
    try:
        notebook_config = dict()
        notebook_config['user_name'] = os.environ['edge_user_name'].replace('_', '-')
        edge_status = AzureMeta().get_instance_status(os.environ['conf_service_base_name'],
                                                      os.environ['conf_service_base_name'] + '-' +
                                                      notebook_config['user_name'] + '-edge')
        if edge_status != 'running':
            logging.info('ERROR: Edge node is unavailable! Aborting...')
            print('ERROR: Edge node is unavailable! Aborting...')
            ssn_hostname = AzureMeta().get_private_ip_address(os.environ['conf_service_base_name'],
                                                              os.environ['conf_service_base_name'] + '-ssn')
            put_resource_status('edge', 'Unavailable', os.environ['ssn_dlab_path'], os.environ['conf_os_user'],
                                ssn_hostname)
            append_result("Edge node is unavailable")
            sys.exit(1)

        print('Generating infrastructure names and tags')
        try:
            notebook_config['exploratory_name'] = os.environ['exploratory_name'].replace('_', '-')
        except:
            notebook_config['exploratory_name'] = ''
        notebook_config['service_base_name'] = os.environ['conf_service_base_name']
        notebook_config['resource_group_name'] = os.environ['azure_resource_group_name']
        notebook_config['region'] = os.environ['azure_region']
        notebook_config['vpc_name'] = os.environ['azure_vpc_name']
        notebook_config['instance_size'] = os.environ['azure_notebook_instance_size']
        notebook_config['key_name'] = os.environ['conf_key_name']
        notebook_config['instance_name'] = '{}-{}-nb-{}'.format(notebook_config['service_base_name'],
                                                                notebook_config['user_name'],
                                                                notebook_config['exploratory_name'])
        notebook_config['tags'] = {"Name": notebook_config['instance_name'],
                                   "SBN": notebook_config['service_base_name'],
                                   "User": notebook_config['user_name'],
                                   "Exploratory": notebook_config['exploratory_name']}
        notebook_config['network_interface_name'] = notebook_config['instance_name'] + "-nif"
        notebook_config['security_group_name'] = '{}-{}-nb-sg'.format(notebook_config['service_base_name'],
                                                                      notebook_config['user_name'])
        notebook_config['private_subnet_name'] = '{}-{}-subnet'.format(notebook_config['service_base_name'],
                                                                       notebook_config['user_name'])
        ssh_key_path = '{}{}.pem'.format(os.environ['conf_key_dir'], os.environ['conf_key_name'])
        key = RSA.importKey(open(ssh_key_path, 'rb').read())
        notebook_config['public_ssh_key'] = key.publickey().exportKey("OpenSSH")
        if os.environ['application'] == 'deeplearning':
            notebook_config['primary_disk_size'] = '30'
        else:
            notebook_config['primary_disk_size'] = '12'
        if os.environ['application'] == 'deeplearning' or os.environ['application'] == 'tensor':
            notebook_config['instance_storage_account_type'] = 'Standard_LRS'
        else:
            notebook_config['instance_storage_account_type'] = 'Premium_LRS'
        if os.environ['conf_os_family'] == 'debian':
            initial_user = 'ubuntu'
            sudo_group = 'sudo'
        if os.environ['conf_os_family'] == 'redhat':
            initial_user = 'ec2-user'
            sudo_group = 'wheel'
        notebook_config['ami_type'] = 'default'
        notebook_config['expected_image_name'] = '{}-{}-notebook-image'.format(notebook_config['service_base_name'],
                                                                               os.environ['application'])
        notebook_config['notebook_image_name'] = (lambda x: x if x != 'None'
                                                else notebook_config['expected_image_name']) \
                                                (str(os.environ.get('notebook_image_name')))
        print('Searching preconfigured images')
        if notebook_config['notebook_image_name'] == 'default':
            if AzureMeta().get_image(notebook_config['resource_group_name'], notebook_config['expected_image_name']):
                print('Preconfigured image found. Using: {}'.format(notebook_config['expected_image_name']))
                notebook_config['ami_name'] = notebook_config['expected_image_name']
                notebook_config['ami_type'] = 'pre-configured'
            else:
                notebook_config['ami_name'] = os.environ['azure_' + os.environ['conf_os_family'] + '_ami_name']
        elif AzureMeta().get_image(notebook_config['resource_group_name'], notebook_config['notebook_image_name']):
            print('Preconfigured image found. Using: {}'.format(notebook_config['notebook_image_name']))
            notebook_config['ami_name'] = notebook_config['notebook_image_name']
            notebook_config['ami_type'] = 'pre-configured'
        else:
            notebook_config['ami_name'] = os.environ['azure_' + os.environ['conf_os_family'] + '_ami_name']
            print('No preconfigured image found. Using default one: {}'.format(notebook_config['ami_name']))
    except Exception as err:
        print("Failed to generate variables dictionary.")
        append_result("Failed to generate variables dictionary.", str(err))
        sys.exit(1)

    with open('/root/result.json', 'w') as f:
        data = {"notebook_name": notebook_config['instance_name'], "error": ""}
        json.dump(data, f)

    # launching instance for notebook server
    try:
        logging.info('[CREATE NOTEBOOK INSTANCE]')
        print('[CREATE NOTEBOOK INSTANCE]')
        params = "--instance_name {} --instance_size {} --region {} --vpc_name {} --network_interface_name {} --security_group_name {} --subnet_name {} --service_base_name {} --resource_group_name {} --dlab_ssh_user_name {} --public_ip_name {} --public_key '''{}''' --primary_disk_size {} --instance_type {} --user_name {} --instance_storage_account_type {} --ami_name {} --tags '{}' --ami_type {}". \
            format(notebook_config['instance_name'], notebook_config['instance_size'], notebook_config['region'],
                   notebook_config['vpc_name'], notebook_config['network_interface_name'],
                   notebook_config['security_group_name'], notebook_config['private_subnet_name'],
                   notebook_config['service_base_name'], notebook_config['resource_group_name'], initial_user,
                   'None', notebook_config['public_ssh_key'], '32', 'notebook',
                   notebook_config['user_name'], notebook_config['instance_storage_account_type'],
                   notebook_config['ami_name'], json.dumps(notebook_config['tags']), notebook_config['ami_type'])
        try:
            local("~/scripts/{}.py {}".format('common_create_instance', params))
        except:
            traceback.print_exc()
            raise Exception
    except Exception as err:
        try:
            AzureActions().remove_instance(notebook_config['resource_group_name'], notebook_config['instance_name'])
        except:
            print("The instance hasn't been created.")
        append_result("Failed to create instance.", str(err))
        sys.exit(1)