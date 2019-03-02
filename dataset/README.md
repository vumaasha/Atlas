# Datasets

We have curated 2 datasets:

1. **Atlas** : This dataset contains 183,996 clothing images from 52 categories for Men and Women. These images along with their category paths were used to train our model for taxonomy predictiion.


2. **Zoomed vs Normal**: This dataset contains images that have been manually segregated as Zoomed and Normal. We used this dataset while cleaning our _**Atlas**_ dataset to remove noisy Zoomed images that were a poor representation of the product. The Zoomed vs Normal dataset was used in [this](https://github.com/vumaasha/Atlas/blob/master/models/zoomed_vs_normal/Zoomed_vs_Normal.ipynb) model to predict whether a given image is Zoomed or Normal.

## Table of Contents
- [Atlas](#1-atlas)
    - [Taxonomy Generation](#11-taxonomy-generation)
    - [About the Dataset](#12-about-the-dataset)
    - [Generating the Datatset](#13-generating-the-dataset)
- [Zoomed Vs Normal](#2-zoomed-vs-normal)
- [Source code- Overview](#3-source-code---overview)
  
## 1. Atlas

### 1.1 Taxonomy Generation

While we were scraping images from different e-commerce websites, we noticed that each website had its own taxonomy with varying levels of category path depth. So, to standardize the taxonomy of our image dataset, we built our own taxonomy structure. The category paths are crucial in predicting the taxonomy of a given image. As you can see in the image below, the taxonomy tree of our **Atlas** dataset along with the count of clean images under each category is shown below. The taxonomy tree we have derived goes upto a maximum depth of 3 levels. 
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_taxonomy_tree.jpg "Taxonomy")

### 1.2 About the Dataset
This dataset contains **183,996** clothing images from 52 categories for Men and Women. The images in our dataset include different views/angles of the product. A sample of the images from our dataset is given below. 
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_category_samples.jpg "Sample dataset")
These images and their corresponding product information were crawled from 13 E-commerce websites. 

|     Count              | Men   | Women  |
|-------------------|-------|--------|
| # of categories   | 22    | 30     |
| Total # of images | 61,370 | 122,626 |

To know more about our data collection procedure, visit [this link](https://github.com/vumaasha/Atlas/tree/master/dataset/data_collection).

### 1.3 Generating the Dataset
Download the `coresdataset19.json` file from [Google drive](https://drive.google.com/file/d/1MLbgQrACPvgxQTCP41FaNZr_gomTXkpu/view?usp=sharing) which contains the URLs of clothing images.

Then, run the following command to download the images from the URLs onto your local machine.

`python create_dataset.py -m atlas` 

***

## 2. Zoomed Vs Normal
To generate the dataset,

Download the `zvsn_data.json` file from [Google drive](https://drive.google.com/file/d/1MLbgQrACPvgxQTCP41FaNZr_gomTXkpu/view?usp=sharing) which contains the URLs of manually classified Zoomed & Normal images.

Then, run the following command to download the images from the URLs into their respective 'zoomed' and 'normal' folders on your local machine.

`python create_dataset.py -m zvsn` 

***
## 3. Source code - Overview
 
`create_dataset.py` has 2 functions:

`create_atlas_dataset()` downloads the cleaned clothing images into the dataset folder. 

In the data_collection folder, there are 13 crawlers that were written to crawl images and data associated with it from specific e-commerce clothing websites. When building the dataset, after downloading the images we had to [clean](https://github.com/vumaasha/Atlas/tree/master/models/zoomed_vs_normal) the dataset. Instead, we have compiled the URLs of the cleaned images we crawled into the `coresdataset19.json` file. 

Structure of the `coresdataset19.json` file:

    |-obj : json object

      |--images 
  
         |--filename : path to the file with filename

         |--title : title of the image

         |--sentences 
         
            |--tokens : taxonomy represented as tokens

         |--image_url : url of image

         |--split : train/test split

Example:

```
{'filename': 'euro-fashion-men-s-cotton-brief-pack-of-3-c9f86351-product.jpeg', 
'title': "euro fashion\n men's cotton brief (pack of  3 )", 
'sentences': [{'tokens': ['Men', 'Inner Wear', 'Underwear']}], 
'image_url': 'https://images.voonik.com/01993582/euro-fashion-men-s-cotton-brief-pack-of-3-c9f86351-product.jpg?1522053196', 'split': 'train'}
```

Steps to create **_Atlas_** dataset can be found [here](#atlas-dataset)

`create_zvsn_dataset()` downloads the images into 2 folders called zoomed and normal that consists of zoomed and normal images. We have included a sample json file called `zvsn_data.json` that contains a collection of zoomed and normal image URLs for the category *Men > Western Wear > Shirts*

Structure of the `zvsn_data.json` file:

    |-obj : json object

      |--images 
  
         |--filename : path to the file with filename

         |--image_url : url of image

         |--title : title of the image 
         
         |--label : zoomed/normal

Example:

```
{'filename': 'af9882e41bb9eb964a32815bc1f5085778a4d7e2.jpg', 
'image_url': 'http://rukmini1.flixcart.com/image/300/300/jepzrm80/shirt/2/t/v/xl-spidershirt-2-tribewear-original-imaf3bvnte6fvv5y.jpeg?q=100', 
'label': 'zoomed', 
'title': "Tribewear Men's Geometric Print Casual White Shirt"}
```

Steps to create zoomed_vs_normal dataset can be found [here](#2-zoomed-vs-normal)
