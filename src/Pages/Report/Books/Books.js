import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import StarRatings from 'react-star-ratings';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import ReactDatePicker from 'react-datepicker';
import { formatDate } from '../../../utils/dateFormat';

const Books = () => {
    const [books, setBooks] = useState([]);
    const [tableData, setTableData] = useState({});

    const [dateRange, setDateRange] = useState([new Date(), new Date(new Date().setMonth(new Date().getMonth() - 1))]);
    const [startDate, endDate] = dateRange;
    const [validDate, setValidDate] = useState(true)

    // console.log(customer[4].full_name.toString())

    const columns = [
        {
            name: '#',
            cell: (row, index) => <span>{index + 1}</span>
        },
        {
            name: "Book Name",
            selector: "book_name",
            sortable: true,
            cell: d => d.book_name === null ? <span>Null</span> : <span>{d.book_name}</span>
        },
        {
            name: "Author Name",
            selector: "author_name",
            sortable: true,
            cell: d => d.author_name === null ? <span>Null</span> : <span>{d.author_name}</span>
        },
        {
            name: "Publisher Name",
            selector: "publisher_name",
            sortable: true,
            cell: d => d.publisher_name === null ? <span>Null</span> : <span>{d.publisher_name}</span>
        },
        {
            name: "Rating",
            selector: "rating",
            sortable: true,
            cell: d => d.rating === null ? <span>Null</span> : <StarRatings
                rating={parseFloat(d.rating)}
                starRatedColor="goldenrod"
                starDimension="20px"
                starSpacing="2px"
            />
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
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/books/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`)
                .then(res => setBooks(res.data))
                .catch(err => console.log(err))
        }
        // axios.get('http://127.0.0.1:8000/api/v1/dashboard/books/',)
        //     .then(res => setBooks(res.data))
        //     .catch(err => console.log(err))
    }, [validDate]);

    useEffect(() => {
        setTableData({ columns: columns, data: books })
    }, [books])


    return (
        <Container>
            <div className="text-start ms-2 mb-3" style={{ maxWidth: 300 }}>
                <div class="d-flex border">
                    <div class="px-4 fs-6 fw-bold d-flex align-items-center bg-light" id="inputGroup-sizing-default">Range</div>
                    <ReactDatePicker
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
            <DataTableContainer tableData={tableData} columns = {columns} data = {books} />
        </Container>
    );
};

export default Books;