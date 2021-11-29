import React, { useEffect, useState } from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import useAuth from '../../../hooks/useAuth';
import { Container, Form, Button } from 'react-bootstrap';

const Login = () => {
    const [loginData, setLoginData] = useState({});

    const { loginUser, authError } = useAuth()

    const location = useLocation();
    const history = useHistory();

    useEffect(() => {
        // setAuthError('');
    }, []);

    const handleOnChange = e => {
        const field = e.target.name;
        const value = e.target.value;
        const newLoginData = { ...loginData };
        newLoginData[field] = value;
        setLoginData(newLoginData);
    }
    const handleLoginSubmit = e => {
        console.log(loginData.phone, loginData.password)
        loginUser(loginData.phone, loginData.password, location, history)
        e.preventDefault();
    }


    return (
        <Container fluid className="login-img">
            <div className="pt-5" style={{ paddingTop: 20 }}>
                <div className="py-3 px-5 mx-auto shadow-lg login-background" style={{ maxWidth: 400 }}>
                    <h3 className="text-center mb-4 primary-color fw-bold">Login</h3>
                    <Form onSubmit={handleLoginSubmit}>
                        <Form.Group className="mb-3" controlId="formBasicEmail">
                            <Form.Label>Phone Number</Form.Label>
                            <Form.Control name="phone" onChange={handleOnChange} type="text" placeholder="Enter Phone" />
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control name="password" onChange={handleOnChange} type="password" placeholder="Password" />
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBasicCheckbox">
                            <Form.Check type="checkbox" label="Check me out" />
                        </Form.Group>
                        <div className="d-flex flex-column justify-content-center">
                            <Button variant="light" type="submit" className="rounded-pill primary-background mt-4 fs-5">
                                Sign In
                            </Button>
                        </div>
                    </Form>
                    <p className="mt-4 text-center text-danger">{authError}</p>
                </div>
            </div>
        </Container>
    );
};

export default Login;