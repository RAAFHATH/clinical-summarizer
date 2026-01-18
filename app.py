"""
Flask application for clinical note summarization.
Simple backend with 3 routes.
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from llm_handler import summarize_clinical_note
from ocr_handler import extract_text_from_image
from utils import preprocess_clinical_text

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Handle text summarization route.
    Accepts text from frontend and returns summary.
    """
    try:
        # Get text from request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text or not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"Received text for summarization (length: {len(text)})")
        
        # Preprocess text - expand abbreviations and clean
        processed_text = preprocess_clinical_text(text)
        print("Text preprocessed")
        
        # Get summary from Ollama
        summary, error = summarize_clinical_note(processed_text)
        
        if error:
            return jsonify({'error': error}), 500
        
        if not summary:
            return jsonify({'error': 'Failed to generate summary'}), 500
        
        print("Summary generated successfully")
        return jsonify({'summary': summary}), 200
        
    except Exception as e:
        # Basic error handling
        print(f"Error in summarize route: {str(e)}")
        return jsonify({'error': 'Something went wrong'}), 500


@app.route('/ocr-summarize', methods=['POST'])
def ocr_summarize():
    """
    Handle image upload, OCR, and summarization.
    Process uploaded image - extract text then summarize.
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use PNG, JPG, or JPEG'}), 400
        
        print(f"Processing uploaded file: {file.filename}")
        
        # Reset file pointer to beginning (in case it was read before)
        file.seek(0)
        
        # Extract text from image using OCR
        extracted_text, confidence = extract_text_from_image(file)
        
        if not extracted_text or not extracted_text.strip():
            return jsonify({'error': 'Could not extract text from image. Image may be unclear or contain no text.'}), 400
        
        print(f"OCR completed. Extracted text length: {len(extracted_text)}, Confidence: {confidence:.2f}")
        
        # Preprocess extracted text
        processed_text = preprocess_clinical_text(extracted_text)
        print("Extracted text preprocessed")
        
        # Get summary from Ollama
        summary, error = summarize_clinical_note(processed_text)
        
        if error:
            return jsonify({'error': error}), 500
        
        if not summary:
            return jsonify({'error': 'Failed to generate summary'}), 500
        
        print("Summary generated successfully from OCR")
        return jsonify({'summary': summary}), 200
        
    except Exception as e:
        # Basic error handling
        print(f"Error in ocr_summarize route: {str(e)}")
        return jsonify({'error': 'Something went wrong'}), 500


if __name__ == '__main__':
    print("Starting Clinical Note Summarizer...")
    print("Make sure Ollama is running: ollama serve")
    app.run(debug=True, host='localhost', port=5000)
