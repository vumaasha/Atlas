# Product Categorization Model

A constrained beam search and attention based sequence model for predicting the category path of a product using PyTorch.

This is the source code of the model explained in our paper "Constrained Beam Search Based Sequence model for product category classification" runnable on GPU and CPU. You can clone and run this project in your CPU/GPU to reproduce the results reported in the paper.

## Table of Contents
- [Quickstart](#quickstart)
- [Model Overview](#model-overview)
  - [Sequence Model - Encoder and Decoder](#sequence-model---encoder-and-decoder)
    - [Encoder](#encoder)
    - [Decoder](#decoder)
  - [Attention](#attention)
  - [Constrained Beam Search](#constrained-beam-search)
- [Sample Predictions](#sample-predictions)

## Quickstart
Follow the steps in this section to train the model and get predictions

### Step 1: Setting up

1. Clone this repository to your local machine

2. Create a virtual environment named `atlas` and install all the project's dependencies listed in `requirements.txt`

### Step 2: Preparing the dataset

We will be using our **_Atlas_** dataset to train our model. Make sure you have the dataset or refer this [section](https://github.com/vumaasha/Atlas/tree/master/dataset#atlas-dataset) to get the dataset.

Once you have our Atlas dataset, open `create_input_files.py` and provide the values for the following parameters:
- `karpathy_json_path` - path of the JSON file `atlas_dataset.json` which has the data along with the splits downloaded from the Google Drive 
- `image_folder` - path of the folder containing the images 
- `output_folder` - path of the folder where you want to store the outputs produced by this script

Run the script from the command line
```
python create_input_files.py
```

This creates the following files:
- An **HDF5 file** containing images for each split in an `I, 3, 256, 256` tensor, where `I` is the number of images in the split.
- A **JSON file** which contains the `word_map`, the word-to-index dictionary. 
- A **JSON file** for each split with a list of `N_c * I` encoded captions, where `N_c` is the number of captions sampled per image. In our case `N_c` is `1`. These captions are in the same order as the images in the HDF5 file. Therefore, the `ith` caption will correspond to the `ith` image.
- A **JSON file** for each split with a list of `N_c * I` caption lengths. In our case `N_c` is `1`. The `ith` value is the length of the `ith` caption, which corresponds to the `ith` image.

### Step 3: Training the Model

Open `train.py` and provide the values for the data parameters
- `data_folder` - The `output_folder` path mentioned in the above step.
- `data_name`  - The base name shared by the files in output folder. For example `atlas_1_cap_per_img_5_min_word_freq`

**_Note:_** Do not modify the model and training parameters if you try to replicate our results. Instead if you would like to explore or play around with the model you can modify these parameters.

To train the model, run this file
```
python train.py
```
This trains the model and saves it as a tar file.

To resume training at a checkpoint, point to the corresponding file with the checkpoint parameter at the beginning of the code.


### Step 4: Getting Predictions and Metrics of the model

Open `generate_metrics.py` and specify the values for the parameters for `get_predictions()` and `get_metrics_from_predictions()` at the end of the file.

-`karpathy_json_path` - path of the JSON file `atlas_dataset.json` which has the data along with the splits
-`model_path` - path where the model is stored
-`word_map_path` - path of the word_map JSON file
-`predictions_file_path` - output CSV file path where you want your predictions to be saved.

Run this script,
```
python generate_metrics.py 
```

This script reads each image in the karpathy JSON, predicts its category path and stores it as a CSV file.
The records in the output CSV file looks like this:

|actual_category | file_name | predicted_category | split_value |
| --- | --- | --- | --- |
| "['Women', 'Western Wear', 'Tops&Tees']" | coresdataset19/Women_Western Wear_Tops&Tees/images/4a69fc38a31f5e168558f02967b70ff14dba580a.jpg | "['Women', 'Western Wear', 'Tops&Tees']" | train |
| "['Men', 'Western Wear', 'Trousers']" | coresdataset19/Men_Western Wear_Trousers/images/739299c941d67567d8bafbc68070a79f204ed599.jpg | "['Men', 'Western Wear', 'Trousers']" | train |


It also prints the classification report for train, validation and test splits in the console. 

### Step 5: Predict category path and Visualise Attention

Run `caption_cbs.py` to predict the category and visualize the attention. 

Command to run: 
`python caption.py -m <path_to_wordmap_file> -wm <path_to_model> -i <path_to_image>`

Example:
```
python caption_cbs.py --img='../../dataset/atlas_test/sample_1.jpg' --model='path/to/BEST_checkpoint_atlas_1_cap_per_img_5_min_word_freq.pth.tar' --word_map='path/to/WORDMAP_atlas_1_cap_per_img_5_min_word_freq.json' --beam_size=5

```
This script predicts the category path and displays an output image that shows which part of the image has been focussed by our model to predict the category level.
![](../../img/prediction_1.png)


## Model Overview


## Sequence Model - Encoder and Decoder

### Encoder

### Decoder

## Attention

## Constrained Beam Search

## Sample Predictions
