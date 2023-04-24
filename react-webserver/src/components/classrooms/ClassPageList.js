import { useHistory } from "react-router-dom";
import classes from "../home/HomeList.module.css";
function ClassPageList() {
  const history = useHistory();
  function clickHandler(event) {
    localStorage.setItem("CONTEST_REPORT", "0");
    history.push(`/${event.target.getAttribute("value")}`);
  }
  return (
    <div className={classes.group}>
      <div
        className={classes.item + " " + classes.about}
        value="practice-list"
        onClick={clickHandler.bind(this)}
      >
        <button
          value="practice-list"
          onClick={clickHandler.bind(this)}
        >PRACTICE</button>
      </div>
      <div
        className={classes.item + " " + classes.explore}
        value="contest-list"
        onClick={clickHandler.bind(this)}
      >
        <button
          value="contest-list"
          onClick={clickHandler.bind(this)}
        >CONTEST</button>
      </div>
      <div
        className={classes.item + " " + classes.report}
        value="report"
        onClick={clickHandler.bind(this)}
      >
        <button
          value="report"
          onClick={clickHandler.bind(this)}
        >RANK REPORT</button>
      </div>
    </div>
  );
}
export default ClassPageList;
