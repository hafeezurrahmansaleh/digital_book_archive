import React, { useState } from 'react';
import { Container, Navbar } from 'react-bootstrap';
import { FaBars } from 'react-icons/fa';
import { Route, useRouteMatch } from 'react-router';
import Books from '../../Report/Books/Books';
import Customers from '../../Report/Customers/Customers';
import Publishers from '../../Report/Publishers/Publishers';
import Subscriptions from '../../Report/Subscriptions/Subscriptions';
import Transactions from '../../Report/Transactions/Transactions';
import Summary from '../../Summary/Summary/Summary';
import Aside from '../Aside/Aside';
import Footer from '../Footer/Footer';

function Layout() {
    let { path, url } = useRouteMatch();
    const [collapsed, setCollapsed] = useState(false);
    const [toggled, setToggled] = useState(false);

    const handleCollapsedChange = (checked) => {
        setCollapsed(checked);
    };

    const handleToggleSidebar = (value) => {
        setToggled(value);
    };

    return (
        <div className={`app ${toggled ? 'toggled' : ''}`}>
            <Aside
                url={url}
                collapsed={collapsed}
                toggled={toggled}
                handleToggleSidebar={handleToggleSidebar}
            />
            <main>
                <Navbar bg="white" variant="light">
                    <Container>
                        <Navbar.Brand>
                            <div className="d-lg-none" onClick={() => handleToggleSidebar(!toggled)}>
                                <FaBars className="mb-1 me-2" /> <span> Dashboard</span>
                            </div>
                            <div className="d-none d-lg-block" onClick={() => handleCollapsedChange(!collapsed)}>
                                <FaBars className="mb-1 me-2" /> <span> Dashboard</span>
                            </div>
                        </Navbar.Brand>
                    </Container>
                </Navbar>
                <section className="block mt-5 text-center">
                    <Route exact path={`${path}`}>
                        <Summary />
                    </Route>
                    <Route path={`${path}/customers`}>
                        <Customers />
                    </Route>
                    <Route path={`${path}/books`}>
                        <Books />
                    </Route>
                    <Route path={`${path}/publishers`}>
                        <Publishers />
                    </Route>
                    <Route path={`${path}/subscriptions`}>
                        <Subscriptions />
                    </Route>
                    <Route path={`${path}/transactions`}>
                        <Transactions />
                    </Route>
                </section>

                <Footer />
            </main>
        </div>
    );
}

export default Layout;
