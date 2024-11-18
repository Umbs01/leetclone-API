import subprocess
from ..config import get_settings

# def run_code(text, *args):
#     # Write code to file 'script.py'
#     with open('script.py', 'w') as f:
#         f.write(text)

#     # Initialize isolate & move script.py to the isolate directory
#     try:
#         subprocess.run(['sudo', 'isolate', '--init'], check=True)
#         subprocess.run(['sudo', 'mv', 'script.py', f'{get_settings().SANDBOX_PATH}/0/box'], check=True)

#         # Run the script with memory and time limits
#         result = subprocess.run(['sudo', 'isolate', '--box-id=0', '--mem=102400', '--time=3', '--run', '--', '/usr/bin/python3', 'script.py', *args ],
#                                 check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         output = result.stdout.decode('utf-8')
#         errors = result.stderr.decode('utf-8')

#         try:
#             # Write output to file 'output.txt'
#             result = subprocess.run(['sudo', 'tee', f'{get_settings().SANDBOX_PATH}/output.txt'], input=output.encode('utf-8'),
#                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#             stderr = result.stderr.decode('utf-8') # errors

#             if stderr:
#                 raise Exception(f"Error writing output: {stderr}")
            
#         except Exception as e:
#             raise Exception(f"Error writing output: {e}")

#         # if code cannot be interpreted, write the error to 'output.txt'
#         if errors:
#             subprocess.run(['sudo', 'tee', f'{get_settings().SANDBOX_PATH}/output.txt'], input=errors.encode('utf-8'),
#                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             raise subprocess.CalledProcessError(1, 'isolate', output=errors)
    
#     except subprocess.CalledProcessError as e:
#         print(f"Error running code: {e}")
        

def run_code(text, *args):
    # Write code to file 'script.py'
    with open('script.py', 'w') as f:
        f.write(text)

    # Initialize isolate & move script.py to the isolate directory
    try:
        subprocess.run(['sudo', 'isolate', '--init'], check=True)
        subprocess.run(['sudo', 'mv', 'script.py', f'{get_settings().SANDBOX_PATH}/0/box'], check=True)

        # Run the Python script with memory and time limits, capturing only Python script output
        result = subprocess.run(
            ['sudo', 'isolate', '--box-id=0', '--mem=102400', '--time=3', '--run', '--', '/usr/bin/python3', 'script.py', *args],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = result.stdout.decode('utf-8') 
        errors = result.stderr.decode('utf-8')  

        try:
            with open(f'{get_settings().SANDBOX_PATH}/output.txt', 'w') as output_file:
                output_file.write(output)  # Write only the Python script's output

        except Exception as e:
            raise Exception(f"Error writing output: {e}")

        # If there are Python script errors, raise an error and write it to 'output.txt'
        if errors:
            with open(f'{get_settings().SANDBOX_PATH}/output.txt', 'w') as output_file:
                output_file.write(errors)  # Append stderr to the output file
            raise subprocess.CalledProcessError(1, 'isolate', output=errors)

    except subprocess.CalledProcessError as e:
        print(f"Error running code: {e}")


def read_output():
    try:
        result = subprocess.run(
            ['sudo', '/bin/cat', f'{get_settings().SANDBOX_PATH}/output.txt'], 
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


def combine_code(template, code) -> str:
    return template + '\n' + code + '\n\nif __name__ == \"__main__\":\n    main()\n'

# input = "1 2 3 4 5" called to run_code(code, 1, 2, 3, 4, 5)
def parsing_input(input: str) -> list:
    return input.split(' ')

def handle_run_code(code: str, test_cases: list[dict]) -> list:
    results = []
    if test_cases == []:
        run_code(code)
        output = read_output()
        results.append(output)
        return results
    
    for test_case in test_cases:
        inputs = parsing_input((test_case['input']))
        run_code(code, *inputs)
        output = read_output()
        results.append(output)
    return results