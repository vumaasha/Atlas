# Product Categorization Model

A constrained beam search and attention based sequence model for predicting the category path of a product using PyTorch.

This is the source code of the model explained in our paper "Constrained Beam Search Based Sequence model for product category classification" runnable on GPU and CPU. You can clone and run this project in your CPU/GPU to reproduce the results reported in the paper.

Table of Contents
- [Quickstart](#quickstart)
- [Model Overview](#model-overview)
  - [Sequence Model - Encoder and Decoder](#)
    - [Encoder](#encoder)
    - [Decoder](#decoder)
  - [Attention](#attention)
  - [Constrained Beam Search](#constrained-beam-search)
- [Sample Predictions](#sample-predictions)

## Quickstart
Follow the steps in this section to train the model and get predictions

**Step 1: ** Setting up 

Clone this repository to your local machine

Create a virtual environment named `atlas` and install all the project's dependencies listed in `requirements.txt`

**Step 2: ** Preparing the dataset

We will be using our **_Atlas_** dataset to train our model. Make sure you have the dataset or refer this [section](https://github.com/vumaasha/Atlas/tree/master/dataset#atlas-dataset) to get the dataset.

Once you have our Atlas dataset, open `create_input_files.py` and provide the values for the following parameters:
- `karpathy_json_path` - path of the JSON file `atlas_dataset.json` which has the data along with the splits downloaded from the Google Drive 
- `image_folder` - path of the folder containing the images 
- `output_folder` - path of the folder where you want to store the outputs produced by this script

Run the script
```
python create_input_files.py
```

This creates the following files:
- An HDF5 file containing images for each split in an I, 3, 256, 256 tensor, where I is the number of images in the split. Pixel values are still in the range [0, 255], and are stored as unsigned 8-bit Ints.
- A JSON file which contains the word_map, the word-to-index dictionary


**Step 3: ** Training the Model


**Step 4: ** Getting Predictions and Metrics of the model

## Model Overview

## Sequence Model - Encoder and Decoder

### Encoder

### Decoder

## Attention

## Constrained Beam Search

## Sample Predictions
