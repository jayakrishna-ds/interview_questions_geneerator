from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def generate_followups(skill,question):
    """
    Returns:
    {
        "answer_points":list[str],
        "followups":list[str]
    }
    """
    try:
        response=client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role":"system",
                    "content":"Respond ONLY in valid JSON. No markdown. No explanation."
                },
                {
                    "role":"user",
                    "content":f"""
                        skill:{skill}
                        question:{question}
                    
                    Return JSON exactly like:{{
                        "answer_points": ["point 1", "point 2", "point 3"],
                        "followups": ["followup 1", "followup 2", "followup 3"]
                        }}
                    """
                }
            ],
            temperature=0.4
        )

        content=response.output_text.strip()
        data=json.loads(content)

        return {
            "answer_points":data.get("answer_points",[]),
            "followups":data.get("followups",[])
        }

    except Exception as e:
        return {
            "answer_points":[f"LLM Error: {e}"],
            "followups":[]
        }
