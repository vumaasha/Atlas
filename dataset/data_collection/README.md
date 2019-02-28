# Data Collection
This folder contains the crawlers that can be used to collet product data and images from 13 e-commerce websites. 

## About the Crawlers

For the purpose of web scraping, we have made use of 2 web scraping tools: Scrapy and Selenium.

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


## Requirements

### dataset.csv

A csv file that contains the Taxonomy of the product and the source url of the website to be crawled. 

Taxonomy: Category path to the product separated by "->"

![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_dataset_prep.jpg "sample of the csv file")

Structure of the csv file:

    |-Taxonomy : contains taxonomy structure for a product

    |-Source url name (example: Utsav, Craftsvilla etc.): for the corresponding taxonomy as row, 
    it contains the source urls of the main product page from which images have to be scraped

### Installations for crawlers



### Crawler python files

There are 3 ways you can use these,

1. Use the existing categories on same source urls

To run the any of the scrapy crawlers,

`scrapy crawler_name.py` 

Replace 'crawler_name' with name of the python file

Example:

`scrapy bollywood_kart.py`

To run the selenium crawler,

`python crawler_name.py`

Example:

`python myntra.py`


2. Expand categories on existing source url list

**Step 1:**

To add additional categories onto the existing source url list, add the taxonomy of the new category in the specified column format and the source url of the product page in the corresponding website column name.

**Step 2:**

Run the crawler as mentioned above.

3. Build a custom dataset

If you are building your own custom dataset, ensure that the resulting json file is created with the necessary information in the format mentioned [here](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md). 
