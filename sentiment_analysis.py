import re
from collections import Counter
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import scraping  

STOP_WORDS = stopwords.words('english')
POSITIVE_WORDS = {
    'great', 'good', 'excellent', 'amazing', 'awesome', 'fantastic', 'love', 'best',
    'perfect', 'happy', 'wonderful', 'superb', 'beautiful', 'fast', 'reliable'
}
NEGATIVE_WORDS = {
    'bad', 'poor', 'terrible', 'awful', 'horrible', 'worst', 'slow', 'broken',
    'disappointing', 'cheap', 'useless', 'hate', 'problem', 'issue', 'faulty'
}
def getStats(reviews_data):
    """Calculate stats for a single product's reviews using precomputed data."""
    reviews = reviews_data.get("reviews", [])
    ratings_count = reviews_data.get("ratings_count", 0)
    average_rating = reviews_data.get("stars", 0.0)
    print(f"Number of ratings in getSTats: {ratings_count}, Average stars in getSTats: {average_rating}")
    if not reviews:
        return {
            'total_reviews': ratings_count,
            'average_rating': round(average_rating, 2),
            'most_common_words': [],
            'top_positive': [],
            'top_negative': []
        }

    # Text analysis
    all_words = []
    positive_counts = Counter()
    negative_counts = Counter()

    for review in reviews:
        text = review['text'].lower()
        words = re.findall(r'\b\w+\b', text)
        all_words.extend([word for word in words if word not in STOP_WORDS])
        for word in words:
            if word in POSITIVE_WORDS:
                positive_counts[word] += 1
            if word in NEGATIVE_WORDS:
                negative_counts[word] += 1

    most_common_words = Counter(all_words).most_common(5)
    top_positive = positive_counts.most_common(3)
    top_negative = negative_counts.most_common(3)

    return {
        'total_reviews': ratings_count,  # Directly from 'ratings_count'
        'average_rating': round(average_rating, 2),  # Directly from 'stars'
        'most_common_words': most_common_words,
        'top_positive': top_positive,
        'top_negative': top_negative
    }

def isProductAScam(product_name):
    links = scraping.search_amazon(product_name)
    comments = []
    total_ratings = 0
    weighted_stars_sum = 0
    stats = None

    if not links:
        print("No products found or error occurred.")
        return {'result': 'No data available', 'stats': None}

    for i, link in enumerate(links, 1):
        print(f"\nProduct {i}: {link}")
        print("Fetching reviews...")

        reviews_data = scraping.get_product_reviews(link)
        reviews = reviews_data["reviews"]
        ratings_count = reviews_data["ratings_count"]
        stars = reviews_data["stars"]

        # Aggregate ratings
        total_ratings += ratings_count
        weighted_stars_sum += stars * ratings_count

        if reviews:
            print(f"Found {len(reviews)} reviews with {ratings_count} ratings and {stars} stars:")
            stats = getStats(reviews_data)
            print(stats)
            for j, review in enumerate(reviews, 1):
                print(f"Review {j}:")
                print(f"Rating: {review['rating']}")
                print(f"Text: {review['text']}")
                comments.append(review['text'])
                print("-" * 50)
        else:
            print("No reviews found for this product.")

    # Calculate overall stats
    overall_avg_rating = weighted_stars_sum / total_ratings if total_ratings > 0 else 0.0
    overall_stats = {
        'total_ratings_across_products': total_ratings,
        'overall_average_rating': round(overall_avg_rating, 2),
        'products_analyzed': len(links)
    }

    # Sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    list_compound = []

    for comment in comments:
        vs = analyzer.polarity_scores(comment)
        list_compound.append(vs['compound'])
        print(str(vs))

    if not list_compound:
        print("No comments to analyze.")
        return {'result': 'No comments available', 'stats': overall_stats}

    max_compound = max(list_compound)
    min_compound = min(list_compound)
    moy_compound = sum(list_compound) / len(list_compound)

    print('la moyenne du score compound est de:', moy_compound)
    print('le score compound minimum est de:', min_compound)
    print('le score compound maximum est de:', max_compound)
    print('le milieu entre max compound et min compound est de:', (max_compound + min_compound) / 2)

    if moy_compound >= 0.05:
        result = 'pretty good product'
    elif moy_compound <= -0.05:
        result = 'WHAT A BIG SCAM'
    else:
        result = 'nothing special about it'

    return {'result': result, 'stats': overall_stats}