import React, { useEffect, useState } from 'react';

import { Container, Nav } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import DateRange from '../../Shared/DateRange/DateRange';
import { formatDate } from '../../../utils/dateFormat';
import useAuth from '../../../hooks/useAuth';


const Subscriptions = () => {
    const { authTokens } = useAuth();

    const [activeSubscriptions, setActiveSubscriptions] = useState([]);
    const [allSubscriptions, setAllSubscriptions] = useState([]);
    const [activeTableData, setActiveTableData] = useState({});
    const [allTableData, setAllTableData] = useState({});
    const [showTab, setShowTab] = useState('active');

    const [dateRange, setDateRange] = useState([new Date(), new Date(new Date().setMonth(new Date().getMonth() - 1))]);
    const [startDate, endDate] = dateRange;
    const [validDate, setValidDate] = useState(true);
    const [pending, setPending] = useState(true);


    const columnsActive = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
        {
            name: "Customer Name",
            selector: "customer_name",
            sortable: true,
            cell: d => d.customer_name === null ? <span>Null</span> : <span>{d.customer_name}</span>
        },
        {
            name: "Subscription Type",
            selector: "subscription_title",
            sortable: true,
            cell: d => d.subscription_title === null ? <span>Null</span> : <span>{d.subscription_title}</span>
        },
        {
            name: "Total Cost",
            selector: "total_cost",
            sortable: true,
            cell: d => d.total_cost === null ? <span>Null</span> : <span>{d.total_cost}</span>
        },
        {
            name: "Start Date",
            selector: "start_date",
            sortable: true,
            cell: d => d.start_date === null ? <span>Null</span> : <span>{d.start_date}</span>
        },
        {
            name: "End Date",
            selector: "end_date",
            sortable: true,
            cell: d => d.end_date === null ? <span>Null</span> : <span>{d.end_date}</span>
        },
    ];
    const columnsAll = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
        {
            name: "Customer Name",
            selector: "customer_name",
            sortable: true,
            cell: d => d.customer_name === null ? <span>Null</span> : <span>{d.customer_name}</span>
        },
        {
            name: "Subscription Type",
            selector: "subscription_title",
            sortable: true,
            cell: d => d.subscription_title === null ? <span>Null</span> : <span>{d.subscription_title}</span>
        },
        {
            name: "Total Cost",
            selector: "total_cost",
            sortable: true,
            cell: d => d.total_cost === null ? <span>Null</span> : <span>{d.total_cost}</span>
        },
        {
            name: "Start Date",
            selector: "start_date",
            sortable: true,
            cell: d => d.start_date === null ? <span>Null</span> : <span>{d.start_date}</span>
        },
        {
            name: "End Date",
            selector: "end_date",
            sortable: true,
            cell: d => d.end_date === null ? <span>Null</span> : <span>{d.end_date}</span>
        },
        {
            name: "Status",
            selector: "subscription_status",
            sortable: true,
            cell: d => d.subscription_status === null ? <span>Null</span> : <span>{d.subscription_status}</span>
        },
    ];

    const handleDateRange = (update) => {
        if (update[0] !== null && update[1] !== null) {
            setValidDate(true);
        }
        else {
            setValidDate(false)
        }
        setDateRange(update)
    }

    useEffect(() => {
        if (validDate) {
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/subscriptions/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`, {
                headers: {
                    Authorization: 'Bearer ' + String(authTokens?.access)
                }
            })
                .then(res => {
                    setActiveSubscriptions(res.data.activeSubscription)
                    setAllSubscriptions(res.data.allSubscription)
                })
                .then(() => setPending(false))
                .catch(err => console.log(err))
        }
    }, [validDate]);

    useEffect(() => {
        setActiveTableData({ columns: columnsActive, data: activeSubscriptions })
        setAllTableData({ columns: columnsAll, data: allSubscriptions })
    }, [activeSubscriptions, allSubscriptions])


    return (
        <Container style={{ minHeight: '75vh' }}>
            <DateRange startDate={startDate} endDate={endDate} handleDateRange={handleDateRange} />
            <Nav justify variant="tabs" style={{cursor: 'pointer'}}>
                <Nav.Item>
                    <div className={`fw-bold fs-6 nav-link ${showTab === 'active' ? 'active' : ''}`} onClick={() => setShowTab('active')}>Active Subscriptions</div>
                </Nav.Item>
                <Nav.Item>
                    <div className={`fw-bold fs-6 nav-link ${showTab === 'all' ? 'active' : ''}`} onClick={() => setShowTab('all')}>All Subscriptions</div>
                </Nav.Item>
            </Nav>
            {showTab === 'active' ?
                <DataTableContainer tableData={activeTableData} columns={columnsActive} data={activeSubscriptions} pending={pending} />
            :
                <DataTableContainer tableData={allTableData} columns={columnsAll} data={allSubscriptions} pending={pending} />
            }                
        </Container>
    );
};

export default Subscriptions;