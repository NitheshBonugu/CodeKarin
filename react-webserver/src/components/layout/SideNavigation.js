import { Link } from "react-router-dom";
import classes from "./SideNavigation.module.css";

function SideNavigation() {
  return (
    <div className={classes.navbar}>
      <ul id="menu">
        <li>
          <Link to="/settings">Profile Settings</Link>
        </li>
        <li>
          <Link to="/logout">Log Out</Link>
        </li>
      </ul>
    </div>
  );
}
export default SideNavigation;
