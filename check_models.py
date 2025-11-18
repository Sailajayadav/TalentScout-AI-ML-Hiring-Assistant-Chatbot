#!/usr/bin/env python3
"""Check available GenAI models for the current API key."""
import os, json, urllib.request, urllib.error
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('GEMINI_API_KEY')
if not key:
    print("ERROR: GEMINI_API_KEY not set in .env or environment")
    import sys; sys.exit(1)

url = f'https://generativelanguage.googleapis.com/v1beta/models?key={key}'
print(f"Querying: {url[:60]}...")

try:
    response = urllib.request.urlopen(url)
    data = json.load(response)
    models = data.get('models', [])
    
    if not models:
        print("\nNo models returned.")
        print("Possible causes: key/project has no access, is suspended, or billing not set up.")
    else:
        print(f"\nFound {len(models)} model(s):\n")
        for m in models:
            name = m.get('name', 'unknown')
            version = m.get('version', 'unknown')
            print(f"  • {name} (version: {version})")
            
except urllib.error.HTTPError as e:
    print(f"\nHTTP Error {e.code}: {e.reason}")
    try:
        err_body = json.load(e.fp)
        print("Response details:")
        print(json.dumps(err_body, indent=2))
    except:
        body = e.read().decode()
        print(f"Response: {body[:500]}")
        
except Exception as e:
    print(f"\nError: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
