from typing import Dict, Any, List
import os

# Resilient imports
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.schema import SystemMessage, HumanMessage, AIMessage
    AI_AVAILABLE = True
except ImportError as e:
    print(f"Warning: AI dependencies missing ({e}). Using mock AI logic.")
    AI_AVAILABLE = False

def get_expert_analysis(weather_data: Dict[str, Any], soil_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate expert agricultural analysis based on weather and soil data.
    """
    if not AI_AVAILABLE or not os.environ.get("OPENAI_API_KEY"):
        return {
            "suggested_crops": ["Wheat", "Rice", "Maize"],
            "soil_analysis": "AI Analysis unavailable (Check API Key or Depedencies). Soil structure appears stable.",
            "action_plan": [
                "Ensure proper drainage",
                "Monitor soil moisture daily",
                "Apply organic compost if possible"
            ]
        }

    try:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")

        # Use a simple prompt for robust JSON parsing
        json_prompt = ChatPromptTemplate.from_template(
            """
            You are an expert Agronomist AI. Analyze the following environmental data:
            
            Weather: {weather_data}
            Soil: {soil_data}
            
            Return a valid JSON object with the following keys:
            - suggested_crops: list of strings (3-5 crops)
            - soil_analysis: string (1 sentence)
            - action_plan: list of strings (3 bullet points)
            
            Do not include markdown formatting like ```json. Just the raw JSON.
            """
        )
        
        chain = json_prompt | llm
        result = chain.invoke({"weather_data": str(weather_data), "soil_data": str(soil_data)})
        
        import json
        clean_content = result.content.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_content)
        
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "suggested_crops": ["Maize", "Sorghum", "Millet"],
            "soil_analysis": "Could not generate analysis due to runtime error. Defaulting to drought-resistant crops.",
            "action_plan": ["Check water sources", "Monitor temperature"]
        }

def get_chat_response(messages: List[Dict[str, str]], context: Dict[str, Any]) -> str:
    """
    Get a response from the AI Chatbot.
    """
    if not AI_AVAILABLE or not os.environ.get("OPENAI_API_KEY"):
        return "I am currently running in offline mode. Please check your OpenAI API Key and dependencies to enable AI features."

    try:
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")
        
        system_text = f"""
        You are an AI Agricultural Advisor. You are helping a farmer who has the following conditions:
        
        Current Crop: {context.get('crop_type', 'Unknown')}
        Soil Type: {context.get('soil_type', 'Unknown')}
        pH Level: {context.get('ph_level', 'Unknown')}
        Weather Alert: {context.get('weather_alert', 'None')}
        
        Provide helpful, concise, and scientifically accurate farming advice.
        """
        
        langchain_messages = [SystemMessage(content=system_text)]
        
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
                
        response = llm.invoke(langchain_messages)
        return response.content
        
    except Exception as e:
        return f"I encountered an error while thinking: {str(e)}"
