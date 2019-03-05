import argparse
import urllib.request
import json
from tqdm import tqdm
import os
cwd = os.getcwd()


def create_atlas_dataset():
    obj = json.load(open('atlas_dataset.json'))
    for url in range(len(obj)):
        image_url = obj['images'][url]['image_url']
        file_path = obj['images'][url]['filename'].split('images/')[0]
        image_name = obj['images'][url]['filename'].split('images/')[1]
        script_path = os.path.dirname(os.path.realpath(__file__))
        file_path = script_path + '/'+ file_path + '/images/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        urllib.request.urlretrieve(image_url, file_path+image_name)


def create_zvsn_dataset():
    if not os.path.exists("zvsn_dataset/normal"):
        os.makedirs("zvsn_dataset/normal")
    if not os.path.exists("zvsn_dataset/zoomed"):
        os.makedirs("zvsn_dataset/zoomed")

    # load list of images from JSON
    with open(cwd+'/zvsn_data.json') as data_file:
        images_data = json.load(data_file)

    # download image from URL and save it in corresponding folders
    for img in tqdm(images_data):
        location = cwd + "/zvsn_dataset/" +img['label']+ "/" + img['filename']
        urllib.request.urlretrieve(img['image_url'], location)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script which creates images dataset for the models')

    parser.add_argument('--model', '-m', help='Name of the model - atlas or zvsn')

    args = parser.parse_args()
    if args.model == 'atlas':
        create_atlas_dataset()
    elif args.model == 'zvsn':
        create_zvsn_dataset()
    else:
        print("Please enter a valid model name")
