import classes from "./SettingsPage.module.css";

function SettingsPage() {
  const user = {
    name: localStorage.getItem("USER"),
    email: localStorage.getItem("EMAIL"),
  };

  return (
    <section>
      <h3>Name: {user.name}</h3>
      <h3>Email: {user.email}</h3>
      <div className={classes.actions}>
        <button>Change Password</button>
      </div>
    </section>
  );
}
export default SettingsPage;
