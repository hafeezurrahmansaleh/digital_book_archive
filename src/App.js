import React from 'react';
import './styles/App.scss';
import 'bootstrap/dist/css/bootstrap.min.css';
import "react-datepicker/dist/react-datepicker.css";
import 'react-data-table-component-extensions/dist/index.css';
import Layout from './Pages/Layout/Layout/Layout';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { Redirect } from 'react-router'
import Login from './Pages/Login/Login/Login';
import AuthProvider from './contexts/AuthProvider/AuthProvider';
import AdminRoute from './Pages/Login/Login/AdminRoute/AdminRoute';
import PageNotFound from './Pages/PageNotFound/PageNotFound';
import ScrollToTop from './Pages/Shared/ScrollToTop/ScrollToTop';


function App() {

  return (
    <>
      <AuthProvider>
        <Router>
          <ScrollToTop />
          <Switch>
            <Route exact path="/">
              <Redirect to="/dashboard" />
            </Route>
            <AdminRoute path="/dashboard">
              <Layout />
            </AdminRoute>
            <Route path="/login">
              <Login />
            </Route>
            <Route path="*">
              <PageNotFound />
            </Route>
          </Switch>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
