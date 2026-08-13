from ollama_api import call_ollama

def planner_agent(state):
    prompt = f"Task: {state.task}\n\nPlease provide a clear step-by-step action plan for this task."
    state.plan = call_ollama(prompt, model='qwen2.5:3b').split('\n')
    return state

def coder_agent(state):
    system_instructions = """
    You are an expert Python developer.
    Your responses should be concise and only include valid Python code.
    Do not include any conversational fluff or explanations.
    """
    prompt = f"System Instructions:\n{system_instructions}\n\nCurrent Code:\n{state.current_code}\n\nAction Plan:\n{'\n'.join(state.plan)}\n\nPlease generate the next step of code based on the action plan."
    state.current_code += call_ollama(prompt, model='qwen2.5-coder:7b')
    return state

def debugger_agent(state):
    system_instructions = """
    You are an expert Python developer.
    Your responses should be concise and only include valid Python code.
    Do not include any conversational fluff or explanations.
    """
    prompt = f"System Instructions:\n{system_instructions}\n\nCurrent Code:\n{state.current_code}\n\nTest Results:\n{state.test_results['stderr']}\n\nPlease analyze the test results and provide the corrected code."
    state.current_code = call_ollama(prompt, model='qwen2.5-coder:7b')
    return state
