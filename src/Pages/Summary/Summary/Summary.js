import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Card, Col, Container, Row } from 'react-bootstrap';
import { FaBook, FaBuilding, FaUserAlt, FaUserCheck, FaUserClock } from "react-icons/fa";
import useAuth from '../../../hooks/useAuth';
import SubscribeChart from '../SubscribeChart/SubscribeChart';


const Summary = () => {
    const { authTokens} = useAuth();
    const [summary, setSummary] = useState([]);

    useEffect(() => {
        console.log(authTokens);
        // const headerData = { headers: { Authorization: 'Bearer ' + authTokens }};
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/summary/', {
            headers: {
                Authorization: 'Bearer ' + String(authTokens?.access)
            }
        })
            .then(res => setSummary(res.data))
            .catch(err => console.log(err))
    }, []);

    return (
        <Container>
            <Row xs={1} md={2} lg={4} className="g-4">
                {
                    summary.map((s, idx) => (
                        <Col key={idx}>
                            <Card
                                className="shadow border-0 h-100"
                                style={{
                                    backgroundColor: `${idx === 0 ? '#B2DFDB' :
                                        idx === 1 ? '#B3E5FC' :
                                            idx === 2 ? '#F8BBD0' :
                                                idx === 3 ? '#FFE0B2' :
                                                    'gray'}`
                                }}
                            >
                                <Card.Body className="d-flex align-items-center justify-content-around">
                                    <Card.Text className="text-secondary">
                                        {s.title === 'Booklist' ? <FaBook className="fs-1" /> :
                                            s.title === 'Customer' ? <FaUserAlt className="fs-1" /> :
                                                s.title === 'Subscription' ? <FaUserCheck className="fs-1" /> :
                                                    s.title === 'Publisher' ? <FaBuilding className="fs-1" /> : ''
                                        }
                                    </Card.Text>
                                    <div className="text-secondary fw-bold">
                                        <div>
                                            <h2> {s.number}</h2>
                                        </div>
                                        <div>
                                            <p className="fs-5"> {s.title}</p>
                                        </div>
                                    </div>
                                </Card.Body>
                            </Card>
                        </Col>
                    ))
                }
            </Row>

            <SubscribeChart />            
        </Container>
    );
};

export default Summary;