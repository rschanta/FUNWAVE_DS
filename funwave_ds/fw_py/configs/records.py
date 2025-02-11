import inspect
import functools

# Dictionary to store the logs of function calls
function_logs = {}

def log_function_call(func):

    """Decorator to record function calls for the pipeline"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Call the function and store the result
        result = func(*args, **kwargs)
        
        # Log the function name, arguments, and result
        function_name = func.__name__
        function_code = inspect.getsource(func)
        
        # Save the details in a dictionary
        function_logs[function_name] = {
            'code': function_code
        }
        
        return result
    return wrapper


def save_logs_to_file(filename="function_log.py"):
    """Save function logs to a text file."""
    with open(filename, "w") as f:
        for func_name, details in function_logs.items():
            f.write(f"# Function: {func_name}\n")
            f.write("# Code:\n")
            f.write(details['code'] + "\n")
            f.write("#" + "-" * 40 + "\n")