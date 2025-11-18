# verbose_listmodels.py
from dotenv import load_dotenv
load_dotenv()
import os, json, traceback
try:
    from google import genai
except Exception as e:
    print("ERROR importing google.genai:", e)
    raise

api_key = os.getenv("GEMINI_API_KEY")
print("Using GEMINI_API_KEY set:", bool(api_key))

try:
    client = genai.Client(api_key=api_key)
    print("Client created:", type(client))
except Exception as e:
    print("Failed creating client:", type(e), e)
    traceback.print_exc()
    raise SystemExit(1)

# try preferred method
try:
    if hasattr(client, "list_models"):
        print("Calling client.list_models()")
        models = client.list_models()
    else:
        print("Calling client.models.list()")
        models = client.models.list()
    print("Raw models repr:\n", repr(models)[:4000])
    # Try to iterate and print attributes
    count = 0
    for m in models:
        count += 1
        print("---- model", count, "----")
        # print some common attributes
        for attr in ("name", "model", "display_name", "id", "supported_methods", "metadata"):
            if hasattr(m, attr):
                try:
                    val = getattr(m, attr)
                    print(f"{attr}:", json.dumps(val, default=str) if not isinstance(val, str) else val)
                except Exception as e:
                    print(f"{attr}: <error getting attribute: {e}>")
        # print a short repr
        try:
            print('repr:', repr(m)[:400])
        except Exception:
            pass
    print("Total models iterated:", count)
except Exception as e:
    print("Error while listing models:", type(e), e)
    traceback.print_exc()
