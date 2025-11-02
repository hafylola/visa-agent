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
            # Get the message from Telex
            data = json.loads(request.body)
            user_message = data.get('message', '')

            # Create AI prompt
            prompt = f"""
            The user said: "{user_message}"

            Extract their passport country and provide visa information.

            Return ONLY valid JSON with this exact structure:
            {{
                "passport_country": "extracted country name",
                "visa_free": ["country1", "country2", "country3"],
                "visa_on_arrival": ["country1", "country2", "country3"],
                "visa_required": ["country1", "country2", "country3"],
                "recommendation": "brief travel advice"
            }}

            Include comprehensive lists of countries. Be accurate.
            """

            # Call Gemini AI
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)

            # Return the AI response to Telex
            return JsonResponse({
                "response": response.text,
                "status": "success"
            })

        except Exception as e:
            return JsonResponse({
                "error": f"Something went wrong: {str(e)}",
                "status": "error"
            }, status=400)

