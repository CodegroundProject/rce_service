from json import loads, dumps


def parse_pytest_report(report):
    """
        Output format:
            {
                "test_results":[
                    {
                        "test_id": "",
                        "status": "passed",
                        "message": "optional message"
                    },
                    {
                        "test_id": "",
                        "status": "failed",
                        "message": "optional message"
                    },
                ],
                "status": "failed"
            }
    """
    pytest_report = loads(report)
    output = {}
    tests = pytest_report["tests"]
    output["test_results"] = []
    for test in tests:
        output["test_results"].append({
            "test_id": test["nodeid"].split("::")[1].split("_")[1],
            "status": test["outcome"],
            "message": ""
        })
    if pytest_report["summary"]["failed"] > 0:

        output["status"] = "failed"
    else:
        output["status"] = "passed"

    return dumps(output)


def parse_jest_report(report):
    """
        Output format:
            {
                "test_results":[
                    {
                        "test_id": "",
                        "status": "passed",
                        "message": "optional message"
                    },
                    {
                        "test_id": "",
                        "status": "failed",
                        "message": "optional message"
                    },
                ],
                "status": "failed"
            }
    """
    json_report = loads(report)
    output = {}
    # output["success"] = json_report["success"]
    output["test_results"] = []
    assertions = json_report["testResults"][0]["assertionResults"]
    for assertion_result in assertions:
        output["test_results"].append({
            "test_id": assertion_result["title"],
            "status": assertion_result["status"],
            "message": ""
        })
    output["status"] = json_report["testResults"][0]["status"]
    return dumps(output)
