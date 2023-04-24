import { Link } from "react-router-dom";
import classes from "./MainNavigation.module.css";
//import notification from "../../images/notifications_black_24dp.svg";
import user from "../../images/person_black_24dp.svg";
//import menu from "../../images/menu_black_24dp.svg";

function MainNavigation({ toggleHandler }) {
  if (localStorage.getItem("USER") !== null) {
    return (
      <header className={classes.header}>
        <div className={classes.logo}>KARIN VIRTUAL CLASSROOM</div>
        <nav>
          <ul>
            <li>
              <Link to="/about">ABOUT KARIN</Link>
            </li>
            <li>
              <Link to="/authors">AUTHORS</Link>
            </li>
            <li>
              <Link to="/login">LOGIN</Link>
            </li>
            <li>
              <Link to="/contact">CONTACT</Link>
            </li>
            <li>
              <Link to="/class-list">VIEW CLASSROOMS</Link>
            </li>
            <li>
              <img
                className={classes.icon + " " + classes.filter}
                src={user}
                alt=""
                onClick={toggleHandler}
              />
            </li>
          </ul>
        </nav>
      </header>
    );
  }

  return (
    <header className={classes.header}>
      <div className={classes.logo}>KARIN VIRTUAL CLASSROOM</div>
      <nav>
        <ul>
          <li>
            <Link to="/about">ABOUT KARIN</Link>
          </li>
          <li>
            <Link to="/authors">AUTHORS</Link>
          </li>
          <li>
            <Link to="/login">LOGIN</Link>
          </li>
          <li>
            <Link to="/contact">CONTACT</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
export default MainNavigation;
