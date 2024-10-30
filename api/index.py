from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


def call_jwt():
    url = "https://smailpro.com/app/key"

    data = {
        'domain': 'gmail.com',
        'username': 'random',
        'server': 'server-1',
        'type': 'alias'
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://smailpro.com',
        'referer': 'https://smailpro.com/temp-gmail',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data['items']


def email_jwt(email, time):
    url = "https://smailpro.com/app/key"

    data = {
        'email': email,
        'timestamp': time  # Use the provided timestamp parameter
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'referer': 'https://smailpro.com/temp-gmail',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.text


def call_api(jwt):
    url = f"https://api.sonjj.com/email/gm/get?key={jwt}&domain=gmail.com&username=random&server=server-1&type=alias"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://smailpro.com',
        'priority': 'u=1, i',
        'referer': 'https://smailpro.com/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-rapidapi-ua': 'RapidAPI-Playground',
    }

    response = requests.get(url, headers=headers)
    return response.json()


def call_inbox(token, email, time):
    url = f"https://api.sonjj.com/email/gm/check?key={token}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081&email={email}&timestamp={time}"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://smailpro.com',
        'priority': 'u=1, i',
        'referer': 'https://smailpro.com/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-rapidapi-ua': 'RapidAPI-Playground',
    }

    response = requests.get(url, headers=headers)
    return response.json()


def read_html(key, email, message_id):
    url = f"https://api.sonjj.com/email/gm/read?key={key}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081&email={email}&message_id={message_id}"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://smailpro.com',
        'priority': 'u=1, i',
        'referer': 'https://smailpro.com/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-rapidapi-ua': 'RapidAPI-Playground',
    }

    response = requests.get(url, headers=headers)

    return response.json()


@app.route('/')
def home():
    return 'Welcome to the API system. Please refer to our documentation for API usage.'


@app.route('/api/createEmail', methods=['GET'])
def create_email():
    try:
        jwt_token = call_jwt()
        api_response = call_api(jwt_token)
        return jsonify(api_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response


@app.route('/api/checkInbox', methods=['POST'])
def check_inbox():
    try:
        data = request.get_json()
        email = data['email']
        time = data['timestamp']
        jwt_response = email_jwt(email, time)  # Fetch the JWT token response
        jwt_token = json.loads(jwt_response)['items']  # Parse the JSON response and extract the token
        api_response = call_inbox(jwt_token, email, time)  # Call the inbox API with the token
        return jsonify(api_response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response


@app.route('/api/readBody', methods=['POST'])
def read_html_route():
    try:
        data = request.get_json()
        email = data['email']
        time = data['timestamp']
        message_id = data['message_id']
        jwt_response = email_jwt(email, time)  # Fetch the JWT token response
        jwt_token = json.loads(jwt_response)['items'] 
        response = read_html(jwt_token, email, message_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error response


if __name__ == '__main__':
    app.run(debug=True)
  
