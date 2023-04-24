import classes from "./ProblemItem.module.css";
import ProblemCard from "../layout/ProblemCard";
import { useHistory } from "react-router-dom";

function QuestionItem(props) {
  const history = useHistory();
  function clickHandler() {
    history.push("/code");
    localStorage.setItem("PROBLEM_ID", props.title);
  }
  return (
    <li className={classes.item} onClick={clickHandler}>
      <ProblemCard>
        <div className={classes.content}>
          <h3>{props.title}</h3>
        </div>
        <div className={classes.content}>
          <h6>Description: {props.description}</h6>
        </div>
      </ProblemCard>
    </li>
  );
}
export default QuestionItem;