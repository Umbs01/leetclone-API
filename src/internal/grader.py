def trim(code: str) -> str:
    code = code.replace('\n', '') # removes newlines
    # removes leading and trailing whitespaces
    return code.strip()

def check_output(outputs: list[str], testcases: list[dict[str,str]]): # will do this after finals
    results = []
    for output, testcase in zip(outputs, testcases):
        output = trim(output)
        if output == testcase['output']:
            results.append(True)
        else:
            results.append(False)
    results = zip(testcases, results)
    return results 

def isAccepted(results: list) -> bool:
    # check if all test cases passed (all True)
    for _, result in results:
        if not result:
            return False

    return True