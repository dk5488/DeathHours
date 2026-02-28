import json
from google import genai
from google.genai import types

client = genai.Client()

def generate_hour_data_from_gemini(business_gmap_uri: str) -> dict:
    # 1. Define the Grounding Tool
    # The 'google_search_retrieval' tool allows the model to access 
    # real-time Google Search and Maps data.
    google_maps_tool = types.Tool(
        google_search_retrieval=types.GoogleSearchRetrieval()
    )

    config = types.GenerateContentConfig(
        system_instruction="""You are a data extraction system.
Return ONLY valid JSON. Do not include explanation, markdown, or comments.
Reference Data: Use the "Popular Times" historical average data.""",
        # 2. Set Temperature to 0 for maximum determinism
        temperature=0,
        # 3. Enable the Grounding Tool
        tools=[google_maps_tool],
        response_mime_type="application/json"
    )

    user_prompt = f"Extract busy hours for the business with Google Maps URI: {business_gmap_uri}"

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=user_prompt,
        config=config
    )
    
    return json.loads(response.text)