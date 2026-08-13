from state import State
from security import CommandExecutor
from agents import planner_agent, coder_agent, debugger_agent

def main():
    task = input("Enter your task (or press Enter for a sample task): ") or "Create a simple Python function to calculate the factorial of a number"
    
    state = State(task=task)
    
    # Run Planner Agent
    state = planner_agent(state)
    
    # Run Coder Agent
    state = coder_agent(state)
    
    # Save current code to a temporary script file
    with open('generated_app.py', 'w') as f:
        f.write(state.current_code)
    
    # Execute the generated code safely
    result = CommandExecutor.execute('python generated_app.py')
    
    if result['returncode'] != 0:
        state.test_results = {
            'stdout': result['stdout'],
            'stderr': result['stderr']
        }
        
        for _ in range(3):
            state = debugger_agent(state)
            
            # Re-execute the code
            result = CommandExecutor.execute('python generated_app.py')
            
            if result['returncode'] == 0:
                break
    
    print(f"Final State Status: {state.status}")
    print("Generated Code:")
    print(state.current_code)
    print("Execution Output:")
    print(result['stdout'])
    print(result['stderr'])

if __name__ == "__main__":
    main()
