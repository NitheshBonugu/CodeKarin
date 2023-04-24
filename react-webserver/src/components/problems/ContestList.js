import classes from "./ProblemList.module.css";
import ContestItem from "./ContestItem";
function ContestList(props) {
  return (
    <div>
      <h1 className={classes.h1}>Contests</h1>
      <ul className={classes.list}>
        {props.contests.map((contest) => (
           <ContestItem
            title={contest.set_name}
            key={contest.id}
            amount={contest.num_probs}
            date={contest.end_date}
          />
        ))}
      </ul>
    </div>
  );
}
export default ContestList;
