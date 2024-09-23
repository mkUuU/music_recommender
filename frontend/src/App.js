import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import MusicRecommendations from './components/MusicRecommendations';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/register" component={Register} />
        <Route path="/login" component={Login} />
        <Route path="/recommendations" component={MusicRecommendations} />
      </Switch>
    </Router>
  );
};

export default App;

