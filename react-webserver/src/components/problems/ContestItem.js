import classes from "./ProblemItem.module.css";
import ProblemCard from "../layout/ProblemCard";
import { useHistory } from "react-router-dom";

function ContestItem(props) {
  const history = useHistory();
  function clickHandler() {
    history.push("/contest-detail");
    localStorage.setItem("PROBLEM_SET", props.title);
  }
  return (
    <li className={classes.item} onClick={clickHandler}>
      <ProblemCard>
        <div className={classes.content}>
          <h3>{props.title}</h3>
        </div>
        <div className={classes.content}>
          <h6>Questions: {props.amount}</h6>
        </div>
        <div className={classes.content}>
          <h6>DUE: {props.date}</h6>
        </div>
      </ProblemCard>
    </li>
  );
}

export default ContestItem;
