import React from "react";
import "./about.css";
//import { Link } from "react-router-dom";

function AuthorPage() {
  const AuthorData = [
    {
      key: 1,
      text: "Bachelor of Computer Science; Dylan Wulfson worked on the API gateway which manages all the of the project’s user authentication and controls layer logic for calling into the teams backend data/services. His outside interests include game development, robotics, and PC building. Mr. Wulfson hopes to purse a career in the game industry, security, or machine learning.",
      img: require("../images/assets/DylanWulfson.png"),
      imgAuthor: "Dylan Wulfson",
    },
    {
      key: 2,
      text: "Bachelor of Computer Science, Minor in Mathematics; Throughout this senior design project he has functioned as the team lead, architecture designer, and backend developer. Jacob's research/hobby interests include, cloud computing, deep machine learning, and video game design. After graduating from Texas Christian University in May 2022, he hopes to secure a job as a software engineer related to cloud computing, systems design/development, and/or machine learning. In this project he leveraged AWS cloud services to create a platform for professors to release code assignments to students that can be completed and graded in the browser.",
      img: require("../images/assets/JacobHollis.png"),
      imgAuthor: "Jacob Hollis",
    },
    {
      key: 3,
      text: "Bachelor of Computer Info Technology, Minor in Mathematics; Kate Brayshaw acted as a fronted developer and lead documenter. She hopes to pursue a career in machine learning, security, or frontend development. Ms. Brayshaw’s hobbies and interests include reading, solving puzzles, and working with AI.  Throughout the process of Code Karin she developed static frontend pages, developed the teams website, and wrote documentation such as the glossary, use cases, and the teams vision document.",
      img: require("../images/assets/KateBrayshaw.png"),
      imgAuthor: "Kate Brayshaw",
    },
    {
      key: 4,
      text: "Bachelor of Computer Science, Minor in General Business; Nghan Hang Tran is the lead Frontend Developer for Code Karin. She will pursue software engineering roles after graduation. Her hobbies include working out, problem solving and eating Vietnamese food.",
      img: require("../images/assets/NganHanhTran.png"),
      imgAuthor: "Ngan HanhTran",
    },
    {
      key: 5,
      text: "Bachelor of Computer Science; During the creation of Code Karin Nithesh Bonugu assisted as a frontend developer. He has an immense interest in Artificial Intelligence and is currently in search of software engineering roles, and looks forward to an exciting career ahead.",
      img: require("../images/assets/NitheshBonugu.png"),
      imgAuthor: "Nithesh Bonugu",
    },
  ];
  return (
    <div>
      <section className="author">
        <div className="author-banner-main">
          <h1>Authors</h1>
        </div>
      </section>

      <section className="">
        {AuthorData.map((author) => (
          <div className="authors-section" key={author.key}>
            <div className="img-section">
              <img src={author.img} alt="Pic 01" />
              <p className="img-text">{author.imgAuthor}</p>
            </div>
            <div className="text-section">
              <p>{author.text}</p>
            </div>
          </div>
        ))}
      </section>

      <footer id="footer">
        <div className="item-wrap">
          <div className="flex">
            <div className="copyright">
              Code Karin 2021-2022. Texas Christian University.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default AuthorPage;
