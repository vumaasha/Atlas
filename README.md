# ATLAS - Constrained Beam Search Based Sequence model for product category classification

This project aims to predict the taxonomy of an image through Attention Sequence model. 

## Architecture Blueprint
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/blueprint.png "Architecture")

## How do I use this Project?
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/Path.png "Path")

There are 2 ways you can use this Project:

1. Path 1
    1. [Use ATLAS Dataset](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
    
    We have built our own dataset of apparel images from 13 e-commerce websites. You can use our dataset either to train on this Attention model or for other Computer Vision Applications.
    
    2. [Run the pre-trained model](https://github.com/vumaasha/Atlas/blob/master/models/apparel_classification/README.md)

The model uses Attention Technique with Constrained Beam Search to predict taxonomy of the given apparel and obtained f-score of 0.88.


2. Path 2
    1. [Use Custom Dataset](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
    2. Run model to generate new Taxonomy
       * [Clean Dataset](https://github.com/vumaasha/Atlas/blob/master/models/normal_vs_zoomed/README.md)
       * [Run Model](https://github.com/vumaasha/Atlas/blob/master/models/apparel_classification/README.md)
      
     
