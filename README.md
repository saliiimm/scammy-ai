
# Scammy AI

The AI part of a scammer detector project using python,scraperAPI and Vader




## Related

Here are the two other parts of the project

[Scammy front with nextjs](https://github.com/saliiimm/scammy-front)

[Scammy back with nestjs](https://github.com/saliiimm/scammy-back)


## Features

- scraping data of amazon products
- get stats about it
- sentiment analysis of the product reviews


## Installation

In order to test this project in your computer you have to install python,Flask,nltk and load_dotenv

[Link to install python](https://www.python.org/downloads/)

```bash
 pip install Flask nltk load_dotenv
```
    


## Environment Variables

To run this project, you will need to you have to go to the scraperAPI website to generate a key [Click here](https://www.scraperapi.com/) then add it to your .env file

`SCRAPE_API_KEY`


## Run Locally

Clone the project

```bash
  git clone https://github.com/saliiimm/scammy-ai
```

Go to the project directory

```bash
  cd my-project
```

Start the server

```bash
  flask --app app --debug run
```


## API Reference

#### Analyze a Product

```http
  POST /analyze
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `product_name` | `string` | **Required**. The product you want to analyze  |




## Documentation

### scraping.py

#### fetch_scraperapi_url(url)
Fetches data from a given URL using ScraperAPI, handling API key authentication and returning the parsed JSON response. Returns None if the request fails.

#### search_amazon(product_name)
Searches Amazon for a given product name, constructs a search URL, and retrieves up to 5 product links using ScraperAPI. Returns a list of product URLs.

#### get_product_reviews(product_url)
Scrapes reviews, ratings, average stars, and images for a product from its Amazon URL using ScraperAPI. Returns a dictionary with reviews, ratings count, average stars, and images.

### sentiment_analysis.py

#### getStats(reviews_data)
Analyzes product reviews to compute statistics like total reviews, average rating, most common words, and top positive/negative words. Returns a dictionary with these stats.

#### isProductAScam(product_name)
Evaluates if a product is a scam by scraping Amazon reviews, analyzing sentiment with VADER, and calculating a compound score. Returns a result ("pretty good product", "WHAT A BIG SCAM", or "nothing special about it"), stats, and images.

### app.py

#### analyze_sentiment(product_name)
Calls isProductAScam from sentiment_analysis.py to analyze the sentiment of a product. Returns a dictionary with the scam result, stats, and images.

#### sentiment_api()
Flask API endpoint that accepts a POST request with a product name, validates the input, and returns the sentiment analysis result as JSON. Returns an error if the product name is missing.

## Authors

- [@saliiimm](https://github.com/saliiimm)



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)   


[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)  

[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

