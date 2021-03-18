import React, {useState, useEffect} from 'react'
import {useDispatch, useSelector} from "react-redux";
import {Link} from "react-router-dom";
import {Row, Col, Image, ListGroup, Button, Card, Form} from "react-bootstrap";
import Rating from "../components/Rating";
import Loader from "../components/Loader";
import Message from "../components/Message";
import {listBookDetails, createBookReview} from "../actions/bookActions";
import {BOOK_CREATE_REVIEW_RESET} from "../constants/bookConstants";

function BookScreen({match, history}) {
    const [qty, setQty] = useState(1)
    const [rating, setRating] = useState(0)
    const [comment, setComment] = useState("")

    const dispatch = useDispatch()

    const bookDetails = useSelector(state => state.bookDetails)
    const {loading, error, book} = bookDetails

    const userLogin = useSelector(state => state.userLogin)
    const {userInfo} = userLogin

    const bookReviewCreate = useSelector(state => state.bookReviewCreate)
    const {success: successBookReview, loading: loadingBookReview, error: errorBookReview} = bookReviewCreate
    useEffect(() => {
        if (successBookReview) {
            setRating(0)
            setComment('')
            dispatch({type: BOOK_CREATE_REVIEW_RESET})
        }
        dispatch(listBookDetails(match.params.id))

        },
        [dispatch, match, successBookReview])
    const addToCartHandler = () => {
        history.push(`/cart/${match.params.id}?qty=${qty}`)
    }
    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(createBookReview(
            match.params.id, {
                rating,
                comment
            }
        ))
    }
    return (
        <div>
            <Link to='/' className='btn btn-light my-3'>Go back</Link>
            {loading ? <Loader/>
                : error ? <Message variant="danger">{error}</Message>
                    : (
                        <div>
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
                                            <Rating value={book.rating} text={`${book.numReviews} reviews`}
                                                    color={"#f8e825"}/>
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
                            <Row>
                                <Col md={6} className="mt-5">
                                    <h4>Reviews</h4>
                                    {book.reviews.length === 0 && <Message variant="info">No Reviews</Message>}
                                    <ListGroup variant="flush">
                                        {book.reviews.map((review) => (
                                            <ListGroup.Item key={review._id}>
                                                <strong>{review.name}</strong>
                                                <Rating value={review.rating} color='#f8e825'/>
                                                <p>{review.createdAt.substring(0, 10)}</p>
                                                <p>{review.comment}</p>
                                            </ListGroup.Item>
                                        ))}
                                        <ListGroup.Item>
                                            <h4>Write a review</h4>
                                            {loadingBookReview && <Loader/>}
                                            {successBookReview && <Message variant='success'>Review submitted</Message>}
                                            {errorBookReview && <Message variant='danger'>{errorBookReview}</Message>}
                                            {userInfo ? (
                                                <Form onSubmit={submitHandler}>
                                                    <Form.Group>
                                                        <Form.Label>Rating</Form.Label>
                                                        <Form.Control as="select"
                                                                      value={rating}
                                                                      onChange={
                                                                          (e) => setRating(e.target.value)
                                                                      }>
                                                            <option value=''>Select...</option>
                                                            <option value='1'>1 - Poor</option>
                                                            <option value='2'>2 - Fair</option>
                                                            <option value='3'>3 - Good</option>
                                                            <option value='4'>4 - Very Good</option>
                                                            <option value='5'>5 - Excelent</option>
                                                        </Form.Control>
                                                    </Form.Group>
                                                    <Form.Group controlId='comment'>
                                                        <Form.Label>Review</Form.Label>
                                                        <Form.Control
                                                            as='textarea'
                                                            row='5'
                                                            value={comment}
                                                            onChange={(e) => setComment(e.target.value)}>
                                                        </Form.Control>
                                                    </Form.Group>
                                                    <Button
                                                        disabled={loadingBookReview}
                                                        type='submit'
                                                        variant='primary'

                                                    >Submit</Button>
                                                </Form>
                                            ) : (
                                                <Message variant="info">
                                                    Please <Link to='/login'>Login</Link> to write a review.
                                                </Message>
                                            )}
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Col>
                            </Row>
                        </div>
                    )
            }
        </div>
    )
}

export default BookScreen;
