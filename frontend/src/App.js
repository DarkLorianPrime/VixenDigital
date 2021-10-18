<<<<<<< Updated upstream
import logo from './logo.svg';
=======
>>>>>>> Stashed changes
import './App.css';
import CategoryDisplay from './CategoryDisplay'
import {Component} from "react";
import {BrowserRouter, Route} from 'react-router-dom';
<<<<<<< Updated upstream
import CategoryLocalDisplay from "./CategoryLocalDisplay";

const BaseTemplate = () => (
    <div className="App">
        <Route path='/' exact component={CategoryDisplay}/>
        <Route path='/:slug' exact component={CategoryLocalDisplay}/>
    </div>
)

class App extends Component
{
    render()
    {
=======
import CategoryCreate from "./CategoryCreate";
import CategoryLocalDisplay from "./CategoryLocalDisplay";
import CategoryLocalCreate from "./CategoryLocalCreate";
import MainPage from "./MainPage";
import ProductDisplay from "./ProductDisplay";
import FeaturesCreate from "./FeaturesCreate";
import ProductCreate from "./ProductCreate";

const BaseTemplate = () => (

    <div>
        <div className="App">
            <Route path='/catalog' exact component={CategoryDisplay}/>
            <Route path='/catalog/:slug' exact component={CategoryLocalDisplay}/>
            <Route path='/catalog/:slug/create' exact component={CategoryLocalCreate}/>
            <Route path='/catalog/create' exact component={CategoryCreate}/>
            <Route path='/' exact component={MainPage}/>
            <Route path='/catalog/:catalog/:category' exact component={ProductDisplay}/>
            <Route path='/catalog/:catalog/:category/create' exact component={ProductCreate}/>
            <Route path='/catalog/:catalog/:category/features/' exact component={FeaturesCreate}/>
        </div>
    </div>
)

class App extends Component {
    render() {
>>>>>>> Stashed changes
        return (
            <BrowserRouter>
                <BaseTemplate/>
            </BrowserRouter>
        );
    }
}

export default App;
