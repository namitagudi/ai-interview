import asyncio
import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama3")

def generate_target_question(resume: str, jd: str, difficulty: int, asked_questions: list) -> str:
    """Generates unique technical questions dynamically using Llama 3."""
    prompt = PromptTemplate(
        input_variables=["resume", "jd", "difficulty", "asked"],
        template="""
        You are a technical interviewer. Generate ONE technical question based on:
        Job Description: {jd}
        Resume: {resume}
        Difficulty Level (1-5): {difficulty}
        
        Do NOT ask any of these previously asked questions: {asked}
        Return ONLY the question text. Do not add intro/outro text.
        """
    )
    chain = prompt | llm
    return chain.invoke({
        "resume": resume,
        "jd": jd,
        "difficulty": difficulty,
        "asked": asked_questions
    }).strip()

async def eval_technical(transcript: str, jd: str):
    prompt = f"Evaluate technical correctness (0-10) for answer: '{transcript}' against JD: '{jd}'. Format output strictly as JSON with keys 'score' (float) and 'feedback' (string)."
    res = await asyncio.to_thread(llm.invoke, prompt)
    return res

async def eval_communication(transcript: str, wpm: float):
    prompt = f"Evaluate STAR structure and clarity (0-10) for answer: '{transcript}' spoken at {wpm} WPM. Format output strictly as JSON with keys 'score' (float) and 'feedback' (string)."
    res = await asyncio.to_thread(llm.invoke, prompt)
    return res

async def eval_verifier(transcript: str, resume: str):
    prompt = f"Cross-verify claims (0-10) between transcript: '{transcript}' and resume: '{resume}'. Format output strictly as JSON with keys 'score' (float) and 'feedback' (string)."
    res = await asyncio.to_thread(llm.invoke, prompt)
    return res

async def run_parallel_evaluations(transcript: str, jd: str, resume: str, wpm: float):
    """Executes 3 automated evaluation agents asynchronously in parallel."""
    results = await asyncio.gather(
        eval_technical(transcript, jd),
        eval_communication(transcript, wpm),
        eval_verifier(transcript, resume)
    )
    
    # Perfected phrase remediation synthesis
    remediation_prompt = f"Rewrite this interview answer in ideal STAR format with strong technical terms: '{transcript}'"
    perfected_phrase = await asyncio.to_thread(llm.invoke, remediation_prompt)
    
    return {
        "raw_results": results,
        "perfected_phrase": perfected_phrase.strip()
    }
