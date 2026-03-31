"""
Password Strength & Security Analyzer
A professional security tool using Shannon Entropy, HaveIBeenPwned API, and zxcvbn
"""

import hashlib
import math
import requests
from collections import Counter
from flask import Flask, render_template, request, jsonify
from zxcvbn import zxcvbn

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ==================== SHANNON ENTROPY CALCULATION ====================
def calculate_shannon_entropy(password: str) -> float:
    """
    Calculate Shannon Entropy to measure password randomness.
    
    Shannon Entropy formula: H(X) = -Σ P(x) * log2(P(x))
    
    Where:
    - P(x) is the probability of each character
    - log2 is the logarithm base 2
    
    Higher entropy = more random = stronger password
    Typically, passwords should have entropy > 50 bits for security
    
    Args:
        password: The password to analyze
        
    Returns:
        Float representing entropy in bits
    """
    if not password:
        return 0.0
    
    # Count character frequencies
    char_counts = Counter(password)
    password_length = len(password)
    
    # Calculate entropy
    entropy = 0.0
    for count in char_counts.values():
        probability = count / password_length
        entropy -= probability * math.log2(probability)
    
    return entropy * password_length


# ==================== HAVE I BEEN PWNED API (k-ANONYMITY) ====================
def check_haveibeenpwned(password: str) -> dict:
    """
    Check if password appears in known data breaches using k-Anonymity.
    
    k-Anonymity Protection:
    - Only the first 5 characters of the SHA-1 hash are sent to the API
    - The API returns all hashes matching those 5 characters
    - We check locally if our full hash is in the list
    - The API cannot know which specific password we're checking
    
    Args:
        password: The password to check
        
    Returns:
        Dictionary with:
        - 'compromised': Boolean indicating if password was found in breaches
        - 'breach_count': Number of breaches the password appeared in
        - 'message': Human-readable message
    """
    try:
        # Calculate SHA-1 hash of password
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1_hash[:5]  # k-Anonymity: only send first 5 chars
        suffix = sha1_hash[5:]
        
        # Request from HIBP API
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        headers = {'User-Agent': 'PasswordAnalyzer/1.0'}
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        # Check if our suffix is in the response
        hashes = response.text.split('\r\n')
        for hash_entry in hashes:
            if not hash_entry:
                continue
            stored_suffix, count = hash_entry.split(':')
            if stored_suffix == suffix:
                return {
                    'compromised': True,
                    'breach_count': int(count),
                    'message': f'⚠️ Password found in {count} known data breaches!'
                }
        
        return {
            'compromised': False,
            'breach_count': 0,
            'message': '✅ Password not found in known data breaches'
        }
        
    except requests.RequestException as e:
        return {
            'compromised': None,
            'breach_count': 0,
            'message': f'Could not verify with HaveIBeenPwned (API unavailable): {str(e)}'
        }


# ==================== CHARACTER SET ANALYSIS ====================
def analyze_character_sets(password: str) -> dict:
    """
    Analyze the character sets used in the password.
    
    Args:
        password: The password to analyze
        
    Returns:
        Dictionary with character set details
    """
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += 32
    
    return {
        'has_lowercase': has_lower,
        'has_uppercase': has_upper,
        'has_digits': has_digit,
        'has_special': has_special,
        'charset_size': charset_size,
        'character_count': len(set(password))
    }


