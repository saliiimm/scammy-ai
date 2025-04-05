import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('SCRAPE_API_KEY')
SCRAPERAPI_URL = "https://api.scraperapi.com"
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

def search_amazon(product_name):
    search_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}&ref=nb_sb_noss"
    data = fetch_scraperapi_url(search_url)
    if not data or "results" not in data:
        print("No products found or error occurred.")
        return []
    product_links = [item["url"] for item in data["results"] if item.get("url")]
    return product_links[:5]

def get_product_reviews(product_url):
    """Extract reviews and ratings data from an Amazon product page."""
    data = fetch_scraperapi_url(product_url)
    print(f"Data fetched: {data}")
    if not data or "reviews" not in data:
        print("No reviews found or error occurred.")
        return {"reviews": [], "ratings_count": 0, "stars": 0.0}

    reviews = [
        {
            "rating": str(review.get("stars", "No rating")),
            "text": review.get("review", "No review text")
        }
        for review in data["reviews"]
    ]
    customer_reviews = data.get("product_information", {}).get("Customer Reviews", {})
    print(f"Customer Reviews raw data: {customer_reviews}")
    num_of_ratings = customer_reviews.get("ratings_count", 0)
    avg_stars = customer_reviews.get("stars", 0.0)
    print(f"Number of ratings in getproductreviews: {num_of_ratings}, Average stars in getproductreviews: {avg_stars}")
    return {
        "reviews": reviews,
        "ratings_count": num_of_ratings,
        "stars": avg_stars
    }