from pydantic import BaseModel

class Result(BaseModel):
    testcases: list[dict[str,str]]
    results: list[bool] 

def trim(code: str) -> str:
    code = code.replace('\n', '') # removes newlines
    # removes leading and trailing whitespaces
    return code.strip()

def check_output(outputs: list[str], testcases: list[dict[str,str]]): # will do this after finals
    summary = Result(testcases=testcases, results=[])
    results = []
    for output, testcase in zip(outputs, testcases):
        output = trim(output)
        if output == testcase['output']:
            results.append(True)
        else:
            results.append(False)
    summary.results = results
    return summary

def isAccepted(results: list) -> bool:
    # check if all test cases passed (all True)
    for _, result in results:
        if not result:
            return False

    return True