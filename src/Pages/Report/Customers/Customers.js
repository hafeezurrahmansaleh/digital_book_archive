import React, { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import { formatDate } from '../../../utils/dateFormat';
import DateRange from '../../Shared/DateRange/DateRange';
import useAuth from '../../../hooks/useAuth';

const Customers = () => {
    const { authTokens } = useAuth();

    const [customers, setCustomers] = useState([]);
    const [tableData, setTableData] = useState({});

    const [dateRange, setDateRange] = useState([new Date(), new Date(new Date().setMonth(new Date().getMonth() - 1))]);
    const [startDate, endDate] = dateRange;
    const [validDate, setValidDate] = useState(true)
    const [pending, setPending] = useState(true);


    const columns = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
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
            selector: "subscription__status",
            sortable: true,
            cell: d => d.subscription__status === null ? <span>No</span> : <span>Yes</span>
        }
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
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/customers/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`, {
                headers: {
                    Authorization: 'Bearer ' + String(authTokens?.access)
                }
            })
                .then(res => setCustomers(res.data))
                .then(() => setPending(false))
                .catch(err => console.log(err))
        }
    }, [validDate]);

    useEffect(() => {
        setTableData({ columns: columns, data: customers })
    }, [customers])


    return (
        <Container className="main" style={{ minHeight: '75vh' }}>
            <DateRange startDate={startDate} endDate={endDate} handleDateRange={handleDateRange} />
            <DataTableContainer tableData={tableData} columns={columns} data={customers} pending={pending} />
        </Container>
    );
};

export default Customers;