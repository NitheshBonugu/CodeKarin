import axios from "axios";

const FRONTEND_API_URL = "https://api.codekarin.com/prod/%7Bproxy+%7D";

axios.defaults.baseURL = FRONTEND_API_URL;

async function getProblemSet(parameters) {
  // function is valid
  try {
    let response = await axios({
      method: "GET",
      url:
        FRONTEND_API_URL + "?user=" + parameters["user"] + "&class_name=" + parameters["class_id"] + "&set_type=" + parameters["set_type"] + "&request_name=getUserUnitTest&request_type=get_classroom&request_no=11",
      headers:{
        "Authorization": parameters["access_token"]
      }
    });
    console.log(response);
    let responseObj = await response["data"]["prob_set_list"];
    return Promise.resolve(responseObj);
  } catch (error) {
    console.error(error);
  }

  return null;
}

async function getProblemList(parameters) {
  // function is valid
  try {
    let response = await axios({
      method: "GET",
      url:
        FRONTEND_API_URL + "?user=" + parameters["user"] + "&class_name=" + parameters["class_id"] + "&problem_set=" + parameters["problem_set"] + "&request_name=getProbSetUnitTest&request_type=view_problems&request_no=31",
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

  return null;
}

async function getProblem(parameters) {
  // function is valid
  try {
    let response = await axios({
      method: "GET",
      url: FRONTEND_API_URL + "?user=" + parameters["user"] + "&class_name=" + parameters["class_id"] + "&problem_id=" + parameters["problem_id"] + "&request_name=getProbSetUnitTest&request_type=get_problem&request_no=33",
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

  return null;
}
export { getProblemSet, getProblemList, getProblem };
