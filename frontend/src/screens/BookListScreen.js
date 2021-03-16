import React, {useEffect, useState} from "react";
import {LinkContainer} from "react-router-bootstrap";
import {Table, Button, Row, Col, Card} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import Loader from "../components/Loader";
import Message from "../components/Message";
import { listBooks, deleteBook } from "../actions/bookActions";

function BookListScreen({history, match}) {

    const dispatch = useDispatch()

    const bookList = useSelector(state => state.bookList)
    const {loading, error, books} = bookList

    const bookDelete = useSelector(state => state.bookDelete)
    const {loading:loadingDelete, error:errorDelete, success:successDelete} = bookDelete

    const userLogin = useSelector(state => state.userLogin)
    const {userInfo} = userLogin


    useEffect(() => {
        if(userInfo && userInfo.isAdmin){
        dispatch(listBooks())
        } else {
            history.push('/login')
        }
    }, [dispatch, history, userInfo, successDelete])

    const deleteHandler = (id) => {
        if (window.confirm('Are you sure that you want to delete this book?'))
        {
            dispatch(deleteBook(id))
        }
    }
    const addBookHandler = (book) => {
        // ADd book
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
        {loading
        ? <Loader/>
        : error
        ? (<Message variant="danger">{error}</Message>)
        : (
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
                {books.map(book =>(
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
                            <Button variant='danger' className='btn-sm' onClick={() => deleteHandler(book._id)}>
                                    <i className="fas fa-trash"></i>
                                </Button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </Table>
                )}
    </div>
    )
}

export default BookListScreen;