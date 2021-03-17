import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";
import {Form, Button} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import Loader from "../components/Loader";
import Message from "../components/Message";
import FormContainer from "../components/FormContainer";
import {listBookDetails, updateBook} from "../actions/bookActions";
import {BOOK_UPDATE_RESET} from "../constants/bookConstants";

function BookEditScreen({match, history}) {
    const bookId = match.params.id
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [price, setPrice] = useState(0)
    const [image, setImage] = useState('')
    const [countInStock, setCountInStock] = useState(0)
    const [pagesNum, setPagesNum] = useState('')
    const [ISBN, setISBN] = useState(0)
    const [author, setAuthor] = useState('')
    const [genre, setGenre] = useState('')


    const dispatch = useDispatch()

    const bookDetails = useSelector(state => state.bookDetails)
    const {error, loading, book} = bookDetails

    const bookUpdate = useSelector(state => state.bookUpdate)
    const {error: errorUpdate, loading: loadingUpdate, success: successUpdate} = bookUpdate


    useEffect(() => {
        if (successUpdate) {
            dispatch({type: BOOK_UPDATE_RESET})
            history.push('/admin/books/')
        } else {
            if (!book.name || book._id !== Number(bookId)) {
                dispatch(listBookDetails(bookId))
            } else {
                setName(book.name)
                setDescription(book.description)
                setPrice(book.price)
                setImage(book.image)
                setCountInStock(book.countInStock)
                setAuthor(book.author)
                setGenre(book.genre)
                setISBN(book.ISBN)
                setPagesNum(book.pagesNum)
            }
        }
    }, [dispatch, book, bookId, history, successUpdate])

    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(updateBook({
            _id: bookId,
            name,
            description,
            price,
            image,
            countInStock,
            author,
            genre,
            ISBN,
            pagesNum
        }))
    }

    return (
        <div>
            <Link to='/admin/books'>Go Back</Link>
            <FormContainer>
                <h1>Edit Book</h1>
                {loadingUpdate && <Loader/>}
                {errorUpdate && <Message variant="danger">{errorUpdate}</Message>}
                {loading ? <Loader/> : error ? <Message variant='danger'>{error}</Message> : (
                    <Form onSubmit={submitHandler}>
                        <Form.Group controlId='name'>
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type='name'
                                placeholder='Enter name'
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='description'>
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={5}
                                type='text'
                                placeholder='Enter description'
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='price'>
                            <Form.Label>Price</Form.Label>
                            <Form.Control

                                type='number'
                                placeholder='Enter price'
                                value={price}
                                onChange={(e) => setPrice(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='image'>
                            <Form.Label>Image</Form.Label>
                            <Form.Control

                                type='text'
                                placeholder='Enter image'
                                value={image}
                                onChange={(e) => setImage(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='countInStock'>
                            <Form.Label>Count in stock</Form.Label>
                            <Form.Control

                                type='number'
                                placeholder='Enter count in stock'
                                value={countInStock}
                                onChange={(e) => setCountInStock(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='author'>
                            <Form.Label>Author</Form.Label>
                            <Form.Control

                                type='text'
                                placeholder='Enter author'
                                value={author}
                                onChange={(e) => setAuthor(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='genre'>
                            <Form.Label>Genre</Form.Label>
                            <Form.Control

                                type='text'
                                placeholder='Enter genre'
                                value={genre}
                                onChange={(e) => setGenre(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='pagesNum'>
                            <Form.Label>Number of pages</Form.Label>
                            <Form.Control

                                type='text'
                                placeholder='Enter number of pages'
                                value={pagesNum}
                                onChange={(e) => setPagesNum(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Form.Group controlId='ISBN'>
                            <Form.Label>Number of ISBN</Form.Label>
                            <Form.Control

                                type='text'
                                placeholder='Enter ISBN'
                                value={ISBN}
                                onChange={(e) => setISBN(e.target.value)}
                            >

                            </Form.Control>
                        </Form.Group>
                        <Button type='submit' variant='primary'>
                            Update
                        </Button>
                    </Form>
                )}
            </FormContainer>
        </div>
    )
}

export default BookEditScreen;
