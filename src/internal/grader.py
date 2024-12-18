from pydantic import BaseModel

class Result(BaseModel):
    testcases: list[dict[str,str]]
    results: list[bool] 

def trim(code: str) -> str:
    code = code.replace('\n', '') # removes newlines
    # removes leading and trailing whitespaces
    return code.strip()

def mutate_to_string(testcases: list[dict]) -> list[dict[str,str]]:
    for testcase in testcases:
        testcase['input'] = str(testcase['input'])
        testcase['output'] = str(testcase['output'])
    return testcases

def check_output(outputs: list[str], testcases: list[dict[str,str]]):
    summary = Result(testcases=testcases, results=[])
    results = []
    for output, testcase in zip(outputs, testcases):
        output = output.split('\n')[0] # get the first line of the output (which is usually the answer)
        output = trim(output)
        if output == testcase['output']:
            results.append(True)
        else:
            results.append(False)
    summary.results = results
    return results

def isAccepted(results: list) -> bool:
    # check if all test cases passed (all True)
    for result in results:
        if not result:
            return False

    return True
