# Password Strength & Security Analyzer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/static/v1?label=Framework&message=Flask%202.3&color=success)](https://flask.palletsprojects.com/)
[![Code Style: Professional](https://img.shields.io/badge/Code%20Style-Professional-brightgreen)](https://pep8.org/)

A professional-grade password security analysis tool built with Python and Flask. This application combines cutting-edge cryptographic theories, breach detection, and pattern recognition to provide comprehensive password strength assessment.

**Live Analysis** | **Real-time Scoring** | **Breach Detection** | **Pattern Recognition**

## 📋 Table of Contents

- [Features](#features)
- [Cybersecurity Concepts](#cybersecurity-concepts)
- [Technology Stack](#technology-stack)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [Metrics & Algorithms](#metrics--algorithms)

---

## ⭐ Features

### Real-Time Analysis
- **Live password evaluation** as you type
- Instant visual feedback with dynamic strength meter
- Real-time scoring breakdowns

### Advanced Security Metrics
- **Shannon Entropy Calculation**: Measures password randomness (target: >50 bits)
- **HaveIBeenPwned Integration**: Checks against 613+ million known compromised passwords
- **Pattern Detection**: Identifies keyboard patterns, dictionary words, sequences, and names
- **Character Analysis**: Evaluates character set diversity and distribution
- **Entropy Breakdown**: Displays detailed scoring for length, variety, patterns, and randomness

### Modern User Interface
- Gradient-based color coding (Red → Yellow → Green)
- Responsive design (desktop, tablet, mobile)
- Comprehensive metrics dashboard
- Actionable security recommendations

### Privacy-Focused
- **Local analysis**: Password never sent unencrypted
- **k-Anonymity protocol**: Only hash prefixes sent to external APIs
- No server-side password storage

---

## 🔬 Cybersecurity Concepts

### 1. Shannon Entropy (Information Theory)

**Definition**: A measure of the average information content (uncertainty) in a password.

**Formula**:
```
H(X) = -Σ P(x) * log₂(P(x))
```

Where:
- `P(x)` = probability of each unique character
- `log₂` = logarithm base 2
- Entropy is multiplied by password length for total bits

**Why It Matters**:
- Higher entropy = more random / harder to guess
- **Target**: >50 bits for strong security
- 50 bits requires ~2⁵⁰ operations to brute force (~1.1 quadrillion attempts)

**Example**:
- Password "aaaaaaaaaa": Very low entropy (only 1 unique character)
- Password "Tr0pic@lM@ng0": High entropy (diverse, mixed case, special chars)

**Security Threshold**:
- <40 bits: Weak (can be cracked in minutes)
- 40-50 bits: Moderate (hours to days)
- 50-60 bits: Strong (weeks to months)
- >60 bits: Very strong (years with modern hardware)

---

### 2. HaveIBeenPwned API with k-Anonymity

**Overview**: A database of 613+ million compromised passwords from public data breaches.

**The k-Anonymity Protocol**:

The key innovation is protecting user privacy while checking passwords:

1. **Hash the password**:
   ```
   SHA-1("MyPassword123") = A1B2C3D4E5F6...
   ```

2. **Send only the first 5 characters**:
   ```
   Request: "A1B2C" 
   (full hash never exposed to the API)
   ```

3. **Receive all matches for that prefix**:
   ```
   Server returns: [A1B2C:15, A1B2D:42, A1B2E:8, ...]
   (potentially thousands of hashes)
   ```

4. **Check locally** which one matches your password's suffix

**Why k-Anonymity is Important**:
- `k=1` anonymity means at least 1 other password has the same prefix
- In HIBP's case, typically k > 10,000 for common prefixes
- Impossible for API to know *which* exact password was checked
- Prevents targeted surveillance

**Security Guarantees**:
- Your full password hash is never exposed
- Even HIBP's servers cannot determine which password you're checking
- Provides differential privacy against mass surveillance

---

### 3. Pattern Recognition (zxcvbn)

**Definition**: A library for detecting predictable patterns that reduce password entropy.

**Patterns Detected**:

| Category | Examples | Risk Level |
|----------|----------|-----------|
| **Dictionary words** | "password", "admin", "123456" | Very High |
| **Sequences** | "abc", "123", "qwerty" | High |
| **Keyboard patterns** | "qwerty", "asdf", "zxcv" | High |
| **Date patterns** | "1999", "12/31", "2023-06-15" | Medium-High |
| **Names** | "John", "Mary", "Michael" | Medium |
| **Spatial patterns** | Consecutive keys on keyboard | Medium-High |
| **Repeating chars** | "aaaa", "1111" | High |
| **Reversed words** | "drowssap" | Medium |

**zxcvbn Score (0-4)**:
- **0**: Extremely weak (cracks instantly)
- **1**: Weak (hours)
- **2**: Fair (days to weeks)
- **3**: Good (months)
- **4**: Strong (years+)

**Example Analysis**:
```
Password: "password123"
Patterns detected:
  - Dictionary word: "password"
  - Sequential digits: "123"
zxcvbn Score: 0 (extremely predictable)

Password: "7Qk#mP9v!2xR"
Patterns detected:
  - None
zxcvbn Score: 4 (very unpredictable)
```

---

### 4. Character Set Analysis

**Character types**:
- **Lowercase** (26): a-z
- **Uppercase** (26): A-Z
- **Digits** (10): 0-9
- **Special** (32+): !@#$%^&*()-_=+[]{};':",.<>?/\|`~

**Effective Character Space**:
```
Total possible characters = Sum of character type sizes
Example: lowercase + uppercase + digits = 26 + 26 + 10 = 62
```

**Entropy per character** = log₂(character_space)
```
- 26-char alphabet: log₂(26) ≈ 4.7 bits/char
- 62-char set: log₂(62) ≈ 5.95 bits/char
- 94-char set: log₂(94) ≈ 6.55 bits/char
```

---

### 5. Scoring Methodology (100-point scale)

The analyzer combines four factors with equal weighting:

**Overall Score = (Length + Variety + Entropy + Pattern) / 4**

#### Length Score (0-25 points)
- 0-2 chars: 0 points
- Each char + 2 points (up to 8 chars)
- At 12+ chars: 25 points

#### Variety Score (0-25 points)
- Each character type: +6.25 points
- Max: 4 types × 6.25 = 25 points

#### Entropy Score (0-25 points)
- Based on Shannon entropy in bits
- Formula: min(25, (entropy_bits / 50) × 25)
- 50 bits = full 25 points

#### Pattern Score (0-25 points)
- Based on zxcvbn's detection
- zxcvbn score 4 = 25 points
- zxcvbn score 0 = 0 points

**Final Strength Categories**:
- **80-100**: Very Strong 🔐 (Green)
- **60-79**: Strong 💪 (Light Green)
- **40-59**: Moderate ⚡ (Orange)
- **20-39**: Weak ⚠️ (Red)
- **0-19**: Very Weak ❌ (Dark Red)

**Penalty**: If password found in breaches, multiply score by 0.5

---

## 🛠 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.8+ | Server logic and analysis |
| **Framework** | Flask 2.3 | Web server and routing |
| **Frontend** | HTML5/CSS3/JavaScript | User interface |
| **Pattern Recognition** | zxcvbn 4.4 | Advanced password analysis |
| **API Integration** | requests 2.31 | HaveIBeenPwned API calls |
| **Hashing** | hashlib (SHA-1) | Password hashing for HIBP |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for HaveIBeenPwned API)

### Step 1: Clone/Download the Project
```bash
cd password-analyzer
```

### Step 2: Create Virtual Environment (Recommended)

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import flask, zxcvbn, requests; print('All dependencies installed successfully!')"
```

---

## 🚀 Running the Application

### Start the Flask Server

**Windows (Command Prompt)**:
```bash
python app.py
```

**macOS/Linux**:
```bash
python3 app.py
```

### Expected Output
```
WARNING in app.runWarnings...
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access the Application
1. Open your web browser
2. Navigate to: **http://127.0.0.1:5000**
3. Start typing a password to analyze

### Stopping the Server
Press `Ctrl+C` in the terminal

---

## 🏗 Architecture

### Project Structure
```
password-analyzer/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── templates/
│   └── index.html                  # Frontend UI
└── static/
    └── css/
        └── style.css               # Styling
```

### Request Flow

```
User Input (Browser)
        ↓
[JavaScript] Real-time input capture
        ↓
POST /api/analyze (JSON)
        ↓
[Flask Backend] assess_password_strength()
        ├─ calculate_shannon_entropy()
        ├─ analyze_character_sets()
        ├─ zxcvbn pattern analysis
        ├─ check_haveibeenpwned()
        │   └─ k-Anonymity protocol
        └─ generate score & recommendations
        ↓
JSON Response
        ↓
[JavaScript] Update UI
        ├─ Update strength meter & color
        ├─ Display metrics
        ├─ Show recommendations
        └─ Animate transitions
```

### Data Flow (HaveIBeenPwned)

```
1. Local Password: "MySecurePass"
        ↓
2. SHA-1 Hash: "A1B2C3D4E5..."
        ↓
3. Extract Prefix: "A1B2C" (5 chars)
        ↓
4. Send to API: GET /range/A1B2C
        ↓
5. Receive Response: [hash1:count1, hash2:count2, ...]
        ↓
6. Match Suffix Locally: "D4E5..." found?
        ├─ YES → Compromised (show count)
        └─ NO → Safe
```

---

## 📊 Metrics & Algorithms

### Shannon Entropy Calculation
```python
entropy_bits = sum of character count / password_length * log2(count/length)
               × password_length
```

### Charset Size Formula
```
charset_size = 26 (if lowercase) + 26 (if uppercase) 
               + 10 (if digits) + 32 (if special)
```

### Effective Security Bits
```
total_entropy_bits = password_length × log2(charset_size)
```

### Time to Crack (Rough Estimates)
```
10 bits  = 1 millisecond (modern GPU)
20 bits  = 1 second
30 bits  = 15 minutes
40 bits  = 1 week
50 bits  = 25 years
60 bits  = 25,000 years
```

---

## 🔒 Security Considerations

### What's Protected
✅ Password is never stored on server  
✅ Password never sent in plaintext  
✅ Only SHA-1 hash prefix sent to HIBP  
✅ Analysis performed client-side when possible  
✅ Uses HTTPS for API calls  

### What's Not Protected
⚠️ Password visible in browser memory  
⚠️ Not suitable for absolutely critical passwords  
⚠️ Depends on HIBP API availability  

### Best Practices
1. Use this tool in a **private/incognito browser window**
2. For highly sensitive passwords, run locally (air-gapped)
3. Don't use identical passwords across multiple services
4. Enable **2FA** on important accounts
5. Use a **password manager** (Bitwarden, 1Password, KeePass)

---

## 🧪 Testing

### Test Case Examples

**Test 1: Weak Password**
```
Input: "password"
Expected: Very Weak (score < 20)
Reasons: Dictionary word, low entropy, all lowercase
```

**Test 2: Strong Password**
```
Input: "Tr0pic@lThund3r$tay"
Expected: Very Strong (score > 80)
Reasons: Mixed case, digits, symbols, high entropy, no patterns
```

**Test 3: Compromised Password**
```
Input: "123456"
Expected: Weak (score heavily reduced due to compromise count)
Reasons: Found in 10+ million breach records
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Connection timeout" on HaveIBeenPwned check
**Solution**: 
- Check internet connection
- API might be temporarily unavailable (rare)
- Tool will gracefully handle and show "API unavailable" message

### Issue: "Address already in use" on port 5000
**Solution**: 
```bash
# Find and stop the process using port 5000
# Or specify a different port in app.py
```

### Issue: Static files not loading (CSS/JS not working)
**Solution**: 
- Ensure `static/css/style.css` exists
- Restart Flask server
- Clear browser cache (Ctrl+F5 / Cmd+Shift+R)

---

## 📚 References

### Cryptography & Entropy
- Shannon, C. E. (1948). "A Mathematical Theory of Communication"
- NIST Special Publication 800-63B: Password Guidelines
- Schneier, B. (2007). "Applied Cryptography"

### Password Security
- HaveIBeenPwned: https://haveibeenpwned.com
- zxcvbn Library: https://github.com/dropbox/zxcvbn
- OWASP Password Security: https://owasp.org/www-community/password

### Python Libraries Documentation
- Flask: https://flask.palletsprojects.com/
- requests: https://requests.readthedocs.io/
- zxcvbn-python: https://github.com/stephenornelas/zxcvbn

---

## 📄 License

This project is open source and available for educational and professional use.

---

## ✨ Features Roadmap

Potential future enhancements:
- [ ] Password history tracking
- [ ] Custom dictionary import
- [ ] Multi-language pattern detection
- [ ] Export security report
- [ ] Dark mode UI
- [ ] Offline mode (HIBP data cache)
- [ ] Browser extension version
- [ ] REST API for integration

---

## 🤝 Contributing

Improvements and bug reports are welcome! Areas for contribution:
- Enhanced pattern detection
- UI/UX improvements
- Performance optimization
- Additional language support
- Security audit results

---

**Built with ❤️ for cybersecurity professionals and developers**
