from flask import Flask, request, jsonify
import sentiment_analysis 
app = Flask(__name__)

def analyze_sentiment(product_name):
    results = sentiment_analysis.isProductAScam(product_name)
    return {"scamResult": results['result'], "stats": results['stats']}

@app.route('/analyze', methods=['POST'])
def sentiment_api():
    data = request.get_json()
    product_name = data.get('product_name')
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400
    result = analyze_sentiment(product_name)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)