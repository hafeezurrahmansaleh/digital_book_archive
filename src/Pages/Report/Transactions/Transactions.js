import React, { useEffect, useRef, useState } from 'react';
import DatePicker from "react-datepicker";
import { Container, Form, FormControl, InputGroup } from 'react-bootstrap';
import axios from 'axios';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import { formatDate } from '../../../utils/dateFormat';

const Transactions = () => {
    const [transactions, setTransactions] = useState([]);
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
            selector: "customer_name",
            sortable: true,
            cell: d => d.customer_name === null ? <span>Null</span> : <span>{d.customer_name}</span>
        },
        {
            name: "Payment Method",
            selector: "payment_method",
            sortable: true,
            cell: d => d.payment_method === null ? <span>Null</span> : <span>{d.payment_method}</span>
        },
        {
            name: "Payment Status",
            selector: "payment_status",
            sortable: true,
            cell: d => d.payment_status === null ? <span>Null</span> : <span>{d.payment_status}</span>
        },
        {
            name: "Amount",
            selector: "amount_paid",
            sortable: true,
            cell: d => d.amount_paid === null ? <span>Null</span> : <span>{d.amount_paid}</span>
        },
        {
            name: "Transaction Id",
            selector: "transaction_id",
            sortable: true,
            cell: d => d.transaction_id === null ? <span>Null</span> : <span>{d.transaction_id}</span>
        }
    ];

    const handleDateRange = (update) => {
        if(update[0] !== null && update[1] !== null){
            setValidDate(true);
        }
        else{
            setValidDate(false)
        }
        setDateRange(update)
    }



    useEffect(() => {
        // const data = { filter: option }
        if (validDate){
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/payments/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`)
                .then(res => setTransactions(res.data))
                .catch(err => console.log(err))
        }
    }, [validDate]);

    useEffect(() => {
        setTableData({ columns: columns, data: transactions })
    }, [transactions])

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
            <DataTableContainer tableData={tableData} columns={columns} data={transactions} />
        </Container>
    );
};

export default Transactions;