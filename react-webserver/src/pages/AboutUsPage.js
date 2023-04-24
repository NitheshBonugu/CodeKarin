import React from "react";
import { useState, useEffect } from 'react';
import { useHistory } from "react-router-dom";
import "./about.css";
import { getUser } from "../services/UserService"

function AboutPage() {
  const history = useHistory();
  function clickHandler() {
    history.push("/authors");
  }

  var reloadFlag = false;
  const [user_data, set_user_data] = useState(null);

  var uri = new URL(window.location.href);
  var str = uri.hash.split('&');
  if(str.length > 1){
    var id_token = str[0];
    id_token = id_token.replace("#id_token=", "");
    var access_token = str[1];
    access_token = access_token.replace("access_token=", "");

    localStorage.setItem("ID_TOKEN", String(id_token));
    localStorage.setItem("ACCESS_TOKEN", String(access_token));

    if(reloadFlag){
      window.location.reload(false);
      reloadFlag = false;
    }
  }

  useEffect(() => {
    const parameters = {
      'id_token': localStorage.getItem("ID_TOKEN"),
      'access_token': localStorage.getItem("ACCESS_TOKEN")
    }
    getUser(parameters).then(data => set_user_data(data)).then(reloadFlag = true);
  }, []);

  if(user_data == null || localStorage.getItem("ID_TOKEN") == null){
    console.log('failure to authenticate');
  }else{
    localStorage.setItem("EMAIL" ,user_data['email']);
    localStorage.setItem("USER" ,user_data['user_id']);
  }

  return (
    <section>
      <div id="banner-main">
        <h1>About Code Karin</h1>
        <p>Virtual Classroom</p>
      </div>

      <div id="second" className="wrapper style1 special">
        <div className="item-wrap">
          <header>
            <h2>Meet The Team</h2>
          </header>
          <div className="flex flex-5">
            <div className="box-item person" onClick={clickHandler}>
              <div className="image circle">
                <img
                  src={require("../images/assets/team lead_Backend Developer.png")}
                  alt="Person 1"
                />
              </div>
              <h3>Jacob Hollis</h3>
              <p>Team Leader</p>
            </div>
            <div className="box-item person" onClick={clickHandler}>
              <div className="image circle">
                <img
                  src={require("../images/assets/API Gateway.png")}
                  alt="Person 2"
                />
              </div>
              <h3>Dylan Wulfson</h3>
              <p>API Gateway</p>
            </div>
            <div className="box-item person" onClick={clickHandler}>
              <div className="image circle">
                <img
                  src={require("../images/assets/Frontend Developer.png")}
                  alt="Person 3"
                />
              </div>
              <h3>Ngan Hanh Tran</h3>
              <p>Frontend Developer</p>
            </div>
            <div className="box-item person" onClick={clickHandler}>
              <div className="image circle">
                <img
                  src={require("../images/assets/Database.png")}
                  alt="Person 4"
                />
              </div>
              <h3>Kate Brayshaw</h3>
              <p>Database</p>
            </div>
            <div className="box-item person" onClick={clickHandler}>
              <div className="image circle">
                <img
                  src={require("../images/assets/JUnit Testing.png")}
                  alt="Person 5"
                />
              </div>
              <h3>Nithesh Bonugu</h3>
              <p>Frontend Developer</p>
            </div>
          </div>
        </div>
      </div>

      <div id="three" className="wrapper special">
        <div className="item-wrap">
          <header className="align-center">
            <h2>Who We Are</h2>
          </header>
          <div className="flex flex-1">
            <article>
              <header>
                <h3>Our Story</h3>
              </header>
              <p>
                Our programming practice platform, CodeKarin, is the brainchild of Dr. Krishna Kadiyala. At its core, Code Karin is fundamentally an effort to address student retention and performance in introductory programming classes. Dr. Kadiyala observed that in her introductory programming classes, first-time programming students often felt unsure of themselves in comparison with their peers who have had prior programming experience. Often, first-time programmers missed out on the opportunity to participate and engage in classes, with their peers and professors. Unfortunately, it also meant that these students often did not ask for help and eventually, were most likely to drop out of the programming class. Dr. Kadiyala also made an alarming observation that it was very easy for these students to assume that they were simply not “programming savvy”, or “as good as their peers”. Code Karin was born as an initial step towards helping students transition into programming classes and increase student engagement in and outside of class by building a sense of community and belonging.
              </p>

              <header>
                <h3>Code Karin</h3>
              </header>
              <p>
                Code Karin does the following important things to help students, especially first-time programmers:
                <ol>
                <li>Students participate on this platform anonymously so there is no fear of judgement from peers.</li>
                <li>A healthy competition in a fun approach of in-class, timed programming contests.</li>
                <li>Extends hands-on programming examples from the classroom into out-of-class programming practice.</li>
                </ol>
                In further extending this platform, Dr. Kadiyala also plans to include a safe space for discussions between students in an anonymous fashion. With this next step, Dr. Kadiyala hopes to encourage student participation in and outside of class.
              </p>
              <div className="image fit">
                <img
                  src={require("../images/assets/BottomHomePagePic.png")}
                  alt="Pic 01"
                />
              </div>
            </article>
          </div>
        </div>
      </div>

      <footer id="footer">
        <div className="item-wrap">
          <div className="flex">
            <div className="copyright">
              Code Karin 2021-2022. Texas Christian University.
            </div>
          </div>
        </div>
      </footer>
    </section>
  );
}
export default AboutPage;
