import React, { useEffect, useState } from 'react';
import DatePicker from "react-datepicker";
import { Container } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [tableData, setTableData] = useState({});
    const [startDate, setStartDate] = useState(new Date());

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
        axios.get(`http://127.0.0.1:8000/api/v1/dashboard/customers/?month=${('0'+(startDate.getMonth()+1)).slice(-2)}&year=${startDate.getFullYear()}`)
            .then(res => setCustomers(res.data))
            .catch(err => console.log(err))
    }, [startDate]);

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
            <div className="text-start ms-2 mb-3" style={{ maxWidth: 300 }}>
                <div class="d-flex border">
                    <div class="px-4 fs-6 fw-bold d-flex align-items-center bg-light" id="inputGroup-sizing-default">Month</div>
                    <DatePicker
                        className="form-control border-0 fs-6"
                        selected={startDate}
                        onChange={(date) => setStartDate(date)}
                        dateFormat="MM/yyyy"
                        showMonthYearPicker
                    />
                </div>

            </div>
            <DataTableContainer tableData={tableData} columns={columns} data={customers} />
        </Container>
    );
};

export default Customers;