import { useState, useEffect } from "react";
import ProblemList from "../components/problems/ProblemList";
import { getProblemSet } from "../services/ProblemService.js";

function PracticePage() {
  const [practice_data, set_practice_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      class_id: localStorage.getItem("CLASSROOM"),
      set_type: "practice",
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      id_token: localStorage.getItem("ID_TOKEN")
    };
    getProblemSet(parameters).then((data) => set_practice_data(data));
  }, []);

  if (practice_data === null) {
    return <h2>Loading practice problems...</h2>;
  }
  return Render(practice_data);
}

function Render(practice_data) {
  return (
    <section>
      <ProblemList problems={practice_data} />
    </section>
  );
}
export default PracticePage;
