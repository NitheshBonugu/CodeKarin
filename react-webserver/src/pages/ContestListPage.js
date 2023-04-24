import { useState, useEffect } from "react";
import ContestList from "../components/problems/ContestList";
import { getProblemSet } from "../services/ProblemService.js";

function ContestPage() {
  const [contest_data, set_contest_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      class_id: localStorage.getItem("CLASSROOM"),
      set_type: "contest",
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      id_token: localStorage.getItem("ID_TOKEN")
    };
    getProblemSet(parameters).then((data) => set_contest_data(data));
  }, []);

  if (contest_data === null) {
    return <h2>Loading contests...</h2>;
  }
  return Render(contest_data);
}

function Render(contest_data) {
  return (
    <section>
      <ContestList contests={contest_data} />
    </section>
  );
}
export default ContestPage;