from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import time

load_dotenv()

app = Flask(__name__)
client = OpenAI()

@app.route('/')
def index():
    """
    This route renders the main HTML form.  Place OCR.html in a folder named "templates".
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
    # print("image:", base64_image)

    input_messages = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "OCR it."},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ]

    try:
        st = time.time()
        response = client.responses.create(model="gpt-4o-mini", input=input_messages)
        # print(response.output_text)
        en = time.time()

        return jsonify({
            "response": response.output_text,
            "generation_time": en - st
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)