import React from 'react';
import Navbar from 'react-bootstrap/Navbar'
//import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <div className="App">
		
		<link
		  rel="stylesheet"
		  href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
		  integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
		  crossorigin="anonymous"
		/>

		<Navbar bg="dark" variant="dark">
			<Navbar.Brand href="#home">
			  <img
				alt="SUMZ"
				src="https://octodex.github.com/images/Fintechtocat.png"
				width="30"
				height="30"
				className="d-inline-block align-top"
			  />{' '}
			  SUMZ Unternehmensbewertung
			</Navbar.Brand>
		  </Navbar>

      <header className="App-header">
        <h1>This is a fancy test app!</h1>
		<img src="https://octodex.github.com/images/Fintechtocat.png" className="App-logo" alt="logo" />
        <p>Edit <code>src/App.js</code> and save to reload.</p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer">
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
