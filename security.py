import subprocess
import shlex

class CommandExecutor:
    ALLOWLIST = ['python', 'pytest', 'git']

    @staticmethod
    def is_allowed(command):
        args = shlex.split(command)
        if any(op in command for op in ('&&', ';', '|', '||', '>', '<')):
            raise ValueError("Command chaining operators are not allowed")
        return args[0] in CommandExecutor.ALLOWLIST

    @staticmethod
    def execute(command, timeout=30):
        if not CommandExecutor.is_allowed(command):
            raise ValueError("Command not allowed")

        try:
            result = subprocess.run(
                command,
                shell=False,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }

# Example usage:
# result = CommandExecutor.execute('python script.py')
# print(result)
