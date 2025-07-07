from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)


GOOGLE_BOOKS_API_KEY = "Your_Api_key"
API_BASE_URL = "http://127.0.0.1:5000/books"  

def fetch_book_data_from_api(query):
    """
    Fetches book data from the Book Information API.

    Args:
        query (str): The search query.

    Returns:
        list: A list of book dictionaries, or an error message.
    """
    try:
        api_url = f"{API_BASE_URL}?query={query}"
        response = requests.get(api_url)
        response.raise_for_status()  
        return response.json()  

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return {"error": "Failed to connect to the API."}
    except (ValueError, KeyError) as e:
        print(f"API Response Parsing Error: {e}")
        return {"error": "Error parsing API response."}



@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page with the search form and results.
    """
    books = None
    error = None

    if request.method == 'POST':
        query = request.form.get('query')  # Get search query from the form

        if query:
            results = fetch_book_data_from_api(query)

            if isinstance(results, list):  # Check if results is a list (success)
                books = results
            else:
                error = results.get("error", "An error occurred.") # extract error message if there is one.

        else:
            error = "Please enter a search query."

    return render_template('index.html', books=books, error=error)


if __name__ == '__main__':
    if not GOOGLE_BOOKS_API_KEY:
        print("Error: GOOGLE_BOOKS_API_KEY environment variable not set.")
    else:
        app.run(debug=True, port=5001) 