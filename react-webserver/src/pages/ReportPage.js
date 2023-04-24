import React from "react";
import classes from "./ReportPage.module.css";
import RankTable from "../components/classrooms/RankTable.js";
import { getClassReport } from "../services/ReportService";
import { useEffect, useState } from "react";

function ReportPage() {
  const columns = React.useMemo(
    () => [
      {
        Header: "Name",
        accessor: "user_id", // accessor is the "key" in the data
      },
      {
        Header: "Finished Problems",
        accessor: "grade_aggregate",
      },
    ],
    []
  );

  const [report_data, set_data] = useState(null);

  useEffect(() => {
    const parameters = {
      user: localStorage.getItem("USER"),
      class: localStorage.getItem("CLASSROOM"),
      access_token: localStorage.getItem("ACCESS_TOKEN"),
      id_token:localStorage.getItem("ID_TOKEN"),
      problem_set:localStorage.getItem("PROBLEM_SET")
    };
    getClassReport(parameters).then((data) => set_data(data));
  }, []);

  if (report_data === null) {
    return <h2>Loading report...</h2>;
  }

  return (
    <section>
      <h1 className={classes.h1}>
        Here is the report for {localStorage.getItem("CLASSROOM")}
      </h1>
      <RankTable columns={columns} data={report_data} />
    </section>
  );
}

export default ReportPage;
