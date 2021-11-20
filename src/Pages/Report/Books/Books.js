import React, { useEffect, useState } from 'react';

import { Container } from 'react-bootstrap';
import axios from 'axios';
import StarRatings from 'react-star-ratings';
import DataTableContainer from '../../Shared/DataTableContainer/DataTableContainer';

const Books = () => {
    const [books, setBooks] = useState([]);
    const [tableData, setTableData] = useState({});

    // console.log(customer[4].full_name.toString())

    const columns = [
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


    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/books/',)
            .then(res => setBooks(res.data))
            .catch(err => console.log(err))
    }, []);

    useEffect(() => {
        setTableData({ columns: columns, data: books })
    }, [books])

    // if (Object.keys(tableData).length ){
    //     console.log(Object.keys(tableData).length)
    //     console.log(customer.length)
    //     console.log(tableData)

    // }

    return (
        <Container>
            <DataTableContainer tableData={tableData} columns = {columns} data = {books} />
        </Container>
    );
};

export default Books;