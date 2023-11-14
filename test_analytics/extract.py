import xmltodict
from .models import TestResults
from sqlalchemy.orm import sessionmaker
from datetime import datetime


def extract(project: str, reportfile: str, session: sessionmaker):
    reportfile_xml = xmltodict.parse(reportfile)
    t = datetime.now().timestamp()
    print(t)
    # print(reportfile_xml)
    for test in reportfile_xml["testsuites"]["testsuite"]["testcase"]:
        result = "success"
        reason = ""
        if test.get("failure"):
            result = "failure"
            reason = test["failure"]["#text"]

        t = TestResults(
            project=project,
            test_run_id=t,
            test_name=test["@name"],
            test_file_name=test["@classname"],
            test_result=result,
            duration=test["@time"],
            reason=reason
        )
        try:
            session.add(t)
            session.commit()
        except Exception as e:
            print(f"Exception in SQL: {e}")
            session.rollback()
