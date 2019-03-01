# Data Collection
This folder contains the crawlers of 13 e-commerce websites that is used to collect product data and images from . 

## About the Crawlers

For the purpose of web scraping, we have used: Scrapy and Selenium.

Most of our crawlers use Scrapy except in the case of one crawler where we used Selenium to scrape data from dynamic web pages.


| Source Website           | Scrapy | Selenium |
|--------------------------|--------|----------|
| Amazon.py                | :heavy_check_mark:  |   :x:       |
| Flipkart.py              | :heavy_check_mark:  |    :x:      |
| bollywood_kart.py        | :heavy_check_mark:  |   :x:       |
| craftsvilla_crawler.py   | :heavy_check_mark:  |      :x:    |
| indian_emporium.py       | :heavy_check_mark:  |       :x:   |
| indian_cloth_store.py    | :heavy_check_mark:  |      :x:    |
| indiarush.py             | :heavy_check_mark:  |        :x:  |
| mirraw_crawler.py        | :heavy_check_mark:  |        :x:  |
| myntra.py                | :x:       | :heavy_check_mark:    |
| snapdeal_crawler.py      | :heavy_check_mark:  |    :x:      |
| utsav_fashion_crawler.py |   :heavy_check_mark:  |     :x:     |
| voonik_crawler.py        |   :heavy_check_mark:  |     :x:     |
| zipker_crawler.py        | :heavy_check_mark:  |      :x:    |

**Note:** For our data collection, we used the above crawlers. However, since the structure of the HTML pages is continually changing, these crawlers may or may no work at the time of your use. You may be requuired to alter parts of the code involving the HMTL tags.


## Collecting data using our crawlers

### Inputs to the crawlers

You will need a csv file-`dataset.csv` of the following structure:

![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_csv_strucure.jpg "sample of the csv file")

About the csv:

    Taxonomy : Contains taxonomy structure for a product

    Source url name (example: Utsav, Craftsvilla etc.): For the corresponding taxonomy as row, 
    it contains the source urls of the main product page from which images have to be scraped

Taxonomy: Category path to the product separated by "->"

The csv file contains the Taxonomy of the product and the source url of the website to be crawled. 

#### Pre-requisite packages to be installed 

Install the required packages to setup the environment for crawler

`pip install -r requirements.txt`

### To run the crawlers

Scrapy:

`scrapy crawler_name.py` 

Replace 'crawler_name' with name of the python file

Example:

`scrapy bollywood_kart.py`

Selenium:

`python crawler_name.py`

Example:

`python myntra.py`

***

## Other ways to use the crawlers

If you would like to use these images or crawlers for other applications. There are 2 ways you can use these,

1. Expand categories on existing source url list

**Step 1:**

To add additional categories onto the existing source url list, add the taxonomy of the new category in the specified column format and the source url of the product page in the corresponding website column name.

**Step 2:**

Run the crawler as mentioned [above](#to-run-the-crawlers).

2. Build a custom dataset

If you are building your own custom dataset, ensure that a json file is created with the necessary information in the format mentioned [here](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md). 


## FAQ

#### [Can I build my own custom dataset or add additional categories to the existing dataset?](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md)
Yes. There are two ways you can do this:
* Expand categories by using our pre-written crawlers to collect additional images
* Use your own custom dataset by writing your own crawlers but the images would have to be modified as per the format required to run our model. After collecting the images for the dataset, re-train the model. 

