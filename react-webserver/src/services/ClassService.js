import axios from "axios";

const FRONTEND_API_URL = "https://api.codekarin.com/prod/%7Bproxy+%7D";
axios.defaults.baseURL = FRONTEND_API_URL;

async function getClasses(parameters) {
  // function is valid

  try {
    let response = await axios({
      method: "GET",
      url:
        FRONTEND_API_URL + "?user=" + parameters["user"] + "&request_name=getUserUnitTest&request_type=get_user&request_no=21",
      headers:{
        "Authorization": parameters["access_token"]
      }
    });
    console.log(response);
    let responseObj = await response["data"]["user_get_response"]["classrooms"];
    return Promise.resolve(responseObj);
  } catch (error) {
    console.error(error);
  }

  return null;
}
export { getClasses };
