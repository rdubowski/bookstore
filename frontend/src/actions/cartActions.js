import axios from "axios";
import {CART_ADD_ITEM, CART_REMOVE_ITEM, CART_SAVE_SHIPPING_ADRESS} from "../constants/cartConstans";

export const addToCart = (id, qty) => async (dispatch, getState) => {
    const {data} = await axios.get(`/api/books/${id}`)
    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            book: data._id,
            name: data.name,
            image: data.image,
            price: data.price,
            countInStock: data.countInStock,
            qty
        }
    })
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}

export const removeFromCart = (id) => (dispatch, getState) => {
    dispatch({
        type: CART_REMOVE_ITEM,
        payload: id,
    })
    localStorage.setItem(('cartItems'), JSON.stringify((getState().cart.cartItems)))
}

export const saveShippingAdress = (data) => (dispatch) => {
    dispatch({
        type: CART_SAVE_SHIPPING_ADRESS,
        payload: data,
    })
    localStorage.setItem(('shippingAdress'), JSON.stringify(data))
}