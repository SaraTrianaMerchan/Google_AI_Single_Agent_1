#!/usr/bin/env python3

from google.genai.types import HttpRetryOptions

retry_config = HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1, # Initial delay before first retry (in seconds)
    http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
)

print("Retry Confin OK.")
