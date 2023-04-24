import classes from "./ProblemCard.module.css";
function ProblemCard(props) {
  return <div className={classes.card}>{props.children}</div>;
}
export default ProblemCard;
