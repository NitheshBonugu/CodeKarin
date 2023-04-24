import { useState, useEffect } from 'react';
import ClassRoomList from "../components/classrooms/ClassRoomList";
import {getClasses} from "../services/ClassService.js";

function ClassroomPage() {

  const [class_data, set_class_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      id_token: localStorage.getItem("ID_TOKEN")

    }
    getClasses(parameters).then(data => set_class_data(data));
  }, []);

  if(class_data === null){
    return <h2>Loading classrooms...</h2>;
  }
  return Render(class_data);
}

function Render(class_data){
  return (
    <section>
      <ClassRoomList classrooms={class_data} />
    </section>
  );
}
export default ClassroomPage;
