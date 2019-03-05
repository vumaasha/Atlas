import argparse
import urllib.request
import json
from tqdm import tqdm
import os
cwd = os.getcwd()


def create_atlas_dataset(json_path):
    obj = json.load(open(json_path))
    for url in tqdm(obj['images']):
        image_url = url['image_url']
        file_path = url['filename'].split('images/')[0]
        image_name = url['filename'].split('images/')[1]
        script_path = os.path.dirname(os.path.realpath(__file__))
        file_path = script_path + '/'+ file_path + 'images/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        urllib.request.urlretrieve(image_url, file_path+image_name)


def create_zvsn_dataset(json_path):
    if not os.path.exists("zvsn_dataset/normal"):
        os.makedirs("zvsn_dataset/normal")
    if not os.path.exists("zvsn_dataset/zoomed"):
        os.makedirs("zvsn_dataset/zoomed")

    # load list of images from JSON
    with open(json_path) as data_file:
        images_data = json.load(data_file)

    # download image from URL and save it in corresponding folders
    for img in tqdm(images_data):
        location = cwd + "/zvsn_dataset/" +img['label']+ "/" + img['filename']
        urllib.request.urlretrieve(img['image_url'], location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script which creates images dataset for the models')

    parser.add_argument('--model', '-m', help='Name of the model - atlas or zvsn')

    parser.add_argument('--json_path', '-jp', help='Path to json file -  atlas_dataset.json or zvsn_dataset.json')

    args = parser.parse_args()
    if args.model == 'atlas':
        create_atlas_dataset(args.json_path)
    elif args.model == 'zvsn':
        create_zvsn_dataset(args.json_path)
    else:
        print("Please enter a valid model name")
