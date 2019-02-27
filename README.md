# ATLAS - Constrained Beam Search Based Sequence model for product category classification

## What does this project do?
* Performs automatic taxonomy prediction of Clothing images
* Provides a dataset of 183,996 clothing images from 52 categories along with image description and pre-defined taxonomy

## What concepts are used?
We use attention based neural network Encoder-Decoder model to generate the sequences in the taxonomy. 
### Encoder-Decoder Model
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_encoder_decoder.jpg "encoder decoder")
#### Encoder
The Encoder unit is a 101 layered Residual Network(ResNet) trained on the ImageNet classification that converts the input image into a fixed size vector.

Since the input images are of variable sizes, we use CNN to produce fixed size vectors. 

The images are resized by adding a 2D adaptive average pooling layer. This enables the encoder to accept images of variable sizes. 

The final encoding produced will have the dimensions batch size x 14 x 14 x 2048.

#### Decoder
This is the part of the model that predicts sequences for the taxonomy. 

The Decoder is a combination of Long Short-Term Memory(LSTM) along with Attention Network. 

It combines combines the output from the encoder and attention weights to predict category paths as sequences for the taxonomy. 



### Attention Sequence Modeling
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_attention.jpg "Attention")

 
Attention Network focuses on relevant parts of the image while generating its taxonomy sequence by sequence(word by word).

### Constrained Beam Search 
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_cbs.jpg "Constrained Beam Search")
We also extend our model by introducing constrained beam search on top of it to restrict the model from generating category paths that are not predefined in our taxonomy. 

CBS limits the sequences chosen by the Decoder unit of the Encode-Decoder model in order to generate the most optimal sequence for the taxonomy.


## [How does it work?](https://github.com/vumaasha/Atlas/blob/master/models/apparel_classification/README.md)
![alt text](https://github.com/vumaasha/Atlas/blob/master/img/archi.png "Architecture")
You can clone our repository and run this project on your CPU/GPU and mimic the results we obtained.

## Can I modify the model?
Yes, you can re-train the model and perform the predictions on the new model by either
* [downloading and using our existing dataset](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
* [using your own custom dataset and then re-training the model](#can-i-build-my-own-custom-dataset-or-add-additional-categories-to-the-existing-dataset)

## [Can I build my own custom dataset or add additional categories to the existing dataset?](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
Yes. There are two ways you can do this:
* Expand categories by using our pre-written crawlers to collect additional images
* Use your own custom dataset by writing your own crawlers but the images would have to be modified as per the format required to run our model. After collecting the images for the dataset, re-train the model. 
