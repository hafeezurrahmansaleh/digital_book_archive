import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [tableData, setTableData] = useState({});

    // console.log(customer[4].full_name.toString())

    const columns = [
        {
            name: "Full Name",
            selector: "full_name",
            sortable: true,
            cell: d => d.full_name === null ? <span>Null</span> : <span>{d.full_name}</span>
        },
        {
            name: "Email",
            selector: "email",
            sortable: true,
            cell: d => d.email === null ? <span>Null</span> : <span>{d.email}</span>
        },
        {
            name: "Phone",
            selector: "phone",
            sortable: true
        },
        {
            name: "Subscription",
            selector: "status",
            sortable: true,
            cell: d => d.status === null ? <span>No</span> : <span>Yes</span>
        }
    ];
    

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/customers/',)
            .then(res => setCustomers(res.data))
            .catch(err => console.log(err))
    }, []);

    useEffect(() => {
        setTableData({ columns: columns, data: customers })
    }, [customers])

    // if (Object.keys(tableData).length ){
    //     console.log(Object.keys(tableData).length)
    //     console.log(customer.length)
    //     console.log(tableData)

    // }

    return (
        <Container className="main">
            <DataTableContainer tableData={tableData} columns={columns} data={customers} />
        </Container>
    );
};

export default Customers;