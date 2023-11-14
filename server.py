from flask import Flask, render_template, redirect
from sqlalchemy import create_engine
from test_analytics.models import Base, TestResults
from sqlalchemy.orm import sessionmaker
from test_analytics.utils import get_test_key
from datetime import datetime
from flask import request
import xmltodict


app = Flask(__name__)

engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route("/<project>")
def index(project):
    results = {}
    tests = session.query(TestResults).filter(TestResults.project == project).all()

    for t in tests:
        key = get_test_key(t)
        if not results.get(key):
            results[key] = {
                "test_file_name": t.test_file_name,
                "test_name": t.test_name,
                "trends": []
            }

        trend = {
            "duration": t.duration,
            "test_run_id": datetime.fromtimestamp(t.test_run_id),
            "test_result": t.test_result,
        }
        results[key]["trends"].append(trend)
    return render_template("index.html", project=project, results=results)



@app.route("/upload/<project>", methods=["POST"])
def upload(project):
    reportfile = request.get_data()
    reportfile_xml = xmltodict.parse(reportfile)
    timestmp = datetime.now().timestamp()
    print(timestmp)
    for test in reportfile_xml["testsuites"]["testsuite"]["testcase"]:
        result = "success"
        reason = ""
        if test.get("failure"):
            result = "failure"
            reason = test["failure"]["#text"]

        t = TestResults(
            project=project,
            test_run_id=timestmp,
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
            return "Error"
    return "OK"



if __name__ == "__main__":
    app.run(debug=True)
