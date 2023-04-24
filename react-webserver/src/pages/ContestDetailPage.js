import QuestionList from "../components/problems/QuestionList";
import { useState, useEffect } from "react";
import { getProblemList } from "../services/ProblemService.js";
import classes from "../components/problems/ProblemItem.module.css";
import { useHistory } from "react-router-dom";

function ContestQuestionPage() {
  const [problem_data, set_problem_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      class_id: localStorage.getItem("CLASSROOM"),
      problem_set: localStorage.getItem("PROBLEM_SET"),
      id_token: localStorage.getItem("ID_TOKEN"),
      access_token: localStorage.getItem("ACCESS_TOKEN")
    };
    getProblemList(parameters).then((data) => set_problem_data(data));
  }, []);

  if (problem_data === null) {
    return <h2>Loading contest problems...</h2>;
  }
  return Render(problem_data);
}

function Render(problem_data) {
  const history = useHistory();
  
  function clickHandler() {
    localStorage.setItem("CONTEST_REPORT", "1");
    history.push("/contest-report");
  }
  return (
    <section>
      <QuestionList questions={problem_data} />
      <div className={classes.actions}>
        <button onClick={clickHandler}>Rank Report</button>
      </div>
    </section>
  );
}
export default ContestQuestionPage;