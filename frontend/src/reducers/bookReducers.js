import {
    BOOK_LIST_REQUEST,
    BOOK_LIST_SUCCESS,
    BOOK_LIST_FAIL,
    BOOK_DETAILS_REQUEST,
    BOOK_DETAILS_SUCCESS,
    BOOK_DETAILS_FAIL,
    BOOK_DELETE_REQUEST,
    BOOK_DELETE_SUCCESS,
    BOOK_DELETE_FAIL,
    BOOK_ADD_REQUEST,
    BOOK_ADD_SUCCESS,
    BOOK_ADD_FAIL,
    BOOK_ADD_RESET,
    BOOK_UPDATE_REQUEST,
    BOOK_UPDATE_SUCCESS,
    BOOK_UPDATE_FAIL,
    BOOK_UPDATE_RESET,
} from "../constants/bookConstants";

export const bookListReducer =
    (state = {books: []}, action) => {
        switch (action.type) {
            case BOOK_LIST_REQUEST:
                return {loading: true, books: []}
            case BOOK_LIST_SUCCESS:
                return {loading: false, books: action.payload}
            case BOOK_LIST_FAIL:
                return {loading: false, error: action.payload}
            default:
                return state
        }
    }

export const bookDetailsReducer =
    (state = {book: {reviews: []}}, action) => {
        switch (action.type) {
            case BOOK_DETAILS_REQUEST:
                return {loading: true, ...state}
            case BOOK_DETAILS_SUCCESS:
                return {loading: false, book: action.payload}
            case BOOK_DETAILS_FAIL:
                return {loading: false, error: action.payload}
            default:
                return state
        }
    }

export const bookDeleteReducer =
    (state = {}, action) => {
        switch (action.type) {
            case BOOK_DELETE_REQUEST:
                return {loading: true,}
            case BOOK_DELETE_SUCCESS:
                return {loading: false, success: true}
            case BOOK_DELETE_FAIL:
                return {loading: false, error: action.payload}
            default:
                return state
        }
    }
export const bookAddReducer =
    (state = {}, action) => {
        switch (action.type) {
            case BOOK_ADD_REQUEST:
                return {loading: true,}
            case BOOK_ADD_SUCCESS:
                return {loading: false, success: true, book: action.payload}
            case BOOK_ADD_FAIL:
                return {loading: false, error: action.payload}
            case BOOK_ADD_RESET:
                return {}
            default:
                return state
        }
    }
export const bookUpdateReducer =
    (state = {book: {}}, action) => {
        switch (action.type) {
            case BOOK_UPDATE_REQUEST:
                return {loading: true,}
            case BOOK_UPDATE_SUCCESS:
                return {loading: false, success: true, book: action.payload}
            case BOOK_UPDATE_FAIL:
                return {loading: false, error: action.payload}
            case BOOK_UPDATE_RESET:
                return {book: {}}
            default:
                return state
        }
    }