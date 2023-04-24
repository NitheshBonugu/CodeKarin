import QuestionList from "../components/problems/QuestionList";
import { useState, useEffect } from 'react';
import { getProblemList } from "../services/ProblemService.js";

function PracticeQuestionPage() {

  const [problem_data, set_problem_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      class_id: localStorage.getItem("CLASSROOM"),
      problem_set: localStorage.getItem("PROBLEM_SET"),
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      id_token: localStorage.getItem("ID_TOKEN")
    }
    getProblemList(parameters).then(data => set_problem_data(data));
  }, []);

  if(problem_data === null){
    return <h2>Loading problem...</h2>;
  }
  return Render(problem_data);
}

function Render(problem_data){
  return (
    <section>
      <QuestionList questions={problem_data} />
    </section>
  );
}
export default PracticeQuestionPage;
