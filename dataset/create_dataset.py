import argparse
import urllib.request
import json
import os
cwd = os.getcwd()


def create_atlas_dataset():
    pass


def create_zvsn_dataset():
    if not os.path.exists("Normal_vs_Zoomed/Normal"):
        os.makedirs("normal")
    if not os.path.exists("Normal_vs_Zoomed/Zoomed"):
        os.makedirs("zoomed")

    # load list of images from JSON
    with open('zvsn_data.json') as data_file:
        images_data = json.load(data_file)

    # download image from URL and save it in corresponding folders
    for img in images_data:
        location = cwd + "/Normal_vs_Zoomed/" +img['label']+ "/" + img['filename']
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
