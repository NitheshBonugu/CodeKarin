import classes from "../problems/ProblemList.module.css";
import ClassRoomItem from "./ClassRoomItem";

function ClassRoomList(props) {
  return (
    <div>
      <h1 className={classes.h1}>Here's your classrooms</h1>
      <ul className={classes.list}>
        {props.classrooms.map((classroom) => (
          <ClassRoomItem
            title={classroom.classroom_id}
            key={classroom.id}
            id={classroom.id}
            professor={classroom.professor_id}
            date={classroom.end_date}
          />
        ))}
      </ul>
    </div>
  );
}
export default ClassRoomList;
