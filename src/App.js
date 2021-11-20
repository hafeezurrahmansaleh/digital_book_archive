import React, { useState } from 'react';
import './styles/App.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import "react-datepicker/dist/react-datepicker.css";
import 'react-data-table-component-extensions/dist/index.css';
import Layout from './Pages/Layout/Layout/Layout';
import { BrowserRouter as Router, Switch, Route, useHistory } from 'react-router-dom'
import Login from './Pages/Login/Login/Login';
import AuthProvider from './contexts/AuthProvider/AuthProvider';
// import Layout from './Layout';

function App() {
  const history = useHistory();

  return (
    <>
      <AuthProvider>
        <Router>
          <Switch>
            {/* <Route exact path="/">
            {
              history.push('/dashboard')
            }
          </Route> */}
            <Route path="/dashboard">
              <Layout />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
          </Switch>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
