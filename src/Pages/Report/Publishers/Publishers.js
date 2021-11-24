import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';

const Publishers = () => {
    const [publishers, setPublisher] = useState([]);
    const [tableData, setTableData] = useState({});

    // console.log(customer[4].full_name.toString())

    const columns = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
        {
            name: "Publisher Name",
            selector: "publisher__name",
            sortable: true,
            cell: d => d.publisher__name === null ? <span>Null</span> : <span>{d.publisher__name}</span>
        },
        {
            name: "Publisher Email",
            selector: "publisher__email",
            sortable: true,
            cell: d => d.publisher__email === null ? <span>Null</span> : <span>{d.publisher__email}</span>
        },
        {
            name: "Total Publication",
            selector: "total",
            sortable: true
        }
    ];


    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/publishers/',)
            .then(res => setPublisher(res.data))
            .catch(err => console.log(err))
    }, []);

    useEffect(() => {
        setTableData({ columns: columns, data: publishers })
    }, [publishers])

    // if (Object.keys(tableData).length ){
    //     console.log(Object.keys(tableData).length)
    //     console.log(customer.length)
    //     console.log(tableData)

    // }

    return (
        <Container className="main">
            <DataTableContainer tableData={tableData} columns={columns} data={publishers} />
        </Container>
    );
};

export default Publishers;