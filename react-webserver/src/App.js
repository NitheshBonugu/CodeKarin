import AWS from "aws-sdk";
import { Route, Redirect, Switch } from "react-router-dom";

//import HomePage from "./pages/HomePage";
import Layout from "./components/layout/Layout";

import ClassListPage from "./pages/ClassListPage";
import ClassPage from "./pages/ClassPage";

import PracticeListPage from "./pages/PracticeListPage";
import PracticeDetailPage from "./pages/PracticeDetailPage";
import ContestListPage from "./pages/ContestListPage";
import ContestDetailPage from "./pages/ContestDetailPage";
import CodingPage from "./pages/CodingPage";

import ContactPage from "./pages/ContactPage";
import SettingsPage from "./pages/SettingsPage";
import ReportPage from "./pages/ReportPage";
import LogoutPage from "./pages/LogoutPage";

//import ChatShell from "./pages/ChatPage";

import AuthorsPage from "./pages/AuthorsPage";
import AboutPage from "./pages/AboutUsPage";

function App() {
  const config = {
    region: "us-west-2",
  };
  AWS.config.update(config);
  return (
    <Layout>
      <Switch>
        <Route path="/health" exact status={200}>
          <h3>The App is Healthy</h3>
        </Route>
        <Route path="/" exact status={200}>
          <AboutPage />
        </Route>
        <Route path="/home" exact status={200}>
          <AboutPage />
        </Route>
        <Route path="/about" exact status={200}>
          <AboutPage />
        </Route>
        <Route path="/authors" exact status={200}>
          <AuthorsPage />
        </Route>
        <Route path="/contact" exact status={200}>
          <ContactPage />
        </Route>
        <Route path="/class-list" exact status={200}>
          <ClassListPage />
        </Route>
        <Route path="/classroom" exact status={200}>
          <ClassPage />
        </Route>
        <Route path="/contest-list" exact>
          <ContestListPage />
        </Route>
        <Route path="/contest-detail" exact>
          <ContestDetailPage />
        </Route>
        <Route path="/practice-list" exact status={200}>
          <PracticeListPage />
        </Route>
        <Route path="/practice-detail" exact status={200}>
          <PracticeDetailPage />
        </Route>
        <Route path="/code" exact>
          <CodingPage />
        </Route>
        <Route path="/report" exact status={200}>
          <ReportPage />
        </Route>
        <Route path="/contest-report" exact status={200}>
          <ReportPage />
        </Route>
        <Route path="/settings" exact status={200}>
          <SettingsPage />
        </Route>
        <Route
          path="/login"
          component={() => {
            window.location.href =
              "https://login.auth.codekarin.com/login?response_type=token&client_id=6fpg65ems7sc487neqnj3dbumi&redirect_uri=https://codekarin.com/home&state=STATE&scope=openid+profile+aws.cognito.signin.user.admin";
            return null;
          }}
        />
        <Route path="/logout" exact status={200}>
          <LogoutPage />
        </Route>
        <Route
          path="/contact-external"
          component={() => {
            window.location.href =
              "https://cse.tcu.edu/faculty-staff/view/krishna-kadiyala";
            return null;
          }}
        />
        <Route path="/not-found" exact status={200}>
          <h3>Page Not Found</h3>
        </Route>
        <Redirect to="/not-found" />
      </Switch>
    </Layout>
  );
}

//App.use(function)
export default App;
