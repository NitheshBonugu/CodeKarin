import axios from "axios";

const FRONTEND_API_URL = "https://api.codekarin.com/prod/%7Bproxy+%7D";

axios.defaults.baseURL = FRONTEND_API_URL;

async function updateCode(parameters) {
  // function is valid
  try {
    let response = await axios({
      method: "POST",
      url:
        FRONTEND_API_URL + "?user=" + parameters["user"] + "&problem_id=" + parameters["problem_id"] + "&classroom_id=" + parameters["class_id"] + "&request_name=submitCodeTest&request_type=submit_code&request_no=3",
      headers:{
        "Authorization": parameters["access_token"]
      },
      data: {
        code: String(parameters["entered_code"]),
      }
    });
    let responseObj = await response["data"];
    console.log(responseObj);
    return Promise.resolve(responseObj);
  } catch (error) {
    console.error(error);
  }

  return null;
}
async function getCodeResult(parameters) {
  var ar = parameters["problem_id"].split("/");
  var set_name = ar[0];
  var problem_name = ar[1];
  // function is valid
  try {
    let response = await axios({
      method: "GET",
      url: FRONTEND_API_URL + "?user=" + parameters["user"] + "&set_name=" + set_name + "&problem_name=" + problem_name + "&classroom_id=" + parameters["class_id"] + "&request_name=checkBuildTest&request_type=check_build&request_no=4",
      headers:{
        "Authorization": parameters["access_token"]
      }
    });
    let responseObj = await response["data"];
    console.log(responseObj);
    return Promise.resolve(responseObj);
  } catch (error) {
    console.error(error);
  }

  return null;
}
export { updateCode, getCodeResult };
