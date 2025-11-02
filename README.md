# Visa Requirements Agent

An AI-powered agent that provides visa information for passport holders. Built with Django and Google Gemini AI.

## What It Does
- Takes a passport nationality (e.g., "I have a Nigerian passport")
- Returns visa-free, visa-on-arrival, and visa-required countries
- Provides travel recommendations

## API Endpoint
POST /a2a/agent/visa-agent
Content-Type: application/json

{
"message": "I have a Nigerian passport"
}



## Response Format
```json
{
  "passport_country": "Nigeria",
  "visa_free": ["Ghana", "Rwanda", "Kenya"],
  "visa_on_arrival": ["Maldives", "Cambodia"],
  "visa_required": ["United States", "United Kingdom", "Canada"],
  "recommendation": "Consider visa-free travel to Rwanda or Kenya"
}
```