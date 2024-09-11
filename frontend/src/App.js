import React from 'react';
import './App.css';
import { Amplify } from 'aws-amplify';
import amplifyconfig from './amplifyconfiguration.json';
import AppRouter from './routes/routes'

Amplify.configure(amplifyconfig);

function App() {

  return (
    <AppRouter />
  );
}

export default App;
