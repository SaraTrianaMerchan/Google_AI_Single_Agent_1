#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
from typing import Dict, Any

# Add parent directory to path to import agent module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import ask_agent
import asyncio

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Vercel serverless function handler for the agent API.

    Expected POST body:
    {
        "question": "What is the weather today?"
    }

    Returns:
    {
        "response": "The agent's response..."
    }
    """

    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }

    # Handle OPTIONS request for CORS preflight
    if event.get("httpMethod") == "OPTIONS" or event.get("method") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": ""
        }

    try:
        # Parse request body
        if isinstance(event.get("body"), str):
            body = json.loads(event.get("body", "{}"))
        else:
            body = event.get("body", {})

        question = body.get("question", "").strip()

        if not question:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "error": "Question is required",
                    "message": "Please provide a 'question' field in the request body"
                })
            }

        # Call the agent
        print(f"[INFO] Processing question: {question}")
        response = asyncio.run(ask_agent(question))

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({
                "response": response,
                "question": question
            })
        }

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        }
