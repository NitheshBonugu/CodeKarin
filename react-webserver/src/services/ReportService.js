import axios from "axios";

const FRONTEND_API_URL = "https://api.codekarin.com/prod/%7Bproxy+%7D";
axios.defaults.baseURL = FRONTEND_API_URL;

async function getClassReport(parameters) {
  // function is valid

  if(localStorage.getItem("CONTEST_REPORT") === "1"){
    try {
      let response = await axios({
        method: "GET",
        url:
          FRONTEND_API_URL + "?user=" + parameters["user"] + "&classroom_id=" + parameters["class"] + "&problem_set=" + parameters["problem_set"] + "&request_no=44&request_type=get_leaderboard&request_name=getGradeParseTest",
        headers:{
          "Authorization": parameters["access_token"]
        }
      });

      console.log(response);
      let responseObj = await response["data"];
      return Promise.resolve(responseObj);
    } catch (error) {
      console.error(error);
    }
  }else{
    try {
      let response = await axios({
        method: "GET",
        url:
          FRONTEND_API_URL + "?user=" + parameters["user"] + "&classroom_id=" + parameters["class"] + "&request_no=43&request_type=get_grade&request_name=getGradeParseTest",
        headers:{
          "Authorization": parameters["access_token"]
        }
      });

        console.log(response);
        let responseObj = await response["data"];
        return Promise.resolve(responseObj);
    } catch (error) {
      console.error(error);
    }
  }
  return null;
}
export { getClassReport };
//https://api.codekarin.com/prod/%7Bproxy+%7D?user=jakehollis&classroom_id=class1&request_no=43&request_type=get_grade&request_name=getGradeParseTest
