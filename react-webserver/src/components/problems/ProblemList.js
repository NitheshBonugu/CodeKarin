import classes from "./ProblemList.module.css";
import ProblemItem from "./ProblemItem";
function ProblemList(props) {
  return (
    <div>
      <h1 className={classes.h1}>Let's Practice</h1>
      <ul className={classes.list}>
        {props.problems.map((problem) => (
          <ProblemItem
            title={problem.set_name}
            key={problem.id}
            amount={problem.num_probs}
          />
        ))}
      </ul>
    </div>
  );
}
export default ProblemList;
