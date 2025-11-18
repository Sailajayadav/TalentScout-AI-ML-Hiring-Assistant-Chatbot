from dotenv import load_dotenv
load_dotenv()
import inspect
import os

try:
    from google import genai
except Exception as e:
    print('ERROR: cannot import google.genai ->', e)
    raise

c = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
print('Client created:', type(c))
print('Has attribute models:', hasattr(c, 'models'))
if hasattr(c, 'models'):
    models = c.models
    print('models object type:', type(models))
    gen = getattr(models, 'generate_content', None)
    print('models.generate_content exists:', gen is not None)
    if gen is not None:
        try:
            print('generate_content signature:', inspect.signature(gen))
        except Exception as e:
            print('Could not get signature for models.generate_content:', e)

print('Client has generate_text:', hasattr(c, 'generate_text'))
print('Client has generate:', hasattr(c, 'generate'))
print('Client has models.generate:', hasattr(getattr(c, 'models', None), 'generate' ) )
print('Client has models.generate_content:', hasattr(getattr(c, 'models', None), 'generate_content'))

# Try calling models.generate_content with a minimal set (dry run) using try/except to see exact error
try:
    print('\nAttempting a test call to models.generate_content with direct params...')
    c.models.generate_content(model='test-model', contents='hi', temperature=0.1, max_output_tokens=10)
except Exception as e:
    print('Direct params call error:', type(e), e)

try:
    print('\nAttempting a test call to models.generate_content with generation_config...')
    c.models.generate_content(model='test-model', contents='hi', generation_config={'temperature':0.1, 'max_output_tokens':10})
except Exception as e:
    print('generation_config call error:', type(e), e)

try:
    print('\nAttempting top-level client.generate_text...')
    if hasattr(c, 'generate_text'):
        c.generate_text(model='test-model', prompt='hi', temperature=0.1, max_output_tokens=10)
    else:
        print('generate_text not present')
except Exception as e:
    print('client.generate_text error:', type(e), e)

print('\nDone')
