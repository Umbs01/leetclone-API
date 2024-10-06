import subprocess
from ..config import get_settings

def run_code(text):
    # Write code to file 'script.py'
    with open('script.py', 'w') as f:
        f.write(text)

    # Initialize isolate & move script.py to the isolate directory
    try:
        subprocess.run(['sudo', 'isolate', '--init'], check=True)
        subprocess.run(['sudo', 'mv', 'script.py', f'{get_settings().SANDBOX_PATH}/box'], check=True)

        # Run the script with memory and time limits
        result = subprocess.run(['sudo', 'isolate', '--box-id=0', '--mem=102400', '--time=3', '--run', '--', '/usr/bin/python3', 'script.py'],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = result.stdout.decode('utf-8')
        errors = result.stderr.decode('utf-8')

        try:
            command = f"echo '{output}' | sudo tee {get_settings().SANDBOX_PATH}/output.txt"
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            stdout = result.stdout.decode('utf-8') # output
            stderr = result.stderr.decode('utf-8') # errors

            if stderr:
                raise Exception(f"Error writing output: {stderr}")
            
        except Exception as e:
            print(e)

        if errors:
            raise subprocess.CalledProcessError(1, 'isolate', output=errors)

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

def read_output():
    try:
        result = subprocess.run(
            ['sudo', 'cat', f'{get_settings().SANDBOX_PATH}/output.txt'], 
            stdout=subprocess.PIPE,  # output
            stderr=subprocess.PIPE   # errors
        )

        output = result.stdout.decode('utf-8')
        errors = result.stderr.decode('utf-8')
        
        if errors:
            raise Exception(f"Error reading output: {errors}")

        return output

    except Exception as e:
        return str(e)
