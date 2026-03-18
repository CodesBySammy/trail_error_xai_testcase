import os
import subprocess
import sys

def execute_user_command(user_provided_string):
    """
    Very dangerous function that blindly executes user input.
    CodeBERT and AST Engine will both flag this heavily.
    """
    # 1. AST Engine Check: Unsafe OS system call
    os.system(f"echo {user_provided_string}")
    
    # 2. AST Engine Check: Unsafe Subprocess with shell=True
    subprocess.Popen(f"ls -la {user_provided_string}", shell=True)
    
    # 3. AST Engine Check: Dangerous built-in eval/exec
    command_to_run = f"print('{user_provided_string}')"
    eval(command_to_run)
    exec(command_to_run)

# Pad the file to increase churn and trigger the "High Churn" risk marker
def filler_function_1(): pass
def filler_function_2(): pass
def filler_function_3(): pass
def filler_function_4(): pass
# ... imagine 60 more lines of code here to make it > 50 lines changed ...
