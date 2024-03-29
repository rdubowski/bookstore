import React from 'react';
import {Card} from 'react-bootstrap';
import Rating from './Rating'
import {Link} from 'react-router-dom'

function Book({book}) {
    return (
        <Card className="my-3 p-3 rounded" style={{height: '570px'}}>
            <Link to={`/books/${book._id}`}>
                <Card.Img src={book.image}/>
            </Link>
            <Card.Body>
                <Link to={`/books/${book._id}`}>
                    <Card.Title>
                        <strong>{book.name}</strong>
                    </Card.Title>
                </Link>
                    {book.author && book.author.map((auth, index, arr) => {
                        return (<Link to={`/books/author/${auth.id}/`}>
                            {index === arr.length-1 ? auth.name : `${auth.name}, `}
                        </Link>)
                    })
                    }
                <Card.Text as="div">
                    <div className="my-3">
                        <Rating value={book.rating} text={`${book.numReviews} reviews`} color={'#f8e825'}/>
                    </div>
                </Card.Text>
                <Card.Text as="h3">
                    ${book.price}
                </Card.Text>
            </Card.Body>
        </Card>
    )
}

export default Book;