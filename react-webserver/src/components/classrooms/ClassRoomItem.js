import classes from "../problems/ProblemItem.module.css";
import ProblemCard from "../layout/ProblemCard";
import { useHistory } from "react-router-dom";
function ClassRoomItem(props) {
  const history = useHistory();

  function clickHandler() {
    history.push(`/classroom`);
    localStorage.setItem('CLASSROOM', props.title);
  }
  return (
    <li className={classes.item} onClick={clickHandler}>
      <ProblemCard>
        <div className={classes.content}>
          <h3>{props.title}</h3>
        </div>
        <div className={classes.content}>
          <h6>Professor: {props.professor}</h6>
        </div>
        <div className={classes.content}>
          <h6>End Date: {props.date}</h6>
        </div>
      </ProblemCard>
    </li>
  );
}
export default ClassRoomItem;
