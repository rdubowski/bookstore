import React, {useEffect, useState} from "react";
import {Form, Button, Row, Col} from "react-bootstrap";
import {useDispatch, useSelector} from "react-redux";
import FormContainer from "../components/FormContainer";
import { saveShippingAdress } from "../actions/cartActions";

function ShippingScreen({history}) {
    const cart = useSelector(state => state.cart)
    const {shippingAdress} = cart
    const dispatch = useDispatch()

    const [adress, setAdress] = useState('')
    const [city, setCity] = useState('')
    const [postalCode, setPostalCode] = useState('')
    const [country, setCountry] = useState( '')
    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(saveShippingAdress({
            adress, city, postalCode, country
        }))
        history.push('/payment')
    }
    return (
        <FormContainer>
            <h1>Shipping</h1>
            <Form onSubmit={submitHandler}>
                 <Form.Group controlId='adress'>
                    <Form.Label>Adress</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter adress'
                        value={adress ? adress : ''}
                        onChange={(e) => setAdress(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>
                 <Form.Group controlId='city'>
                    <Form.Label>Adress</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter city'
                        value={city ? city : ''}
                        onChange={(e) => setCity(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>
                 <Form.Group controlId='postalCode'>
                    <Form.Label>Adress</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter postalCode'
                        value={postalCode ? postalCode : ''}
                        onChange={(e) => setPostalCode(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>
                 <Form.Group controlId='country'>
                    <Form.Label>Adress</Form.Label>
                    <Form.Control
                        required
                        type='text'
                        placeholder='Enter country'
                        value={country ? country : ''}
                        onChange={(e) => setCountry(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>
                <Button type='submit' variant="primary">
                    Continue
                </Button>
            </Form>
        </FormContainer>
    )

}

export default ShippingScreen;