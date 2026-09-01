import json
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

def generate_remediation_quiz(transcript: str, perfected_phrase: str) -> dict:
    """
    Asks Llama 3 to generate a 1-question multiple-choice quiz based on the 
    structural improvement made in the perfected phrase.
    Returns a dictionary with the question, options, and correct index.
    """
    prompt = f"""
    You are an interview coach. 
    Original candidate answer: "{transcript}"
    Perfected answer: "{perfected_phrase}"

    Generate ONE multiple choice quiz question testing what structural or technical improvement was made.
    Return STRICTLY valid JSON with no extra text or markdown code blocks:
    {{
      "question": "What is the primary technical improvement made in the perfected phrase?",
      "options": [
        "Added concrete technical details and STAR methodology structure",
        "Made the response shorter and removed context",
        "Used filler words to increase word count"
      ],
      "correct_index": 0
    }}
    """
    
    try:
        response_text = llm.invoke(prompt).strip()
        # Clean potential markdown formatting from LLM output
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        quiz_data = json.loads(response_text)
        return quiz_data
    except Exception:
        # Robust fallback quiz if JSON parsing fails from local LLM
        return {
            "question": "What key structural improvement was highlighted in the perfected response?",
            "options": [
                "Integrated precise technical terms and structured STAR logic",
                "Removed all technical depth to keep it vague",
                "Reduced speech clarity and speed"
            ],
            "correct_index": 0
        }
