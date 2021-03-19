import React, {useState, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {Row, Col} from 'react-bootstrap';
import Book from '../components/Book'
import Loader from "../components/Loader";
import Message from "../components/Message";
import Paginate from "../components/Paginate";
import {listBooks} from "../actions/bookActions";
import BookCarousel from "../components/BookCarousel";

function HomeScreen({history}) {
    const dispatch = useDispatch()
    const bookList = useSelector(state => state.bookList)
    const {error, loading, books, page, pages} = bookList
    let keyword = history.location.search
    useEffect(() => {
            dispatch(listBooks(keyword))
        },
        [dispatch, keyword])
    return (
        <div>
            {!keyword && <BookCarousel />}
            <h1>Latest Books</h1>
            {loading ? <Loader/>
                : error ? <Message variant="danger">{error}</Message>
                    :
                    <div>

                        <Row>
                            {books.map(book => (
                                <Col key={book._id} sm={12} md={6} lg={4} xl={3}>
                                    <Book book={book}/>
                                </Col>
                            ))}
                        </Row>
                        <Paginate page={page} pages={pages} keyword={keyword} />
                    </div>
            }

        </div>
    )
}

export default HomeScreen;