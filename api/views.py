from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
import os

# Configure Gemini - use your actual API key
genai.configure(api_key='AIzaSyCIlo9aJ5KaJ5wtAeKGQaTl75rxexnTbgQ')

@csrf_exempt
def visa_agent(request):
    if request.method == 'POST':
        try:
            # Parse the request
            data = json.loads(request.body)
            print("=== FULL REQUEST ===")
            print(json.dumps(data, indent=2))

            # Extract message from Telex's nested structure
            params = data.get('params', {})
            message_data = params.get('message', {})

            # Get the text - Telex might send it in different places
            user_message = message_data.get('text', '')

            # If no text found, try to extract from parts array
            if not user_message and 'parts' in message_data:
                for part in message_data['parts']:
                    if part.get('kind') == 'text' and part.get('text'):
                        user_message = part['text']
                        break

            print(f"EXTRACTED MESSAGE: '{user_message}'")

            if not user_message:
                return JsonResponse({
                    "response": "{\"error\": \"No message provided\"}",
                    "status": "error"
                })

            # STRICT PROMPT - FORCE JSON ONLY
            prompt = f"""
EXTRACT PASSPORT FROM: "{user_message}"

RETURN ONLY THIS JSON. NO OTHER TEXT. NO CONVERSATION. NO QUESTIONS.

{{
    "passport_country": "country",
    "visa_free": ["country1", "country2", "country3", "country4", "country5"],
    "visa_on_arrival": ["country1", "country2", "country3", "country4", "country5"],
    "visa_required": ["country1", "country2", "country3", "country4", "country5"],
    "recommendation": "one sentence advice"
}}

IF YOU RETURN ANYTHING ELSE BESIDES THIS EXACT JSON FORMAT, THE APPLICATION WILL CRASH.
"""


            # Call Gemini
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)

            # Clean the response - remove any markdown code blocks
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            print(f"AI RESPONSE: {response_text}")

            # Return A2A compliant JSON
            return JsonResponse({
                "response": response_text,
                "status": "success"
            })

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return JsonResponse({
                "response": f"{{\"error\": \"{str(e)}\"}}",
                "status": "error"
            }, status=400)

# Simple health check
def health_check(request):
    return JsonResponse({"status": "healthy", "service": "visa_agent"})

