import webview # pywebview for creating the desktop application.
import pytesseract # pytesseract for performing OCR on the image. (OCR = Optical character recognition )
from PIL import Image # Pillow for handling image files.
import base64 # Conversion
import io # Lecture
import pyperclip # To copy the text to the clip board

# Configure pytesseract to use the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path according to your tesseract installation path

def extract_text_from_image(image_data):
    # Decode the base64 image data
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    
    # Perform OCR on the image
    text = pytesseract.image_to_string(image, lang='eng+spa+fra+deu+ita+chi_sim+jpn+kor+rus')  # Add more languages as needed
    return text

def copy_to_clipboard(text):
    pyperclip.copy(text)
    return "Text copied to clipboard!"

class Api:
    def extract_text(self, image_data):
        return extract_text_from_image(image_data)
    
    def copy_text(self, text):
        return copy_to_clipboard(text)

api = Api()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>OCR App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 600px;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
        }
        #imageInput {
            margin-bottom: 20px;
        }
        button {
            background-color: #007BFF;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        pre {
            background-color: #f8f8f8;
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap;
            text-align: left;
            margin-top: 20px;
        }
        .copy-button {
            margin-top: 10px;
            background-color: #28a745;
        }
        .copy-button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Text Extractor</h1>
        <input type="file" id="imageInput" accept="image/*">
        <button onclick="extractText()">Extract Text</button>
        <h2>Extracted Text</h2>
        <pre id="result"></pre>
        <button class="copy-button" onclick="copyText()">Copy Text</button>
    </div>

    <script>
        function extractText() {
            const input = document.getElementById('imageInput');
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const imageData = e.target.result;
                    pywebview.api.extract_text(imageData).then(result => {
                        document.getElementById('result').innerText = result;
                    });
                };
                reader.readAsDataURL(input.files[0]);
            } else {
                alert('Please select an image file first.');
            }
        }

        function copyText() {
            const resultElement = document.getElementById('result');
            const text = resultElement.innerText;
            pywebview.api.copy_text(text).then(response => {
                alert(response);
            });
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    window = webview.create_window('OCR App', html=html, js_api=api)
    webview.start()
