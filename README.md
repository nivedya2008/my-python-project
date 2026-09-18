# Advanced Password Generator & Strength Checker

A high-performance Python security tool designed to generate cryptographically secure passwords and evaluvate validation strength in real-time.

## Core Features
* **Secure Entropy:** Leverages Python's 'secrets' module for secure randomized character generation.
* **Pattern Validation:** inspects length thresholds and character diversity using regular expressions ('re').
* **Vulnerability Mitigation:** instantly flags common weak strings, consecutive repetitions, and predictable sequences.

## Technical Stack
* **Language:** Python 3.x
* **Core Modules:** 'secrets' | 'string' | 're'

## About the Developer
* **Education:** 2nd-Year BCA student
* **Focus Area:** Python Engineering, Automation, and Secure Input Validation.
* **Goal:** Building clean, optimized, and production-ready source code.


## Link Shorter & QR Code Generator

A simple and engaging Python terminal-based program that helps users shorten long URLs and automatically generates a text-based ASCII QR code in the terminal.

### Features
- **User Greetings:** Interactive welcome with username input.
-**URL Validation:** Checks if the URL starts with 'http://' or 'https://'.
-**Link Shortener:** Generates a simulated short link.
-**ASCII QR Code:** Automatically creates a fun QR code in the console.

### How to Run
Run the following command in your terminal:
'''bash
python link_tool.py
'''


### 4. Smart Contact Book (CLI Applicaton)
* **Description:** An interactive command-line application that allows users to add, view, search, and delete contacts dynamically.
* **Key Features:** Input validation (ensuring strict 10-digit phone numbers and valid emails), custom error handling (`try-except`), and local data persistence using JSON formatting.
* **Core File:** `contact_book.py`