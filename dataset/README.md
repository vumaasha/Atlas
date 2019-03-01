# Dataset Generation

## ATLAS Dataset
- To download the clothing image dataset, **_ATLAS_** we used in our model, run the following command

`python create_dataset.py -m atlas` 


## Zoomed vs Normal Dataset
- To download the dataset of images into folders 'zoomed' and 'normal' respectingly

`python create_dataset.py -m zvsn` 



*** 

## About the Dataset
This dataset contains 183,996 clothing images from 52 categories for Men and Women. The images in our dataset include different views/angles of the product. A sample of the images from our dataset is given below. 
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_category_samples.jpg "Sample dataset")
These images and their corresponding product information were crawled from 13 E-commerce websites. 

|     Count              | Men   | Women  |
|-------------------|-------|--------|
| # of categories   | 22    | 30     |
| Total # of images | 61,370 | 122,626 |

To know more about our data collection procedure, visit [this link](https://github.com/vumaasha/Atlas/tree/master/dataset/data_collection).

## About the Taxonomy

While building our dataset, we developed our own taxonomy that standardizes the taxonomy of the images scraped from different e-commerce websites. The category path is crucial in predicting the taxonomy of a given image. As you can see in the image below, the taxonomy tree of our **Atlas** dataset along with the count of clean images under each category is shown below. The taxonomy tree we have derived goes upto a maximum depth of 3 levels. 
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_taxonomy_tree.jpg "Taxonomy")

## Source code for Data Generation
 
`create_dataset.py` has 2 functions:

* `create_atlas_dataset` downloads the cleaned clothing images into the dataset folder. 

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

Example:

```
{'filename': 'euro-fashion-men-s-cotton-brief-pack-of-3-c9f86351-product.jpeg', 
'title': "euro fashion\n men's cotton brief (pack of  3 )", 
'sentences': [{'tokens': ['Men', 'Inner Wear', 'Underwear']}], 
'image_url': 'https://images.voonik.com/01993582/euro-fashion-men-s-cotton-brief-pack-of-3-c9f86351-product.jpg?1522053196', 'split': 'train'}
```

To generate the _*ATLAS*_ dataset, run [this script](#atlas-dataset).

* `create_zvsn_dataset` downloads the images into 2 folders called zoomed and normal that consists of zoomed and normal images. We have included a sample csv file called `zvsn_data.csv` that contains a collection of zoomed and normal image URLs for the category *Men > Western Wear > Shirts*

Structure of the `coresdataset19.json` file:

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
To generate the _*zoomed_vs_normal*_ dataset, run [this script](#zoomed-vs-normal-dataset).

