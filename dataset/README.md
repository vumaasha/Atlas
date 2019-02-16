# Dataset Generation

In the data_collection folder, there are 13 crawlers that were written to crawl images and data associated with it from specific e-commerce clothing websites. We used these crawlers to generate the dataset for our model. However, since the structure of the HTML pages is continually changing, these crawlers may no longer work at the time of your use or may need minor changes to be made in the html tags.

Instead, we compiled the urls of he images we crawled into `_.json` file. 
Structure of the _.json file:

Use the `_script.py` to download the images into the dataset folder. 

Command to run the python script:
`python _script.py` 

