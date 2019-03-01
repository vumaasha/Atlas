# Dataset Generation

## Quick Start

- To download the apparel image dataset we used in our model, run the following command

`python create_dataset.py -m atlas` 

Json file used `coresdataset.json`

- To download the dataset of images into folders 'zoomed' and 'normal' respectfully

`python create_dataset.py -m zvsn` 

Json file used `zvsn_data.json`

*** 

## About the Dataset
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_category_samples.jpg "Sample dataset")
This dataset contains 52 categories of images of Apparel for Men and Women.

|     Count              | Men   | Women  |
|-------------------|-------|--------|
| # of categories   | 22    | 50     |
| Total # of images | 61,370 | 122,626 |

These images and their corresponding product information were crawled from 13 E-commerce websites. To know more about our data collection procedure, visit [this link](https://github.com/vumaasha/Atlas/tree/master/dataset/data_collection).

## About the Taxonomy

The taxonomy tree we have derived goes upto a maximum depth of 3 levels. While building our dataset, we developed our own taxonomy that standardizes the taxonomy of the images scraped from different e-commerce websites. The category path is crucial in predicting the taxonomy of a given image. As you can see in the image below, the taxonomy tree of our **Atlas** dataset along with the count of clean images under each category is shown below.
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_taxonomy_tree.jpg "Taxonomy")

## About the code
 
`create_dataset.py` has 2 modules:

* `create_atlas_dataset` downloads the cleaned apparel images into the dataset folder. 

In the data_collection folder, there are 13 crawlers that were written to crawl images and data associated with it from specific e-commerce clothing websites. For ease of use, we have compiled the urls of the clean images we crawled into `coresdataset19.json` file. 

Structure of the `coresdataset19.json` file:

    |-obj : json object

      |--images 
  
         |--filename : path to the file with filename

         |--title : title of the image

         |--sentences 
         
            |--tokens : taxonomy represented as tokens

         |--image_url : url of image

         |--split : train/test split



* `create_zvsn_dataset` downloads the images into 2 folders called zoomed and normal that consists of zoomed and normal images. We have included a sample csv file called `zvsn_data.json` that contains a collection of zoomed and normal images for the category *Men > Western Wear > Shirts*

Structure of the `coresdataset19.json` file:

    |-obj : json object

      |--images 
  
         |--filename : path to the file with filename

         |--image_url : url of image

         |--title : title of the image 
         
         |--label : zoomed/normal


Steps to run these can be found [here](#quick-start)

