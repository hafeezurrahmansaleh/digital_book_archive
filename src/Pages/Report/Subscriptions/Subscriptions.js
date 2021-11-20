import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';

const Subscriptions = () => {
    const [activeSubscriptions, setActiveSubscriptions] = useState([]);
    const [allSubscriptions, setAllSubscriptions] = useState([]);
    const [activeTableData, setActiveTableData] = useState({});
    const [allTableData, setAllTableData] = useState({});

    // console.log(customer[4].full_name.toString())

    const columns = [
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


    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/subscriptions/',)
            .then(res =>{ 
                setActiveSubscriptions(res.data.activeSubscription)
                setAllSubscriptions(res.data.allSubscription)
            })
            .catch(err => console.log(err))
    }, []);

    useEffect(() => {
        setActiveTableData({ columns: columns, data: activeSubscriptions })
        setAllTableData({ columns: columns, data: allSubscriptions })
    }, [activeSubscriptions, allSubscriptions])

    // if (Object.keys(tableData).length ){
    //     console.log(Object.keys(tableData).length)
    //     console.log(customer.length)
    //     console.log(tableData)

    // }

    return (
        <Container>
            <DataTableContainer tableData={activeTableData} columns={columns} data={activeSubscriptions} />
            <DataTableContainer tableData={allTableData} columns={columns} data={allSubscriptions} />
            <hr />
            <hr />
        </Container>
    );
};

export default Subscriptions;