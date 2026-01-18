"""
LLM handler for clinical note summarization using Ollama.
Uses local Llama3.2 model - no internet required.
"""

import ollama
import time


# Model to use for summarization
MODEL_NAME = 'llama3.1:8b'


def check_ollama_running():
    """
    Check if Ollama service is running.
    Simple check by trying to list models.
    """
    try:
        # Try to list models - if this works, Ollama is running
        models = ollama.list()
        return True
    except Exception as e:
        print(f"Ollama check failed: {str(e)}")
        return False


def summarize_clinical_note(text):
    """
    Summarize clinical note using Ollama Llama3.1 model.
    Returns structured summary or error message.
    """
    if not text or not text.strip():
        return None, "No text provided"
    
    # Check if Ollama is running first
    if not check_ollama_running():
        return None, "Ollama service is not running. Please start Ollama."
    
    # Create prompt for summarization
    prompt = f"""Summarize the following clinical note. Provide a structured summary with these sections:

1. Chief Complaint: Main reason for visit
2. Key Findings: Important observations and test results
3. Diagnosis: Medical diagnosis or impression
4. Treatment Plan: Medications and recommendations

IMPORTANT: Only use information present in the note. Do not add information that is not in the original note.

Clinical Note:
{text}

Summary:"""
    
    try:
        # Call Ollama API for summarization
        print("Sending request to Ollama...")
        
        # Using chat method instead of generate for better results
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        
        # Extract the generated text from response
        summary = response['message']['content']
        
        if not summary:
            return None, "Empty response from Ollama"
        
        print("Received summary from Ollama")
        return summary, None
        
    except Exception as e:
        # Basic error handling
        error_msg = str(e)
        print(f"Ollama error: {error_msg}")
        
        # Check if it's a model not found error
        if "model" in error_msg.lower() or "not found" in error_msg.lower():
            return None, f"Model {MODEL_NAME} not found. Please run: ollama pull {MODEL_NAME}"
        
        return None, f"Error generating summary: {error_msg}"