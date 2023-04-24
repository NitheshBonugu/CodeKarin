import { useState, useEffect } from "react";
//import parse from 'html-react-parser';
import Card from "../layout/Card";
import classes from "./CodeForm.module.css";
import { updateCode, getCodeResult } from "../../services/CodeService";
import { getProblem } from "../../services/ProblemService";

function CodeForm() {
  const [result, setResult] = useState(null);
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));
  const [contest_data, set_contest_data] = useState(null);

  var code = "loading in progress";
  var problem_id = "loading in progress";
  var description = "loading in progress";
  var res = "Console";

  const parameters = {
    user: localStorage.getItem("USER"),
    class_id: localStorage.getItem("CLASSROOM"),
    problem_id: localStorage.getItem("PROBLEM_ID"),
    access_token: localStorage.getItem("ACCESS_TOKEN")
  };

  useEffect(() => {
    getProblem(parameters).then((data) => set_contest_data(data));
  }, []);

  if (contest_data !== null) {
    let element = contest_data["problem_get_response"];

    if (contest_data["problem_name"] === parameters["problem_id"]) {
      code = String(element["boilerplate"]);
      problem_id = String(contest_data["problem_name"]);
      description = JSON.parse(JSON.stringify(element["description"]["description"]));
    }
  }

  if (result !== null) {
    res = result;
  }

  var data = {
    code: code,
    prob_name: problem_id,
    description: description,
    result: res,
  };
  return Render(data);

  async function SubmitHandler(event) {
    event.preventDefault();
    document.getElementById("submit_button").disabled = true;
    var element = document.getElementById("code").textContent;
    var enteredCode = String(element);

    const params = {
      user: localStorage.getItem("USER"),
      problem_id: localStorage.getItem("PROBLEM_ID"),
      class_id: localStorage.getItem("CLASSROOM"),
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      entered_code: enteredCode,
    };
    var rs = null;
    var loopFlag = false;
    rs = await updateCode(params).then(loopFlag = true);

    while (loopFlag) {
      console.log(rs);
      if("status" in rs){
          if (rs["status"].includes("COMPLETE", 0) || rs["status"].includes("READ", 0)) {
            setResult("Build complete, test results: " + rs["body"]);
            document.getElementById("submit_button").disabled = false;
            loopFlag = false;
            break;
          } else if (rs["status"].includes("IN_PROGRESS", 0)) {
            setResult("Build in progress, test results loading...");
            rs = await getCodeResult(params);
          }
      }else {
        setResult("Build not started, internal server error... check your internet connecion and contact your instructor");
      }
      await delay(15000);
    }

    data["result"] = result;
    return Render(data);
  }

  function Render(data) {
    var code = data["code"];
    var result = data["result"];
    return (
      <Card>
        <div className={classes.problem}> {data["prob_name"]} <br /> <br /> {data["description"]} </div>
        <form className={classes.form} onSubmit={SubmitHandler}>
          <div className={classes.coding}>
            <label htmlFor="code">Code</label>
            <div id="code" className={classes.textarea} required rows="20" contenteditable="true"> <pre>{code}</pre> </div>
          </div>
          <div className={classes.actions}>
            <button id="submit_button" type="submit" onclick={SubmitHandler}>
              Run
            </button>
          </div>
        </form>
        <div id="console" className={classes.console}>
          <pre>{result}</pre>
        </div>
      </Card>
    );
  }
}
export default CodeForm;
