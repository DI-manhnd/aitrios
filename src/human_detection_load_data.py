import os
import yaml
import argparse
from tqdm import tqdm
import json

from datetime import datetime, timedelta, timezone
import console_data_loaderv2
from ppl_decoder import decode_od_result
from smart_camera_human_schema.upload_data import UploadData


# Custom JSON Encoder to handle datetime serialization
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Define the function to process data and create JSON
def process_and_create_json(meta_data, times, image_infor):
    all_deserialize_data = []

    # Process each data and time pair
    for data, time in zip(meta_data, times):
        # Assuming UploadData and decode_od_result are defined elsewhere
        ppl_out = UploadData.GetRootAsUploadData(data, 0)
        raw_all = decode_od_result(data, image_infor['device_id'])
        all_deserialize_data.append(raw_all)

    # Convert to JSON format using CustomEncoder
    json_data = json.dumps(all_deserialize_data, indent=4, cls=CustomEncoder)

    # Write JSON data to a file
    with open('all_data.json', 'w') as json_file:
        json_file.write(json_data)

    print("JSON file has been created.")


def main():
    """main process

    """

    # Get argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, default='config/human_detect.yaml')
    args = parser.parse_args()

    # Init
    data_loader = None
    # Load config from yaml file
    if os.path.exists(args.config_path):
        with open(args.config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    else:
        raise ValueError(f'cannot open {args.config_path}')


    # Select load data method and create instance
    if config['data_source_settings']['mode'] == 'console':
        data_loader = console_data_loaderv2.ConsoleDataLoader(
            config['data_source_settings']['console_data_settings'])
    else:
        raise ValueError(
            f"{config['data_source_settings']['mode']} is not supported")

    image_infor = data_loader.get_image_info()
    # print('image information',image_infor['device_id'])
    meta_data, times = data_loader._get_inference_results()
    process_and_create_json(meta_data, times, image_infor)

if __name__ == '__main__':
    main()
