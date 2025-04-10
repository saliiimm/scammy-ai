import requests
from dotenv import load_dotenv
import os

#here we load api key of scrape api so we can scrape data froma amzon easily,i tried from scratch but takes too much time beacuse of layers of security of amazon(proxies,anti-spam,...)
load_dotenv()
API_KEY = os.getenv('SCRAPE_API_KEY')
SCRAPERAPI_URL = "https://api.scraperapi.com"
#defined a function so i give the link to scrap api and he gives me back the data of the website
def fetch_scraperapi_url(url):
    params = {
        "api_key": API_KEY,
        "url": url,
        "country_code": "us",
        "autoparse": "true"
    }
    try:
        response = requests.get(SCRAPERAPI_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

#defined a function where based on a product name i will get 5 different product links so i can scrape from them reviews,images and ratings
def search_amazon(product_name):
    search_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}&ref=nb_sb_noss"
    data = fetch_scraperapi_url(search_url)
    if not data or "results" not in data:
        print("No products found or error occurred.")
        return []
    product_links = [item["url"] for item in data["results"] if item.get("url")]
    return product_links[:5]

#the hardest part of the project:scraping the reviews and ratings
#the difficulty was that amazon is intelligent and that to avoid scraping they send data under different formats 
# but i fount the structure that is used for most of it
#you can see example of how is structured the data we fetch in the test.txt file
def get_product_reviews(product_url):
    data = fetch_scraperapi_url(product_url)
    print(f"Raw data for {product_url}: {data}")  
    if not data or "reviews" not in data:
        print("No reviews found or error occurred.")
        return {"reviews": [], "ratings_count": 0, "stars": 0.0, "images": []}

    reviews = [
        {
            "rating": str(review.get("stars", "No rating")),
            "text": review.get("review", "No review text")
        }
        for review in data["reviews"]
    ]
    #once i get the data from a url,i save its reviews,num of ratings,avg stars,and images in lists
    # so i can merge it with the 4 other links data
    customer_reviews = data.get("product_information", {}).get("Customer Reviews", {})
    num_of_ratings = customer_reviews.get("ratings_count", 0) or 0
    avg_stars = customer_reviews.get("stars", 0.0) or 0.0
    images = data.get("images", []) or []
    print(f"Reviews: {reviews}, Ratings: {num_of_ratings}, Stars: {avg_stars}, Images: {images}")
    return {
        "reviews": reviews,
        "ratings_count": num_of_ratings,
        "stars": avg_stars,
        "images": images
    }