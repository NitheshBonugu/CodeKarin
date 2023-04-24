import classes from "./ProblemList.module.css";
import QuestionItem from "./QuestionItem";
function QuestionList(props) {
  return (
    <div>
      <h1 className={classes.h1}>Look what questions we can do today!!!</h1>
      <ul className={classes.list}>
        {props.questions.map((question) => (
          <QuestionItem
            title={question.prob_name}
            key={question.id}
            description={question.description}
          />
        ))}
      </ul>
    </div>
  );
}
export default QuestionList;
