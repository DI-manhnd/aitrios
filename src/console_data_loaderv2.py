"""
Copyright 2023 Sony Semiconductor Solutions Corp. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import base64
import logging
import cv2
import numpy as np

import console_access_library
from console_access_library.client import Client
from console_access_library.common.config import Config
from console_access_library.common.read_console_access_settings import ReadConsoleAccessSettings

import data_loader


class ConsoleDataLoader(data_loader.DataLoader) :
    """load data from console

    Args:
        DataLoader (class): load data interface class
    """

    def __init__(self, config):

        # Init
        self._params = {}
        self._params['device_id'] = ''
        self._params['number_of_images'] = 0
        self._params['number_of_inference_results'] = 0
        self.image_time = "20240419105253862"
        self._console_access_client = None
        self._meta_time_list = []
        self._meta_data_list = []

        # Check parameter
        if not 'setting_path' in config:
            raise ValueError('Console Access Library setting file is not found')
        if not os.path.exists(config['setting_path']):
            raise ValueError(f"cannot open {config['setting_path']}")

        # Instantiate Console Access Library Client.
        console_access_library.set_logger(logging.INFO)

        read_console_access_settings_obj = ReadConsoleAccessSettings(config['setting_path'])
        config_obj = Config(
            read_console_access_settings_obj.console_endpoint,
            read_console_access_settings_obj.portal_authorization_endpoint,
            read_console_access_settings_obj.client_id,
            read_console_access_settings_obj.client_secret,
        )
 
        self._console_access_client = Client(config_obj)

        # Get parameter from config
        self._params['device_id'] = config['device_id']
        self._params['sub_directory_name'] = config['sub_directory_name']

        if isinstance(self._params['sub_directory_name'], str) \
            and self._params['sub_directory_name']:
            # metas and images
            self._params['number_of_images'] = config['number_of_images']
            self._params['number_of_inference_results'] \
                = config['number_of_inference_results']
            print('Data contain both metaData and Image....')
        else:
            # only metas
            self._params['number_of_inference_results'] \
                = config['number_of_inference_results']
            self._params['first_timestamp'] = config['first_timestamp']
            self._params['last_timestamp'] = config['last_timestamp']
            print('Data is metaData only!')


    def _get_inference_results(self):
        # with images
        meta_data = []
        timestamp = []
        if isinstance(self._params['sub_directory_name'], str) \
            and self._params['sub_directory_name']:
            if self._params['number_of_images'] > 0:

                # self._params['first_timestamp'] = self._image_time_list[0]
                # self._params['last_timestamp'] = self._image_time_list[-1]
                self._params['number_of_inference_results'] \
                    = self._params['number_of_images']
                print('number of inference results: ', self._params['number_of_inference_results'])
                print('device Id: ', self._params['device_id'])
                print('Image name: ', self._params['sub_directory_name'])
                print('i have image')
            else:
                self._params['number_of_inference_results'] = 0
                print('i dont have image')

        inference_response = self._console_access_client.insight.get_inference_results(
                            self._params['device_id'],
                            number_of_inference_results=self._params['number_of_inference_results'],
                            raw=1,
                            )
        # print('raw data respinse', inference_response)

        # get meta data from inference results
        for inference_data in inference_response:
            # print(inference_data, '\n')
            base64_data = inference_data['inference_result']['Inferences'][0]['O']
            base64_decode = base64.b64decode(base64_data)
            time = inference_data['inference_result']['Inferences'][0]['T']
            self._meta_data_list.append(base64_decode)
            self._meta_time_list.append(time)
        meta_data = self._meta_data_list
        timestamp = self._meta_time_list
        return meta_data, timestamp

    def get_image_info(self):
        """get image info for other process

        Returns:
            dict: infomation of image
        """
        image_info = {}

        if isinstance(self._params['sub_directory_name'], str) \
            and self._params['sub_directory_name']:
            image_info['image_flg'] = True
            # image_info['image_name'] = "20240415054229435"
            image_info['image_name'] = self._params['sub_directory_name']
            image_info['device_id'] = self._params['device_id']
        else:
            image_info['image_flg'] = False
            image_info['image_name'] = None

        return image_info


