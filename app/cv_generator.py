from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

from app.prompts import CV_OPTIMIZATION_PROMPT


def generate_cv(cv_text: str, job_text: str):
    llm = Ollama(model="llama3")

    prompt = PromptTemplate(
        template=CV_OPTIMIZATION_PROMPT,
        input_variables=["cv", "job"]
    )

    chain = prompt | llm

    result = chain.invoke({
        "cv": cv_text,
        "job": job_text
    })

    return result