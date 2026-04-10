import json

def build_rag_prompt(context: dict, question: str) -> str:
    """Synthesizes explicit boundary instructions routing behavior strictly upon user constraints explicitly natively"""
    mode = context.get("mode", "doubt")
    
    system_base = """You are AI Guruji, an expert AI teacher.

CRITICAL RULES:
- Answer ONLY starting from the provided context chunks.
- Do NOT hallucinate or utilize external generalized knowledge securely outside the constraints natively.
- If the exact answer truly cannot be reasonably derived strictly from the text, state exactly:
  "This is not directly covered in the current lecture material."
"""

    if mode == "quiz":
        system_base += "- Generate a short MCQ strictly based exclusively on the detailed context provided.\n"
    elif mode == "explain_simple":
        system_base += "- Analyze the technical chunks but rewrite the response using extremely simple, beginner-friendly analogies. Do NOT add missing facts, just simplify existing ones.\n"
    elif mode == "summarize":
        system_base += "- Provide a meticulously structured high-level outline summary capturing critical elements natively.\n"
    
    # Safely dump nested dictionary elements gracefully avoiding crash bugs
    chunks_text = json.dumps(context.get("relevant_chunks", []), indent=2)
    slide_text = json.dumps(context.get("current_slide_data", {}), indent=2)
    
    history_arr = []
    for h in context.get("history", []):
         history_arr.append(f"User: {h.get('question')}\nGuruji: {h.get('answer')}")
    history_text = "\n\n".join(history_arr)
    
    prompt = f"""{system_base}

=== Recent Chat History Context ===
{history_text if history_text else "No prior history in this session."}

=== Currently Focused Slide / Timestamp Node ===
{slide_text}

=== Retrieved Fact Vector Grounding ===
{chunks_text}

=== Student Request / Question ===
{question}
"""
    return prompt
