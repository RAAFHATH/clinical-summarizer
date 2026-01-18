# Clinical Note Summarizer

A simple web application for summarizing clinical notes using local AI. This project uses Ollama with Llama3.2 for natural language processing and EasyOCR for handwritten text recognition.

## About This Project

This is a college project that demonstrates how to use local LLMs for medical text summarization. The application can process both typed and handwritten clinical notes, extracting key information and presenting it in a structured format. All processing happens locally on your machine - no cloud services or API keys required.

## Technologies Used

- **Flask** - Python web framework for backend
- **Ollama with Llama3.2** - Local LLM for text summarization
- **EasyOCR** - Pre-trained OCR model for handwriting recognition
- **HTML/CSS/JavaScript** - Frontend interface
- **Bootstrap 5** - UI styling framework

## Setup Instructions

1. **Install Ollama**
   - Download from https://ollama.ai
   - Follow installation instructions for your operating system

2. **Pull the Llama3.2 model**
   ```bash
   ollama pull llama3.2
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```
   Keep this terminal window open while using the application.

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Navigate to http://localhost:5000

## Features

- Summarize typed clinical notes
- OCR for handwritten notes (supports PNG, JPG, JPEG)
- Local AI processing (no cloud, no API keys needed)
- Privacy-friendly (all data stays on your machine)
- Structured summary format:
  - Chief Complaint
  - Key Findings
  - Diagnosis
  - Treatment Plan

## How It Works

1. **For typed notes**: User pastes text → Text is cleaned and abbreviations expanded → Ollama (Llama3.2) generates structured summary → Results displayed

2. **For handwritten notes**: User uploads image → EasyOCR extracts text → Text is processed → Ollama generates summary → Results displayed

The application uses pre-trained models only - no fine-tuning or custom training required. Processing typically takes 10-15 seconds on CPU.

## Future Improvements

- Better OCR accuracy for difficult handwriting
- Support for more LLM models (not just Llama3.2)
- Save summary history to local file
- Export summaries to PDF
- Support for multiple note formats
- Better error handling and validation

## Notes

- Make sure Ollama is running before using the application
- First run may be slower as models initialize
- OCR works best with clear, high-contrast images
- All processing happens locally - no internet connection required after setup