# ==================== COMPREHENSIVE STRENGTH ASSESSMENT ====================
def assess_password_strength(password: str) -> dict:
    """
    Comprehensive password security assessment combining multiple factors.
    
    Factors considered:
    1. Shannon Entropy (randomness)
    2. Length requirements
    3. Character diversity
    4. Known breach history (HaveIBeenPwned)
    5. Common patterns (zxcvbn)
    
    Args:
        password: The password to assess
        
    Returns:
        Dictionary with comprehensive strength assessment
    """
    if not password:
        return {
            'strength_score': 0,
            'strength_label': 'Empty',
            'entropy': 0,
            'entropy_bits': 0,
            'length_score': 0,
            'variety_score': 0,
            'pattern_score': 5,
            'breach_result': {'compromised': False, 'breach_count': 0, 'message': ''},
            'character_sets': {},
            'recommendations': ['Enter a password to analyze'],
            'color': '#999999'
        }
    
    # Calculate Shannon Entropy
    entropy = calculate_shannon_entropy(password)
    # Entropy is already in bits (from Shannon formula with password_length multiplier)
    entropy_bits = entropy
    
    # Analyze character sets
    char_analysis = analyze_character_sets(password)
    
    # Length score (0-25 points)
    length = len(password)
    if length < 8:
        length_score = length * 2
    elif length < 12:
        length_score = 16 + (length - 8) * 2
    else:
        length_score = 25
    
    # Variety score (0-25 points)
    variety_count = sum([
        char_analysis['has_lowercase'],
        char_analysis['has_uppercase'],
        char_analysis['has_digits'],
        char_analysis['has_special']
    ])
    variety_score = variety_count * 6.25
    
    # Pattern analysis using zxcvbn (score 0-4, higher is better)
    zxcvbn_result = zxcvbn(password)
    pattern_score = zxcvbn_result['score'] * 6.25  # Convert 0-4 score to 0-25 points
    
    # Breach check
    breach_result = check_haveibeenpwned(password)
    
    # Calculate total strength (0-100)
    # Components: Entropy (25%) + Length (25%) + Variety (25%) + Pattern (25%)
    entropy_max_score = min(25, (entropy_bits / 50) * 25)
    strength_score = (entropy_max_score + length_score + variety_score + pattern_score) / 4
    
    # Penalize if password found in breaches
    if breach_result['compromised']:
        strength_score *= 0.5
    
    strength_score = min(100, max(0, strength_score))
    
    # Determine strength label and color - Updated color palette
    if strength_score >= 80:
        strength_label = 'Very Strong'
        color = '#06b6d4'  # Cyan
    elif strength_score >= 60:
        strength_label = 'Strong'
        color = '#10b981'  # Emerald
    elif strength_score >= 40:
        strength_label = 'Moderate'
        color = '#f59e0b'  # Amber
    elif strength_score >= 20:
        strength_label = 'Weak'
        color = '#ef4444'  # Red
    else:
        strength_label = 'Very Weak'
        color = '#991b1b'  # Dark Red
    
    # Generate recommendations
    recommendations = []
    if length < 12:
        recommendations.append('Use at least 12 characters')
    if not char_analysis['has_uppercase']:
        recommendations.append('Add uppercase letters (A-Z)')
    if not char_analysis['has_digits']:
        recommendations.append('Add digits (0-9)')
    if not char_analysis['has_special']:
        recommendations.append('Add special characters (!@#$%^&*)')
    if zxcvbn_result['score'] < 4:
        if zxcvbn_result['feedback']['suggestions']:
            recommendations.extend(zxcvbn_result['feedback']['suggestions'][:2])
    if entropy_bits < 50:
        recommendations.append(f'Increase password entropy (current: {entropy_bits:.1f} bits, target: >50 bits)')
    
    if not recommendations:
        recommendations.append('Password is well-constructed!')
    
    return {
        'strength_score': round(strength_score, 2),
        'strength_label': strength_label,
        'entropy': round(entropy, 4),
        'entropy_bits': round(entropy_bits, 2),
        'length_score': round(length_score, 2),
        'variety_score': round(variety_score, 2),
        'pattern_score': round(pattern_score, 2),
        'breach_result': breach_result,
        'character_sets': char_analysis,
        'zxcvbn_score': zxcvbn_result['score'],
        'recommendations': recommendations,
        'color': color
    }


# ==================== FLASK ROUTES ====================
@app.route('/')
def index():
    """Display the main analyzer page."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint to analyze password strength.
    
    Expected JSON:
    {
        "password": "user_password_string"
    }
    """
    data = request.get_json()
    password = data.get('password', '')
    
    result = assess_password_strength(password)
    
    return jsonify(result)


@app.route('/api/entropy-explanation', methods=['GET'])
def entropy_explanation():
    """Provide information about Shannon Entropy."""
    return jsonify({
        'title': 'Shannon Entropy',
        'description': 'Measures the randomness and unpredictability of a password.',
        'formula': 'H(X) = -Σ P(x) * log2(P(x))',
        'unit': 'bits per character',
        'significance': 'Higher entropy indicates greater randomness and strength',
        'safe_threshold': '> 50 bits total entropy'
    })


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
