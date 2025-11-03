from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key='AIzaSyCIlo9aJ5KaJ5wtAeKGQaTl75rxexnTbgQ')

@csrf_exempt
def visa_agent(request):
    if request.method == 'POST':
        try:
            # Parse request
            data = json.loads(request.body)

            # Extract IDs (A2A requirement)
            request_id = data.get('id', '')
            message_id = data.get('params', {}).get('message', {}).get('messageId', '')

            # SIMPLE MESSAGE EXTRACTION (fixes concatenation issue)
            full_text = data.get('params', {}).get('message', {}).get('text', '')

            # If no text found, use default for testing
            if not full_text:
                user_message = "Nigerian passport"
            else:
                # Extract last meaningful part (fixes history problem)
                words = full_text.split()
                if len(words) > 4:
                    user_message = ' '.join(words[-4:])  # Last 4 words
                else:
                    user_message = full_text

            # ULTRA-STRICT PROMPT (fixes conversational AI)
            prompt = f"""EXTRACT PASSPORT COUNTRY FROM: "{user_message}"

OUTPUT ONLY THIS JSON, NOTHING ELSE:

{{
    "passport_country": "country name",
    "visa_free": ["country1", "country2", "country3", "country4", "country5"],
    "visa_on_arrival": ["country1", "country2", "country3", "country4", "country5"],
    "visa_required": ["country1", "country2", "country3", "country4", "country5"],
    "recommendation": "one sentence advice"
}}"""

            # Call Gemini
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)

            # Clean response
            response_text = response.text.strip()
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()

            # Return PERFECT A2A JSON (fixes protocol issues)
            return JsonResponse({
                "id": request_id,
                "messageId": message_id,
                "response": response_text,
                "status": "success"
            })

        except Exception as e:
            # Error response still follows A2A format
            return JsonResponse({
                "id": data.get('id', ''),
                "messageId": message_id,
                "response": "{\"error\": \"Processing failed\"}",
                "status": "error"
            }, status=400)

def health_check(request):
    return JsonResponse({"status": "visa_agent_healthy"})

