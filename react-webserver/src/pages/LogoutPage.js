//import classes from "./SettingsPage.module.css";
import { useHistory } from "react-router-dom";

function LogoutPage() {
  const history = useHistory();
  localStorage.clear();
  history.push("/home");
  window.location.reload(false);
  return null;
}
export default LogoutPage;
