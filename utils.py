"""
Text processing utilities for clinical notes.
Expands abbreviations and cleans text.
"""

# Dictionary of common medical abbreviations
MEDICAL_ABBREV = {
    'pt': 'patient',
    'hx': 'history',
    'c/o': 'complains of',
    'bp': 'blood pressure',
    'hr': 'heart rate',
    'dx': 'diagnosis',
    'tx': 'treatment',
    'rx': 'prescription',
    'bid': 'twice daily',
    'tid': 'three times daily',
    'qd': 'once daily',
    'sob': 'shortness of breath',
    'n/v': 'nausea and vomiting',
    'cp': 'chest pain',
    'prn': 'as needed',
    'yo': 'years old',
    'mg': 'milligrams',
    'ecg': 'electrocardiogram',
    'sx': 'symptoms',
    'htn': 'hypertension',
    'dm': 'diabetes mellitus',
    'copd': 'chronic obstructive pulmonary disease',
    'mi': 'myocardial infarction',
    'cad': 'coronary artery disease',
    'cbc': 'complete blood count',
    'bmp': 'basic metabolic panel',
    'labs': 'laboratory tests',
    'w/u': 'workup'
}


def expand_abbreviations(text):
    """
    Expand medical abbreviations in text.
    Simple word-by-word replacement.
    """
    words = text.split()
    expanded = []
    
    for word in words:
        # Remove punctuation for matching
        word_lower = word.lower().strip('.,;:!?()[]')
        
        if word_lower in MEDICAL_ABBREV:
            # Replace abbreviation with full form
            expanded.append(MEDICAL_ABBREV[word_lower])
        else:
            expanded.append(word)
    
    return ' '.join(expanded)


def clean_text(text):
    """
    Basic text cleaning - remove extra whitespace.
    """
    if not text:
        return ""
    
    # Remove multiple spaces
    cleaned = ' '.join(text.split())
    
    # Remove extra newlines
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    
    return '\n'.join(lines)


def preprocess_clinical_text(text):
    """
    Main preprocessing function - combines cleaning and abbreviation expansion.
    """
    if not text:
        return ""
    
    # First clean the text
    cleaned = clean_text(text)
    
    # Then expand abbreviations
    # Note: This is a simple approach - could be improved but keeping it basic
    expanded = expand_abbreviations(cleaned)
    
    return expanded
