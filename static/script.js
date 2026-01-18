// Vanilla JavaScript for clinical note summarizer
// Handles form interactions and API calls

// Handle image preview when file is selected
function handleImagePreview(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const previewContainer = document.getElementById('imagePreviewContainer');
    const previewImage = document.getElementById('imagePreview');
    const fileError = document.getElementById('fileError');
    const fileUploadArea = document.getElementById('fileUploadArea');
    
    // Hide any previous errors
    fileError.style.display = 'none';
    
    if (!file) {
        previewContainer.style.display = 'none';
        return;
    }
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
        fileError.textContent = 'Invalid file type. Please select a PNG, JPG, or JPEG image.';
        fileError.style.display = 'block';
        previewContainer.style.display = 'none';
        fileInput.value = '';
        return;
    }
    
    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        fileError.textContent = 'File size exceeds 10MB. Please select a smaller image.';
        fileError.style.display = 'block';
        previewContainer.style.display = 'none';
        fileInput.value = '';
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
        // Update upload area to show filename
        fileUploadArea.querySelector('.file-upload-text').textContent = `Selected: ${file.name}`;
    };
    reader.readAsDataURL(file);
}

// Remove image preview
function removeImagePreview() {
    const fileInput = document.getElementById('imageFile');
    const previewContainer = document.getElementById('imagePreviewContainer');
    const fileError = document.getElementById('fileError');
    const fileUploadArea = document.getElementById('fileUploadArea');
    
    fileInput.value = '';
    previewContainer.style.display = 'none';
    fileError.style.display = 'none';
    fileUploadArea.querySelector('.file-upload-text').textContent = 'Click to upload or drag and drop';
}

// Summarize text from textarea
async function summarizeText() {
    const text = document.getElementById('clinicalText').value.trim();
    
    if (!text) {
        alert('Please enter some text to summarize');
        return;
    }
    
    // Show loading message
    document.getElementById('loadingMessage').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    console.log('Sending text for summarization...');
    
    try {
        // Send POST request to /summarize endpoint
        const response = await fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        // Hide loading message
        document.getElementById('loadingMessage').style.display = 'none';
        
        if (!response.ok) {
            // Handle error
            alert('Error: ' + (data.error || 'Something went wrong'));
            console.error('Error response:', data);
            return;
        }
        
        // Display summary
        if (data.summary) {
            document.getElementById('summaryOutput').textContent = data.summary;
            document.getElementById('resultsSection').style.display = 'block';
            // Scroll to results
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            console.log('Summary received successfully');
        } else {
            alert('No summary received');
        }
        
    } catch (error) {
        // Basic error handling
        document.getElementById('loadingMessage').style.display = 'none';
        alert('Error: ' + error.message);
        console.error('Fetch error:', error);
    }
}

// Summarize image (OCR + summarization)
async function summarizeImage() {
    const fileInput = document.getElementById('imageFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select an image file');
        return;
    }
    
    // Check file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    const fileError = document.getElementById('fileError');
    
    if (!allowedTypes.includes(file.type)) {
        fileError.textContent = 'Invalid file type. Please select a PNG, JPG, or JPEG image.';
        fileError.style.display = 'block';
        return;
    }
    
    // Check file size
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        fileError.textContent = 'File size exceeds 10MB. Please select a smaller image.';
        fileError.style.display = 'block';
        return;
    }
    
    // Hide error if validation passes
    fileError.style.display = 'none';
    
    // Show loading message
    document.getElementById('loadingMessage').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    
    console.log('Processing image file:', file.name);
    
    try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Send POST request to /ocr-summarize endpoint
        const response = await fetch('/ocr-summarize', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Hide loading message
        document.getElementById('loadingMessage').style.display = 'none';
        
        if (!response.ok) {
            // Handle error - show in error div if on image tab
            const fileError = document.getElementById('fileError');
            if (fileError) {
                fileError.textContent = 'Error: ' + (data.error || 'Something went wrong');
                fileError.style.display = 'block';
            } else {
                alert('Error: ' + (data.error || 'Something went wrong'));
            }
            console.error('Error response:', data);
            return;
        }
        
        // Display summary
        if (data.summary) {
            document.getElementById('summaryOutput').textContent = data.summary;
            document.getElementById('resultsSection').style.display = 'block';
            // Scroll to results
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            console.log('Summary from OCR received successfully');
        } else {
            alert('No summary received');
        }
        
    } catch (error) {
        // Basic error handling
        document.getElementById('loadingMessage').style.display = 'none';
        alert('Error: ' + error.message);
        console.error('Fetch error:', error);
    }
}

// Copy summary to clipboard
function copySummary() {
    const summaryText = document.getElementById('summaryOutput').textContent;
    
    if (!summaryText) {
        alert('No summary to copy');
        return;
    }
    
    // Use clipboard API
    navigator.clipboard.writeText(summaryText).then(function() {
        // Show visual feedback
        const btn = event.target.closest('.btn');
        const originalText = btn.querySelector('.btn-text').textContent;
        btn.querySelector('.btn-text').textContent = 'Copied!';
        btn.style.background = 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)';
        
        setTimeout(function() {
            btn.querySelector('.btn-text').textContent = originalText;
            btn.style.background = '';
        }, 2000);
        
        console.log('Summary copied to clipboard');
    }, function(err) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = summaryText;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        // Show visual feedback
        const btn = event.target.closest('.btn');
        const originalText = btn.querySelector('.btn-text').textContent;
        btn.querySelector('.btn-text').textContent = 'Copied!';
        btn.style.background = 'linear-gradient(135deg, #4caf50 0%, #388e3c 100%)';
        
        setTimeout(function() {
            btn.querySelector('.btn-text').textContent = originalText;
            btn.style.background = '';
        }, 2000);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clinical Note Summarizer loaded');
    
    // Add drag and drop functionality for file upload
    const fileUploadArea = document.getElementById('fileUploadArea');
    const fileInput = document.getElementById('imageFile');
    
    if (fileUploadArea && fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileUploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            fileUploadArea.addEventListener(eventName, function() {
                fileUploadArea.style.borderColor = 'var(--primary-color)';
                fileUploadArea.style.backgroundColor = 'var(--primary-light)';
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            fileUploadArea.addEventListener(eventName, function() {
                fileUploadArea.style.borderColor = '';
                fileUploadArea.style.backgroundColor = '';
            }, false);
        });
        
        fileUploadArea.addEventListener('drop', function(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files;
                handleImagePreview({ target: fileInput });
            }
        }, false);
    }
});
