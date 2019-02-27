# ATLAS - Constrained Beam Search Based Sequence model for product category classification

## What does this project do?
* Performs automatic taxonomy prediction of Clothing images
* Provides a dataset of 183,996 clothing images from 52 categories along with image description and pre-defined taxonomy
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/archi.png "Architecture")
## What concepts are used?
### Attention Sequence modeling
Attention Netowork focuses on relevant parts of the image while generating its taxonomy sequence by sequence(word by word).
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_attention.jpg "Attention")
### Constrained Beam Search 
CBS limits the sequences chosen by the Decoder unit of the Encode-Decoder model in order to generate the most optimal sequence for the taxonomy.


## [How does it work?](https://github.com/vumaasha/Atlas/blob/master/models/apparel_classification/README.md)
You can clone our repository and run this project on your CPU/GPU and mimic the results we obtained.

## Can I modify the model?
Yes, you can re-train the model and perform the predictions on the new model by either
* [downloading and using our existing dataset](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
* [using your own custom dataset and then re-training the model](#can-i-build-my-own-custom-dataset-or-add-additional-categories-to-the-existing-dataset)

## [Can I build my own custom dataset or add additional categories to the existing dataset?](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
Yes. There are two ways you can do this:
* Expand categories by using our pre-written crawlers to collect additional images
* Use your own custom dataset by writing your own crawlers but the images would have to be modified as per the format required to run our model. After collecting the images for the dataset, re-train the model. 
