import subprocess
from ..config import get_settings

def run_code(text):
    # Write code to file 'script.py'
    with open('script.py', 'w') as f:
        f.write(text)

    # Initialize isolate & move script.py to the isolate directory
    try:
        subprocess.run(['isolate', '--init'], check=True)
        subprocess.run(['sudo', 'mv', 'script.py', f'{get_settings().SANDBOX_PATH}/box'], check=True)

        # Run the script with memory and time limits
        result = subprocess.run(['sudo', 'isolate', '--box-id=0', '--mem=102400', '--time=3', '--run', '--', '/usr/bin/python3', f'{get_settings().SANDBOX_PATH}/box/script.py'],
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Capture output and errors
        output = result.stdout.decode('utf-8')
        errors = result.stderr.decode('utf-8')

        with open(f'{get_settings().SANDBOX_PATH}/output.txt', 'w') as f:
            f.write(output)

        if errors:
            raise subprocess.CalledProcessError(1, 'isolate', output=errors)

    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

def read_output():
    with open(f'{get_settings().SANDBOX_PATH}/output.txt', 'r') as f:
        return f.read()
