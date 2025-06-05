from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Update the API URL to include the full path
API_URL = 'https://cloudinfra-services.ubilink.ai/f03b5d13-c6d3-435d-9278-a5929bf9ac69/bento/txt2img'

@app.route('/txt2img', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200

    try:
        # Log the incoming request
        request_data = request.get_json()
        logger.info("Received request with data: %s", request_data)
        
        # Forward the request to the actual API
        response = requests.post(
            API_URL,
            json=request_data,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
        # Log the API response
        logger.info("API response status: %s", response.status_code)
        logger.info("API response headers: %s", response.headers)
        
        # Return the response with the same status code and content
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/json')
        )
    except Exception as e:
        logger.error("Error in proxy: %s", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    logger.info("Starting proxy server on port 5000...")
    logger.info("Proxying requests to: %s", API_URL)
    app.run(port=5000, debug=True) 