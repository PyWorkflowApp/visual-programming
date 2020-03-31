import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import About from './About';
import Workspace from './Workspace';


function App() {

    return (
        <Container fluid={true} className="App">
            <Header />
            <Workspace />
        </Container>
    )
}


function Header() {
    return (
        <>
            <Row>
                <Col md={12}>
                    <h1>Visual Programming Workspace</h1>
                </Col>
                <About show={false} />
            </Row>
            <hr />
        </>
    )
}

export default App;
