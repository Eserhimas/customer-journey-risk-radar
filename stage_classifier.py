import yaml
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from typing import Optional
from crewai import Agent
from langchain_community.chat_models import ChatOpenAI
import os
import json

load_dotenv()

# load the YAML file
with open("tasks.yaml", "r") as file:
    stage_config = yaml.safe_load(file)["tasks"]
    
# OpenRouter
class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: Optional[str] = None,
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)
        
# free deepseek model
llm = ChatOpenRouter(model_name="deepseek/deepseek-chat-v3-0324:free")

def generate_stage_prompt(post_text: str, yaml_path: str = "tasks.yaml") -> str:
    with open(yaml_path, "r", encoding="utf-8") as file:
        task_data = yaml.safe_load(file)["tasks"]

    stage_blocks = ""
    for task in task_data:
        examples = "\n    - ".join(task["examples"])
        stage_blocks += f"\n\n### {task['stage']}\n{task['description']}\n    - {examples}"

    prompt = f"""
You are a customer experience analyst specializing in OTT platforms.

Below is a Reddit post followed by possible customer journey stages. Classify the post into the most relevant stage. Respond with only the stage name.

Reddit Post:
\"\"\"{post_text}\"\"\"

Stages:
{stage_blocks}

Your answer:"""
    return prompt

# classification function
def classify_post(post_text: str) -> str:
    prompt = generate_stage_prompt(post_text) 
    messages = [{"role": "user", "content": prompt}]
    try:
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown"
    
# json classification
def classify_json_file(json_path: str, output_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        reddit_data = json.load(f)

    classified = []
    for post in reddit_data:
        content = f"{post.get('title', '')}\n\n{post.get('selftext', '')}".strip()
        if content:
            stage = classify_post(content)
            post["journey_stage"] = stage
            print(f"[{stage}] → {post['title'][:80]}")
        classified.append(post)

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(classified, out, indent=2, ensure_ascii=False)
        
# testing single post
'''if __name__ == "__main__":
    test_text = "I signed up last night but still haven’t received the confirmation email. Anyone else?"
    result = classify_post(test_text)
    print("Predicted stage:", result)'''

# classifying the reddit data  
classify_json_file("reddit_data_20250613_150351.json", "classified_reddit.json")
