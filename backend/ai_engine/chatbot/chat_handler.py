from ai_engine.context_engine.context_builder import build_context
from ai_engine.context_engine.prompt_builder import build_rag_prompt
from ai_engine.memory.memory_store import add_user_memory
from ai_engine.llm.groq_client import generate_chat_completion
import logging

logger = logging.getLogger(__name__)

def handle_chat(job_id: str, user_id: str, question: str, current_slide: int, mode: str = "doubt"):
    """
    Central Nervous System routing explicitly constructed structured prompts natively onto LLM engines.
    """
    logger.info(f"Chat request - Mode: '{mode}' - Slide/Turn: {current_slide} - Job {job_id}")
    
    # 1. Synthesize explicit Data Structure spanning Vectors, Strings, and Logs
    context = build_context(job_id, user_id, current_slide, question, mode)
    
    # 2. Stringify strict constraint prompt guarding completely against Hallucination
    user_prompt = build_rag_prompt(context, question)
    system_prompt = "You are an advanced Context-Aware AI pedagogical assistant locally scoped entirely to strict textual constraints."
    
    # 3. Call standard Groq LLM cascade natively (General Text logic formatting bypassing Object limits securely)
    answer = generate_chat_completion(system_prompt, user_prompt, temperature=0.2)
    
    # 4. Save sequence actively natively creating local User Memory array logs linearly over session
    add_user_memory(job_id, user_id, question, answer)
    
    return {
        "answer": answer,
        "source_chunks": context["relevant_chunks"]
    }
