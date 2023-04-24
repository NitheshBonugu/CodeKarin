import "./about.css";
import { useHistory } from "react-router-dom";

function ContactPage() {

  const history = useHistory();
  function clickHandler() {
    history.push("/contact-external");
  }

  return (
  	<section>
	  	<div>
	  		<h1> CONTACT </h1>
	  	</div>
	    <div className="box-item person" onClick={clickHandler}>
	      <div className="image circle">
	        <img
	          src={require("../images/assets/kk.jpeg")}
	          alt="Person 1"
	          min_width="50%"
	        />
	      </div>
	      <h3>Krishna Kadiyala, Ph.D.</h3>
	      <p>Assistant Professor of Computer Science at Texas Christian University</p>
	      <p>Project Client & Mentor</p>
	      <p>k.kadiyala@tcu.edu</p>
	      <div>
	  		<p>For further information about the project, implementation, and future plans, feel free to reach out to project client and mentor:</p>
	  		<p>Dr. Krishna Kadiyala; Assistant Professor of Computer Science at Texas Christian University.</p>
	  	  </div>
	    </div>
    </section>
  );
}
export default ContactPage;
