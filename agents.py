import re

from ollama_api import call_ollama

def clean_code_response(text: str) -> str:
    # Remove Markdown code blocks using regex
    code_block_pattern = r'```(?:python)?\s*(.*?)\s*```'
    match = re.search(code_block_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Strip leading/trailing backticks and whitespace
    return text.strip('`').strip()

def planner_agent(state):
    print('[+] Running Planner Agent (qwen2.5:3b)...')
    prompt = f"Task: {state.task}\n\nPlease provide a clear step-by-step action plan for this task."
    state.plan = call_ollama(prompt, model='qwen2.5:3b').split('\n')
    print('[+] Planner Agent completed.')
    return state

def coder_agent(state):
    system_instructions = """
    You are an expert Python developer.
    Your responses should be concise and only include valid Python code.
    Do not include any conversational fluff or explanations.
    """
    prompt = f"System Instructions:\n{system_instructions}\n\nCurrent Code:\n{state.current_code}\n\nAction Plan:\n{'\n'.join(state.plan)}\n\nPlease generate the next step of code based on the action plan."
    response = call_ollama(prompt, model='qwen2.5-coder:3b')
    state.current_code += clean_code_response(response)
    print('[+] Coder Agent completed.')
    return state

def debugger_agent(state):
    system_instructions = """
    You are an expert Python developer.
    Your responses should be concise and only include valid Python code.
    Do not include any conversational fluff or explanations.
    """
    prompt = f"System Instructions:\n{system_instructions}\n\nCurrent Code:\n{state.current_code}\n\nTest Results:\n{state.test_results['stderr']}\n\nPlease analyze the test results and provide the corrected code."
    response = call_ollama(prompt, model='qwen2.5-coder:3b')
    state.current_code = clean_code_response(response)
    print('[+] Debugger Agent completed.')
    return state
