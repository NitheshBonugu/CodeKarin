import classes from "./HomeList.module.css";
import { useHistory } from "react-router-dom";

function HomePageList() {
  const history = useHistory();

  function aboutHandler() {
    history.push("/about");
  }

  function authorHandler() {
    history.push("/authors");
  }

  function loginHandler() {
    history.push("/login");
  }

  return (
    <div className={classes.group}>
      <div
        className={classes.item + " " + classes.about}
        onClick={aboutHandler}
      >
        ABOUT KARIN TEAM
      </div>
      <div
        className={classes.item + " " + classes.explore}
        onClick={authorHandler}
      >
        AUTHORS
      </div>
      <div className={classes.item + " " + classes.contact}>CONTACT</div>
      <div
        className={classes.item + " " + classes.login}
        onClick={loginHandler}
      >
        LOGIN
      </div>
    </div>
  );
}
export default HomePageList;
