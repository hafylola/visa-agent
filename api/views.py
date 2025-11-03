from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai
import os
import uuid
from datetime import datetime

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
                # Return JSON-RPC format for error too
                return JsonResponse({
                    "jsonrpc": "2.0",
                    "id": data.get('id', ''),
                    "error": {
                        "code": -32600,
                        "message": "No message provided"
                    }
                })

            # STRICT PROMPT - FORCE JSON ONLY
            prompt = f"""
            EXTRACT THE PASSPORT COUNTRY FROM THIS USER MESSAGE: "{user_message}"

            YOU MUST RETURN ONLY VALID JSON. NO OTHER TEXT.

            REQUIRED JSON FORMAT:
            {{
                "passport_country": "extracted passport country",
                "visa_free": ["list of 5-10 visa-free countries"],
                "visa_on_arrival": ["list of 5-10 visa-on-arrival countries"],
                "visa_required": ["list of 5-10 visa-required countries"],
                "recommendation": "brief travel advice based on visa access"
            }}

            RULES:
            - Extract passport country from the message
            - Return ONLY the JSON object, no other text
            - No conversation, no questions, no "checking" messages
            - If multiple passports mentioned, use the first one
            - If destination specified, focus visa info on that country
            """

            # Call Gemini
            model = genai.GenerativeModel('gemini-2.5-pro')
            response = model.generate_content(prompt)

            # Clean the response - remove any markdown code blocks
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            print(f"AI RESPONSE: {response_text}")

            # Generate IDs for JSON-RPC response
            task_id = str(uuid.uuid4())
            message_id = str(uuid.uuid4())
            context_id = str(uuid.uuid4())

            # Return CORRECT JSON-RPC 2.0 format
            return JsonResponse({
                "jsonrpc": "2.0",
                "id": data.get('id', ''),
                "result": {
                    "id": task_id,
                    "contextId": context_id,
                    "status": {
                        "state": "completed",
                        "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        "message": {
                            "kind": "message",
                            "role": "agent",
                            "parts": [
                                {
                                    "kind": "text",
                                    "text": response_text
                                }
                            ],
                            "messageId": message_id,
                            "taskId": task_id
                        }
                    }
                }
            })

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return JsonResponse({
                "jsonrpc": "2.0",
                "id": data.get('id', ''),
                "error": {
                    "code": -32000,
                    "message": str(e)
                }
            })

# Simple health check
def health_check(request):
    return JsonResponse({"status": "healthy", "service": "visa_agent"})



