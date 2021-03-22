import {Container} from 'react-bootstrap';
import {BrowserRouter as Router, Route} from "react-router-dom";
import Header from './components/Header';
import Footer from './components/Footer';
import HomeScreen from "./screens/HomeScreen";
import BookScreen from "./screens/BookScreen";
import CartScreen from "./screens/CartScreen";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";
import ProfileScreen from "./screens/ProfileScreen";
import ShippingScreen from "./screens/ShippingScreen";
import PaymentScreen from "./screens/PaymentScreen";
import PlaceOrderScreen from "./screens/PlaceOrderScreen";
import OrderScreen from "./screens/OrderScreen";
import UserListScreen from "./screens/UserListScreen";
import UserEditScreen from "./screens/UserEditScreen"
import BookListScreen from "./screens/BookListScreen";
import BookEditScreen from "./screens/BookEditScreen";
import OrderListScreen from "./screens/OrderListScreen";
function App() {
    return (
        <Router>
            <Header/>
            <main className="py-3">
                <Container>
                    <Route path='/' component={HomeScreen} exact/>
                    <Route path='/books/:id' component={BookScreen} exact/>
                    <Route path='/books/author/:id/' component={HomeScreen} exact/>
                    <Route path='/cart/:id?' component={CartScreen}/>
                    <Route path='/login' component={LoginScreen}/>
                    <Route path='/register' component={RegisterScreen}/>
                    <Route path='/profile' component={ProfileScreen}/>
                    <Route path='/shipping' component={ShippingScreen}/>
                    <Route path='/payment' component={PaymentScreen}/>
                    <Route path='/placeorder' component={PlaceOrderScreen}/>
                    <Route path='/order/:id' component={OrderScreen}/>
                    <Route path='/admin/userslist' component={UserListScreen}/>
                    <Route path='/admin/user/:id/edit' component={UserEditScreen}/>
                    <Route path='/admin/books/' component={BookListScreen}/>
                    <Route path='/admin/book/:id/edit' component={BookEditScreen}/>
                    <Route path='/admin/orderslist/' component={OrderListScreen}/>
                </Container>
            </main>
            <Footer/>
        </Router>
    );
}

export default App;
