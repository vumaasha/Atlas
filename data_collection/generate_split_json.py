import glob
import json
import os
import random
import argparse

def get_product_data_with_split(source_folder,categories, train_split_val=0.70, val_split_val=0.20):
    full_product_data_list = []
    temp = source_folder.split('/atlas_dataset')[0]
    for category in categories:
        # Get list of images in source folder
        images_list = glob.glob(source_folder + category + '/images/*.jp*', recursive=True)
        with open(source_folder + category + '/data.json', 'r') as f:
            json_data = json.load(f)

        cleaned_json_data = []
        for product_data in json_data:
            product_data['file_path'] = product_data['file_path']
            actual_data = {'filename': product_data['file_path'], 'title': product_data['product_title'],
                           'sentences': [{'tokens': product_data['taxonomy'].split('/')}]}
            cleaned_json_data.append(actual_data)

        for i in cleaned_json_data:
            i['filename'] = temp+'/'+i['filename']

        # Get product data for the images
        product_data = list(filter(lambda x: x['filename'] in images_list, cleaned_json_data))
        print('Total number of products in {}: {}'.format(category, len(product_data)))

        # shuffle the list
        random.shuffle(product_data)

        # split into train,test and val
        train_set1 = product_data[:int(len(product_data) * train_split_val)]
        test_set = product_data[int(len(train_set1)) + 1:]
        val_set = train_set1[: int(len(test_set) * val_split_val)]
        train_set = train_set1[len(val_set) + 1:]
        for product in train_set:
            product['split'] = 'train'
            full_product_data_list.append(product)
        for product in test_set:
            product['split'] = 'test'
            full_product_data_list.append(product)
        for product in val_set:
            product['split'] = 'val'
            full_product_data_list.append(product)
    return full_product_data_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script which splits the data into Train, Validate and Test to train the product_categorization model')
    parser.add_argument('--dataset_path', '-dp', help='Path to atlas_dataset')

    args = parser.parse_args()
    source_folder = args.dataset_path
    json_source_folder = source_folder.split('atlas_dataset')[0]

    # get categories/labels list
    categories = os.listdir(source_folder)
    print('{} Categories have been found: {}'.format(len(categories), categories))

    # get full product data along with split
    product_data_with_split = get_product_data_with_split(source_folder,categories)
    print('Total number of samples:{}'.format(len(product_data_with_split)))

    # save it as a json file
    json_file_name = 'atlas_dataset'
    with open(json_source_folder+json_file_name+'.json', 'w') as outfile:
        json.dump({'images': product_data_with_split}, outfile)
