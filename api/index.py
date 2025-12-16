#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

# Get API key
api_key = os.environ.get('GOOGLE_API_KEY')

if not api_key:
    print("[ERROR] GOOGLE_API_KEY environment variable is not set!")
else:
    print(f"[INFO] API Key configured: {api_key[:10]}...")

# Configure the API
genai.configure(api_key=api_key)

# Create the model - Using stable Gemini 1.5 Flash
model = genai.GenerativeModel('gemini-1.5-flash')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Handle POST request"""
        try:
            # Check API key
            if not os.environ.get('GOOGLE_API_KEY'):
                self.send_error_response(500, "API Key not configured. Please add GOOGLE_API_KEY to environment variables.")
                return

            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))

            # Read and parse body
            body = self.rfile.read(content_length).decode('utf-8')
            print(f"[DEBUG] Request body: {body}")

            data = json.loads(body) if body else {}

            question = data.get('question', '').strip()

            if not question:
                self.send_error_response(400, "Question is required")
                return

            # Generate response using Gemini
            print(f"[INFO] Processing question: {question}")

            response = model.generate_content(question)

            print(f"[INFO] Got response: {response.text[:100]}...")

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            result = {
                "response": response.text,
                "question": question
            }

            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            import traceback
            print(f"[ERROR] {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.send_error_response(500, str(e))

    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        error = {
            "error": "Error",
            "message": message
        }

        self.wfile.write(json.dumps(error).encode('utf-8'))
