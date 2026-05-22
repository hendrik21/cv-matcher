from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

from app.prompts import MATCH_PROMPT

def get_llm():
    return Ollama(model="qwen2.5:7b")

def evaluate_match(cv_text: str, job_text: str):
    llm = get_llm()

    prompt = PromptTemplate(
        template=MATCH_PROMPT,
        input_variables=["cv", "job"]
    )

    chain = prompt | llm

    result = chain.invoke({
        "cv": cv_text,
        "job": job_text
    })

    return result