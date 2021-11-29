import React, { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import axios from 'axios';
import StarRatings from 'react-star-ratings';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';
import { formatDate } from '../../../utils/dateFormat';
import DateRange from '../../Shared/DateRange/DateRange';
import useAuth from '../../../hooks/useAuth';

const Books = () => {
    const { authTokens } = useAuth();

    const [books, setBooks] = useState([]);
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
            axios.get(`http://127.0.0.1:8000/api/v1/dashboard/books/?startDate=${formatDate(startDate)}&endDate=${formatDate(endDate)}`, {
                headers: {
                    Authorization: 'Bearer ' + String(authTokens?.access)
                }
            })
                .then(res => setBooks(res.data))
                .then(() => setPending(false))
                .catch(err => console.log(err))
        }
    }, [validDate]);

    useEffect(() => {
        setTableData({ columns: columns, data: books })
    }, [books])


    return (
        <Container style={{ minHeight: '75vh' }}>
            <DateRange startDate={startDate} endDate={endDate} handleDateRange={handleDateRange} />
            <DataTableContainer tableData={tableData} columns={columns} data={books} pending={pending} />
        </Container>
    );
};

export default Books;