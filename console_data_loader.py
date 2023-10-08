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

import json
import os
import base64
import logging
import cv2
import numpy as np
import collections

import console_access_library
from console_access_library.client import Client
from console_access_library.common.config import Config
from console_access_library.common.read_console_access_settings import ReadConsoleAccessSettings

from common import get_deserialize_data

import data_loader


class ConsoleDataLoader(data_loader.DataLoader) :
    def __init__(self, config):

        # Init
        self._params = {}
        self._params['device_id'] = ''
        self._params['sub_directory_name'] = ''
        self.pts = np.array([[0, 169], [145, 82], [258, 159], [218, 319], [0, 319]], np.int32).reshape((-1, 1, 2))
        # self.match_image_infrence = {}
        self.array_image = ""
        self.image_time = ""
        self.cv_mat_image = np.zeros((300, 300, 3), dtype=np.uint8)
        self.deserialize_data = ""
        self.last_query_inference_time = 0
        self.last_query_image_time = 0
        self.is_writing_video = False

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
    
    def get_images(self):
        try:
            device_id = self._params['device_id']
            sub_dir = self._params['sub_directory_name']
            if device_id == "":
                return "Error"

            image_response = self._console_access_client.insight.get_images(device_id,
                                                        sub_dir,
                                                        number_of_images=1,
                                                        order_by="DESC")
            # for image in image_response['images']:
            binary_image = base64.b64decode(image_response['images'][0]["contents"])
            array_image = np.frombuffer(binary_image, dtype=np.uint8)
            # if (image_response['images'][0]['name'].replace('.jpg', '') not in self.image_dict):
            self.image_time = image_response['images'][0]['name'].replace('.jpg', '')
            self.array_image = array_image
            
            self.is_writing_video = True
            return "OK"
        except:
            return "Error"
    def get_inferences(self):
        try:
            device_id = self._params['device_id']
            if device_id == "":
                return "Error"
            if self.image_time != "":
                inference_response = self._console_access_client.insight.get_inference_results(device_id,
                    number_of_inference_results=1,
                    raw=1,
                    time=self.image_time)
                # for inference in inference_response:
                # inference_data = inference["inference_result"]['Inferences'][0]["O"]
                inference_data = inference_response[0]['inferences'][0]["O"]
                self.deserialize_data = get_deserialize_data.get_deserialize_data(inference_data)
                self.cv_mat_image = cv2.imdecode(self.array_image, flags=cv2.IMREAD_COLOR)
                # self.match_image_infrence[self.image_time] = (cv_mat_image, deserialize_data)
            #Sorted by time
            # self.match_image_infrence = collections.OrderedDict(sorted(self.match_image_infrence.items()))


            return "OK"
        except:
            return "Error"
        

    def get_image_info(self):
        """get image info for other process

        Returns:
            dict: infomation of image
        """
        image_info = {}

        if isinstance(self._params['sub_directory_name'], str) \
            and self._params['sub_directory_name']:
            image_info['image_flg'] = True
            image_info['image_name'] = self._params['sub_directory_name']
        else:
            image_info['image_flg'] = False
            image_info['image_name'] = None

        return image_info


