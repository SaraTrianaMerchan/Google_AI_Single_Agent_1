#!/usr/bin/env python3

import os 

try: 
     GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"] 
     print("Gemini API Key setup complete.")
except  KeyError:
    print( "Environment variable 'GOOGLE_API_KEY' not found")
except Exception as e:
    print( f"Unexpected erro: {e}")


