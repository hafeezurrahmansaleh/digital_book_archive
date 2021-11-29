import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import DateRange from '../../Shared/DateRange/DateRange';
import useAuth from '../../../hooks/useAuth';

const Publishers = () => {
    const { authTokens } = useAuth();

    const [publishers, setPublisher] = useState([]);
    const [tableData, setTableData] = useState({});
    const [pending, setPending] = useState(true);


    const columns = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
        {
            name: "Publisher Name",
            selector: "name",
            sortable: true,
            cell: d => d.name === null ? <span>Null</span> : <span>{d.name}</span>
        },
        {
            name: "Publisher Email",
            selector: "email",
            sortable: true,
            cell: d => d.email === null ? <span>Null</span> : <span>{d.email}</span>
        },
        {
            name: "Total Publication",
            selector: "total",
            sortable: true
        }
    ];


    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/publishers/', {
            headers: {
                Authorization: 'Bearer ' + String(authTokens?.access)
            }
        })
            .then(res => setPublisher(res.data))
            .then(() => setPending(false))
            .catch(err => console.log(err))
    }, []);

    useEffect(() => {
        setTableData({ columns: columns, data: publishers })
    }, [publishers])


    return (
        <Container className="main" style={{ minHeight: '75vh' }}>
            <DataTableContainer tableData={tableData} columns={columns} data={publishers} pending={pending} />
        </Container>
    );
};

export default Publishers;