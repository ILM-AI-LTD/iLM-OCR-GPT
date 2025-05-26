from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Explicitly get the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Initialize OpenAI client with the API key
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    """
    This route renders the main HTML form. Place OCR.html in a folder named "templates".
    """
    return render_template('OCR.html')

@app.route("/process-image", methods=["POST"])
def process_image():
    """
    This route handles the image processing logic.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    print("Image type: ", type(image_file))
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    # Get the actual image format
    image_format = image_file.content_type or "image/jpeg"
    print(f"Image format: {image_format}")

    input_messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "OCR it."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image_format};base64,{base64_image}"
                    }
                },
            ],
        }
    ]

    try:
        st = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=input_messages
        )
        en = time.time()

        return jsonify({
            "response": response.choices[0].message.content,
            "generation_time": en - st
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)