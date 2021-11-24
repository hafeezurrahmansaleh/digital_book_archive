import React, { useEffect, useState } from 'react';
import DatePicker from "react-datepicker";
import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import { formatDate } from '../../../utils/dateFormat';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [tableData, setTableData] = useState({});

    const [dateRange, setDateRange] = useState([new Date(), new Date(new Date().setMonth(new Date().getMonth() - 1))]);
    const [startDate, endDate] = dateRange;
    const [validDate, setValidDate] = useState(true)

    // console.log(customers)

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
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/customers/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`)
                .then(res => setCustomers(res.data))
                .catch(err => console.log(err))
        }
        // axios.get(`http://127.0.0.1:8000/api/v1/dashboard/customers/?month=${('0'+(startDate.getMonth()+1)).slice(-2)}&year=${startDate.getFullYear()}`)
        //     .then(res => setCustomers(res.data))
        //     .catch(err => console.log(err))
    }, [validDate]);

    useEffect(() => {
        setTableData({ columns: columns, data: customers })
    }, [customers])


    return (
        <Container className="main">
            <div className="text-start ms-2 mb-3" style={{ maxWidth: 300 }}>
                <div class="d-flex border">
                    <div class="px-4 fs-6 fw-bold d-flex align-items-center bg-light" id="inputGroup-sizing-default">Range</div>
                    <DatePicker
                        className="border-0"
                        selectsRange={true}
                        startDate={startDate}
                        endDate={endDate}
                        shouldCloseOnSelect={false}
                        onChange={(update) => {
                            // setDateRange(update);
                            handleDateRange(update)
                        }}
                        isClearable={true}
                    />
                </div>
            </div>
            <DataTableContainer tableData={tableData} columns={columns} data={customers} />
        </Container>
    );
};

export default Customers;