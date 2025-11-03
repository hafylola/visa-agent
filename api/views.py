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
USER QUERY: "{user_message}"

EXTRACT THE PASSPORT COUNTRY from the user's message and provide comprehensive visa information.

YOU MUST RETURN ONLY VALID JSON. NO CONVERSATION. NO QUESTIONS.

REQUIRED JSON FORMAT:
{{
    "passport_country": "extracted country name",
    "visa_free": ["country1", "country2", "country3", "..."],
    "visa_on_arrival": ["country1", "country2", "country3", "..."],
    "visa_required": ["country1", "country2", "country3", "..."],
    "recommendation": "brief travel advice based on visa access"
}}

CRITICAL INSTRUCTIONS:
- Extract passport country from the message
- Provide comprehensive lists of countries in each category
- Return ONLY the JSON object, no other text
- Do not say "checking" or any conversational phrases
- If destination is specified, focus on that country's requirements
- If no destination, provide general visa information for the passport
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

from django.http import HttpResponse

def health_check(request):
    return HttpResponse("Server is working!")