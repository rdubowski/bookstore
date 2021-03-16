import React, {useState, useEffect} from 'react'
import {useDispatch, useSelector} from "react-redux";
import {Link} from "react-router-dom";
import {Row, Col, Image, ListGroup, Button, Card, Form} from "react-bootstrap";
import Rating from "../components/Rating";
import Loader from "../components/Loader";
import Message from "../components/Message";
import {listBookDetails} from "../actions/bookActions";

function BookScreen({match, history}) {
    const [qty, setQty] = useState(1)
    const dispatch = useDispatch()
    const bookDetails = useSelector(state => state.bookDetails)
    const {loading, error, book} = bookDetails
    useEffect(() => {
            dispatch(listBookDetails(match.params.id))
        },
        [])
    const addToCartHandler = () => {
        history.push(`/cart/${match.params.id}?qty=${qty}`)
    }
    return (
        <div>
            <Link to='/' className='btn btn-light my-3'>Go back</Link>
            {loading ? <Loader/>
                : error ? <Message variant="danger">{error}</Message>
                    :
                    <Row>
                        <Col md={6}>
                            <Image src={book.image} alt={book.name} fluid/>
                        </Col>
                        <Col md={3}>
                            <ListGroup variant="flush">
                                <ListGroup.Item>
                                    <h3>{book.name}</h3>
                                    {book.author}
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    <Rating value={book.rating} text={`${book.numReviews} reviews`} color={"#f8e825"}/>
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    Price: ${book.price}
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    {book.description}
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    Genre: {book.genre}
                                </ListGroup.Item>
                                <ListGroup.Item>
                                    Number of pages: {book.pagesNum}
                                </ListGroup.Item>
                            </ListGroup>
                        </Col>
                        <Col md={3}>
                            <Card>
                                <ListGroup variant="flush">
                                    <ListGroup.Item>
                                        <Row>
                                            <Col>Price: </Col>
                                            <Col><strong>${book.price}</strong></Col>
                                        </Row>
                                    </ListGroup.Item>
                                    <ListGroup.Item>
                                        <Row>
                                            <Col>Status: </Col>
                                            <Col>{book.countInStock > 0 ? 'In stock' : 'Out of Stock'}</Col>
                                        </Row>
                                    </ListGroup.Item>
                                    {book.countInStock > 0 && (
                                        <ListGroup.Item>
                                            <Row>
                                                <Col>Quantity</Col>
                                                <Col xs='auto' className="my-1">
                                                    <Form.Control
                                                        as="select"
                                                        value={qty}
                                                        onChange={(e) => setQty(e.target.value)}
                                                    >
                                                        {
                                                            [...Array(book.countInStock).keys()].map((x) =>
                                                                <option key={x + 1} value={x + 1}>
                                                                    {x + 1}
                                                                </option>)
                                                        }

                                                    </Form.Control>
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    )}

                                    <ListGroup.Item>
                                        <Button
                                            onClick={addToCartHandler}
                                            className='btn-block'
                                            disabled={book.countInStock == 0}
                                            type='button'>
                                            Add
                                            to
                                            Cart
                                        </Button>
                                    </ListGroup.Item>
                                </ListGroup>
                            </Card>
                        </Col>
                    </Row>
            }
        </div>
    )
}

export default BookScreen;