import React from 'react';
import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import About from './About';


function App() {

    return (
        <Container className="App">
            <h1>Visual Programming Workspace</h1>
            <About show={false} />
        </Container>
    )
}

export default App;
