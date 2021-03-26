import React, {useState, useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {Row, Col} from 'react-bootstrap';
import Book from '../components/Book'
import Loader from "../components/Loader";
import Message from "../components/Message";
import Paginate from "../components/Paginate";
import {listBooks, listBooksByAuthor} from "../actions/bookActions";
import BookCarousel from "../components/BookCarousel";

function HomeScreen({history, match}) {
    const authorId = match.params.id
    const dispatch = useDispatch()

    const bookListByAuthor = useSelector(state => state.listBooksByAuthor)
    const {error: bookListByAuthorError, loading: bookListByAuthorLoading, books: booksByAuthor} = bookListByAuthor

    const bookList = useSelector(state => state.bookList)
    const {error, loading, books, page, pages} = bookList
    let keyword = history.location.search
    useEffect(() => {
            if (match.params.id) {
                dispatch(listBooksByAuthor(match.params.id))
            } else {
                dispatch(listBooks(keyword))
            }
        },
        [dispatch, keyword, authorId])
    return (
        <div>
            {!authorId && !keyword && <BookCarousel/>}
            {authorId ? <div>
                    {bookListByAuthorLoading ? <Loader/>
                        : bookListByAuthorError ? <Message variant="danger">{error}</Message>
                            :
                            <div>

                                <Row>
                                    {booksByAuthor.map(book => (
                                        <Col key={book._id} sm={12} md={6} lg={4} xl={3}>
                                            <Book book={book}/>
                                        </Col>
                                    ))}
                                </Row>
                            </div>
                    }

                </div> :

                <div>

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
                                <Paginate page={page} pages={pages} keyword={keyword}/>
                            </div>
                    }

                </div>
            }
        </div>
    )
}

export default HomeScreen;