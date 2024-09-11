from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline

app = Flask(__name__)

# Initialize the text generation pipeline
generator = pipeline('text-generation', model='distilgpt2')

# HTML template for the GUI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Text Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        textarea, input, button {
            width: 100%;
            margin-bottom: 10px;
        }
        #result {
            white-space: pre-wrap;
            border: 1px solid #ddd;
            padding: 10px;
            min-height: 100px;
        }
    </style>
</head>
<body>
    <h1>AI Text Generator</h1>
    <textarea id="prompt" rows="3" placeholder="Enter your prompt here..."></textarea>
    <input type="number" id="max-length" value="50" min="10" max="200">
    <button onclick="generateText()">Generate Text</button>
    <h2>Generated Text:</h2>
    <div id="result"></div>

    <script>
        function generateText() {
            const prompt = document.getElementById('prompt').value;
            const maxLength = document.getElementById('max-length').value;
            const resultDiv = document.getElementById('result');

            resultDiv.textContent = 'Generating...';

            fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt, max_length: parseInt(maxLength) }),
            })
            .then(response => response.json())
            .then(data => {
                resultDiv.textContent = data.generated_text;
            })
            .catch(error => {
                resultDiv.textContent = 'Error: ' + error.message;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    prompt = data.get('prompt', '')
    max_length = data.get('max_length', 50)

    # Generate text
    generated = generator(prompt, max_length=max_length, num_return_sequences=1)
    
    return jsonify({'generated_text': generated[0]['generated_text']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
