import json
import time
from random import shuffle
import ast
import pandas as pd
import torch
from sklearn.metrics import classification_report
from tqdm import tqdm
from collections import defaultdict
from caption_cbs import caption_image_beam_search, get_valid_categories_list
import os


def report2dict(cr):
    # Parse rows
    tmp = list()
    for row in cr.split("\n"):
        parsed_row = [x for x in row.split("  ") if len(x) > 0]
        if len(parsed_row) > 0:
            tmp.append(parsed_row)

    # Store in dictionary
    measures = tmp[0]

    D_class_data = defaultdict(dict)
    for row in tmp[1:]:
        class_label = row[0]
        for j, m in enumerate(measures):
            D_class_data[class_label][m.strip()] = float(row[j + 1].strip())
    return D_class_data


def get_predictions(karpathy_json_path, image_folder, model_path, word_map_path, beam_size, predictions_file_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    start_time = time.time()

    # Load model
    checkpoint = torch.load(model_path, map_location=device)
    decoder = checkpoint['decoder']
    decoder = decoder.to(device)
    decoder.eval()
    encoder = checkpoint['encoder']
    encoder = encoder.to(device)
    encoder.eval()

    # Load word map (word2ix)
    with open(word_map_path, 'r') as j:
        word_map = json.load(j)
    rev_word_map = {v: k for k, v in word_map.items()}  # ix2word

    # get valid sequence wordmap
    source_folder = karpathy_json_path.rsplit('/',1)[0]
    valid_wordmap_seq = get_valid_categories_list(karpathy_json_path, word_map)

    with open(karpathy_json_path, 'r') as j:
        data = json.load(j)

    actual_label_list = []
    predicted_label_list = []
    file_name_list = []
    split_value_list = []

    shuffle(data['images'])
    data['images'] = data['images'][0:50]
    for img in tqdm(data['images']):
        img_path = os.path.join(image_folder, img['filename'])
        split_value = img['split']
        # Encode, decode with attention and beam search
        seq, alphas = caption_image_beam_search(encoder, decoder, img_path, word_map, valid_wordmap_seq, beam_size)

        # get predicted labels as words
        predicted_labels = [rev_word_map[ind] for ind in seq]
        predicted_labels = [e for e in predicted_labels if e not in ['<start>', '<end>', '<unk>']]
        predicted_label_list.append(predicted_labels)

        # get actual labels from json
        actual_label = img['sentences'][0]['tokens']
        actual_label_list.append(actual_label)
        split_value_list.append(split_value)
        file_name_list.append(img['filename'])

    results_df = pd.DataFrame({'file_name': file_name_list, 'actual_category': actual_label_list, 'predicted_category': predicted_label_list,
                'split_value': split_value_list})
    results_df.to_csv(predictions_file_path)
    print("--- Execution time %s seconds ---" % (time.time() - start_time))


def get_metrics_from_predictions(predictions_file_path, output_folder):
    results = pd.read_csv(predictions_file_path)
    results['predicted_category'] = results['predicted_category'].apply(lambda x: ast.literal_eval(x))
    results['actual_category'] = results['actual_category'].apply(lambda x: ast.literal_eval(x))
    results['actual_label_string'] = results['actual_category'].apply(lambda x: ' > '.join(map(str, x)))
    results['predicted_label_string'] = results['predicted_category'].apply(lambda x: ' > '.join(map(str, x)))

    # For train set
    y_true = results[results['split_value'] == 'train']['actual_label_string']
    y_pred = results[results['split_value'] == 'train']['predicted_label_string']
    print("---Classification report for train set---")
    print(classification_report(y_true, y_pred))
    metrics_df = pd.DataFrame(report2dict(classification_report(y_true, y_pred))).T
    train_metrics_path = os.path.join(output_folder, "train_data_metrics.csv")
    metrics_df.to_csv(train_metrics_path)

    # For test set
    y_true = results[results['split_value'] == 'test']['actual_label_string']
    y_pred = results[results['split_value'] == 'test']['predicted_label_string']
    print("---Classification report for test set---")
    print(classification_report(y_true, y_pred))
    metrics_df = pd.DataFrame(report2dict(classification_report(y_true, y_pred))).T
    test_metrics_path = os.path.join(output_folder, "test_data_metrics.csv")
    metrics_df.to_csv(test_metrics_path)


if __name__ == '__main__':
    get_predictions(karpathy_json_path='../../dataset/atlas_dataset.json',
                    image_folder='../../dataset/',
                    model_path='output/BEST_checkpoint_atlas_1_cap_per_img_1_min_word_freq.pth.tar',
                    word_map_path='output/WORDMAP_atlas_1_cap_per_img_1_min_word_freq.json',
                    beam_size=5,
                    predictions_file_path='output/model_predictions_cbs.csv'
                    )
    get_metrics_from_predictions(predictions_file_path='output/model_predictions_cbs.csv',
                                 output_folder='output')
