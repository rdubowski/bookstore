import React, {useEffect, useState} from "react";
import {LinkContainer} from "react-router-bootstrap";
import {Table, Button, Row, Col, Card} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import Loader from "../components/Loader";
import Message from "../components/Message";
import Paginate from "../components/Paginate";
import {listBooks, deleteBook, addBook} from "../actions/bookActions";
import {BOOK_ADD_RESET} from "../constants/bookConstants";

function BookListScreen({history, match}) {

    const dispatch = useDispatch()

    const bookList = useSelector(state => state.bookList)
    const {loading, error, books, pages, page} = bookList

    const bookDelete = useSelector(state => state.bookDelete)
    const {loading: loadingDelete, error: errorDelete, success: successDelete} = bookDelete

    const bookAdd = useSelector(state => state.bookAdd)
    const {loading: loadingAdd, error: errorAdd, success: successAdd, book: addedBook} = bookAdd

    const userLogin = useSelector(state => state.userLogin)
    const {userInfo} = userLogin

    let keyword = history.location.search
    useEffect(() => {
        dispatch({type: BOOK_ADD_RESET})
        if (!userInfo.isAdmin) {
            history.push('/login')
        }
        if (successAdd) {
            history.push(`/admin/book/${addedBook._id}/edit`)
        } else {
            dispatch(listBooks(keyword))
        }
    }, [dispatch, history, userInfo, successDelete, successAdd, addedBook, keyword])

    const deleteHandler = (id) => {
        if (window.confirm('Are you sure that you want to delete this book?')) {
            dispatch(deleteBook(id))
        }
    }
    const addBookHandler = (book) => {
        dispatch(addBook())
    }
    return (
        <div>
            <Row className='align-items-center'>
                <Col>
                    <h1>Books</h1>
                </Col>
                <Col className='text-right'>
                    <Button className='my-3' onClick={addBookHandler}>
                        <i className='fas fa-plus'></i> Add book
                    </Button>
                </Col>
            </Row>
            {loadingDelete && <Loader/>}
            {errorDelete && <Message variant="danger">{errorDelete}</Message>}
            {loadingAdd && <Loader/>}
            {errorAdd && <Message variant="danger">{errorAdd}</Message>}
            {loading
                ? <Loader/>
                : error
                    ? (<Message variant="danger">{error}</Message>)
                    : (
                        <div>
                            <Table striped bordered hover responsive className="table-sm">
                                <thead>
                                <tr>

                                    <th>ID</th>
                                    <th>NAME</th>
                                    <th>PRICE</th>
                                    <th>GENRE</th>
                                    <th>AUTHOR</th>
                                    <th></th>
                                </tr>
                                </thead>
                                <tbody>
                                {books.map(book => (
                                    <tr key={book._id}>
                                        <td>{book._id}</td>
                                        <td>{book.name}</td>
                                        <td>${book.price}</td>
                                        <td>{book.genre}</td>
                                        <td>{book.author}</td>
                                        <td>
                                            <LinkContainer to={`/admin/book/${book._id}/edit`}>
                                                <Button variant='light' className='btn-sm'>
                                                    <i className="fas fa-edit"></i>
                                                </Button>
                                            </LinkContainer>
                                            <Button variant='danger' className='btn-sm'
                                                    onClick={() => deleteHandler(book._id)}>
                                                <i className="fas fa-trash"></i>
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </Table>
                            <Paginate pages={pages} page={page} isAdmin={true}/>
                        </div>
                    )}
        </div>
    )
}

export default BookListScreen;
