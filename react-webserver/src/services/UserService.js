import axios from "axios";

const FRONTEND_API_URL = "https://api.codekarin.com/prod/%7Bproxy+%7D";

axios.defaults.baseURL = FRONTEND_API_URL;

async function getUser(parameters) {
  // function is invalid

  try {
    let response = await axios({
      method: "GET",
      url: FRONTEND_API_URL + "?access_token=" + parameters["access_token"] + "&id_token=" + parameters["id_token"] + "&request_name=getUserUnitTest&request_type=whoami&request_no=1",
      headers:{
        "Authorization": parameters["access_token"]
      }
    });
    let responseObj = await response['data'];
    console.log(responseObj);
    return Promise.resolve(responseObj);
  } catch (error) {
    console.error(error);
  }
}
export { getUser };
