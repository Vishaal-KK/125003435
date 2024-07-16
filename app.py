from flask import Flask, jsonify
import requests
import time
from threading import Lock

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
THIRD_PARTY_API_URLS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMTM3NTM2LCJpYXQiOjE3MjExMzcyMzYsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjAzNmE4ZjQ4LTY5YzMtNGUyZS1iNTM3LWVkNGJhMmQ4MDAzZiIsInN1YiI6IjEyNTAwMzQzNUBzYXN0cmEuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoiZ29tYXJ0IiwiY2xpZW50SUQiOiIwMzZhOGY0OC02OWMzLTRlMmUtYjUzNy1lZDRiYTJkODAwM2YiLCJjbGllbnRTZWNyZXQiOiJSaWJzUlNmUVp5TFZGUGNOIiwib3duZXJOYW1lIjoiVmlzaGFsLktLIiwib3duZXJFbWFpbCI6IjEyNTAwMzQzNUBzYXN0cmEuZWR1LmluIiwicm9sbE5vIjoiMTI1MDAzNDM1In0.fF3s_co0Ru3waNMQQyG3FBKa4asdRh6cP4V5rNHYIIg"

# Data store
window = []
lock = Lock()

def fetch_numbers(number_type):
    url = THIRD_PARTY_API_URLS.get(number_type)
    if not url:
        print(f"Invalid number type: {number_type}")
        return []
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=0.5)
        elapsed_time = time.time() - start_time
        
        print(f"Fetched from {url}: {response.status_code} in {elapsed_time:.2f} seconds")
        
        if response.status_code == 200 and elapsed_time < 0.5:
            data = response.json()
            print(f"Response JSON: {data}")
            return data.get("numbers", [])
        else:
            print(f"Response failed or took too long: {response.status_code} in {elapsed_time:.2f} seconds")
    except (requests.Timeout, requests.RequestException) as e:
        print(f"Error fetching numbers from {url}: {e}")
    
    return []


def update_window(new_numbers):
    global window
    with lock:
        for number in new_numbers:
            if number not in window:
                if len(window) >= WINDOW_SIZE:
                    window.pop(0)
                window.append(number)

def calculate_average():
    if not window:
        return 0.0
    return sum(window) / len(window)

@app.route('/numbers/<number_type>', methods=['GET'])
def get_numbers(number_type):
    if number_type not in THIRD_PARTY_API_URLS:
        return jsonify({"error": "Invalid number type"}), 400
    
    # Fetch numbers from the third-party server
    new_numbers = fetch_numbers(number_type)
    print(f"New Numbers: {new_numbers}")
    
    # Get the previous state of the window
    with lock:
        window_prev_state = list(window)
    
    # Update the window with new numbers
    update_window(new_numbers)
    
    # Get the current state of the window
    with lock:
        window_curr_state = list(window)
    
    # Calculate the average
    avg = calculate_average()
    
    # Prepare the response
    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
    
    print(f"Response: {response}")
    
    return jsonify(response)

if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=9876)
