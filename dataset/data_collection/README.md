

# Data Collection
This folder contains the crawlers of 13 e-commerce websites that we used to collect product images and their corresponding data for our _**Atlas**_ dataset. 

**Note:** For our data collection, we used the above crawlers. However, since the structure of the HTML pages is continually changing, these crawlers may or may no work at the time of your use. You may be requuired to alter parts of the code involving the CSS selectors.

## Table of Contents
- [About the Crawlers](#about-the-crawlers)
- [Collecting data using our crawlers](#collecting-data-using-our-crawlers)
    - [Pre-requisite packages to be installed ](#pre-requisite-packages-to-be-installed)
    - [Inputs to the crawlers](#inputs-to-the-crawlers)
    - [Working of the crawlers](#working-of-the-crawlers)
    - [To run the crawlers](#to-run-the-crawlers)
- [FAQs](#faqs)


## About the Crawlers

To perform web scraping, we used: [Scrapy](https://scrapy.org/) and [Selenium](https://www.seleniumhq.org/).

Most of our crawlers use Scrapy except in the case of one crawler where we used Selenium to scrape data from dynamic web pages.

|Source Website| Crawler Name           | Scrapy | Selenium |
|-------------|--------------------------|--------|----------|
|[Amazon](https://www.amazon.in/)| Amazon.py                | :heavy_check_mark:  |   :x:       |
|[Flipkart](https://www.flipkart.com/)| Flipkart.py              | :heavy_check_mark:  |    :x:      |
|[BollywoodKart](https://www.bollywoodkart.com/)| bollywood_kart.py        | :heavy_check_mark:  |   :x:       |
|[Craftsvilla](https://www.craftsvilla.com)| craftsvilla_crawler.py   | :heavy_check_mark:  |      :x:    |
|[India Emporium](https://indiaemporium.com)| indian_emporium.py       | :heavy_check_mark:  |       :x:   |
|[Indian Clothstore](https://www.indianclothstore.com/)| indian_cloth_store.py    | :heavy_check_mark:  |      :x:    |
|[Indiarush](https://indiarush.com/)| indiarush.py             | :heavy_check_mark:  |        :x:  |
|[Mirraw](https://www.mirraw.com/)| mirraw_crawler.py        | :heavy_check_mark:  |        :x:  |
|[Myntra](https://www.myntra.com/)| myntra.py                | :x:       | :heavy_check_mark:    |
|[Snapdeal](https://www.snapdeal.com/)| snapdeal_crawler.py      | :heavy_check_mark:  |    :x:      |
|[Utsav Fashion](https://www.utsavfashion.in/)| utsav_fashion_crawler.py |   :heavy_check_mark:  |     :x:     |
|[Voonik](https://www.voonik.com/)| voonik_crawler.py        |   :heavy_check_mark:  |     :x:     |
|[Zipker](https://www.zipker.com/)| zipker_crawler.py        | :heavy_check_mark:  |      :x:    |


## Collecting data using our crawlers

### Pre-requisite packages to be installed 

Install the required packages to setup the environment for crawler

`pip install -r requirements.txt`

### Inputs to the crawlers

The csv file is needed for the crawlers to scrape the product details from the specified URL. The csv file `crawler_dataset.csv` has the following structure:

![alt text](https://github.com/vumaasha/Atlas/blob/master/img/atlas_csv_strucure.jpg "sample of the csv file")

For example in from teh image above, 

The first column is named _Taxonomy_ and contains the category path for a product which is separated by "->". 
Example: Men-> Western Wear-> Jeans

The remaining columns are named after the crawler and the rows are filled with the product page URL for the given source.

### Working of the crawlers

Each of the crawlers follow these steps while scraping images from a URL

**Step 1:**
Parse the input csv file `crawler_datasett.csv` to obtain the source URL of website to be scraped

**Step 2:**
At each iteration, scraper visits each product page URL starting from the source URL and scrapes the following information and stores it into a dictionary

```
 'product_title' : Title of the image
 'product_price' : Price of product in the image
 'product_image_url' : Image download link
 'product_details' : Additional details about the product
 `taxonomy` : Category path of product as specified in the source csv file
```

**Step 3:**
`file_path : Contains folder path to store the file` which in this case is in the `category_path/images` directory
The images are downloaded from the `product_image_url` link into the image file path. 

**Step 4:**
The dictionary containing information about the product is written into a Json file.

**Step 5**
The scraper checks if there is Next Page in the source URL web page, if so, repeats step 2 through 5, else ends the process.


### Running the crawlers

- To run Scrapy crawlers : `scrapy crawler_name.py` 

Replace 'crawler_name' with name of the python file

Example:

`scrapy bollywood_kart.py`

- To run Selenium crawlers : `python crawler_name.py`

Example:

`python myntra.py`

***

## FAQs

#### 1. Can I build my own custom dataset? 

Yes, you can build your own custom dataset.If you are building your own custom dataset, ensure that a json file is created with the necessary information in the format mentioned [here](https://github.com/vumaasha/Atlas/blob/master/dataset/README.md). If the dataset includes zoomed images, you can clean your dataset as mentioned [here](https://github.com/vumaasha/Atlas/blob/master/models/zoomed_vs_normal/Zoomed_vs_Normal.ipynb).

#### 2. How can I add additional categories to the existing dataset?

To add additional categories onto the existing source url list, add the taxonomy of the new category in the specified column format and the source url of the product page in the corresponding website column name as shown [here](#inputs-to-the-crawlers).
Run the crawler as [mentioned](#to-run-the-crawlers).










