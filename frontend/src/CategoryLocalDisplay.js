import CategoryService from "./CategoryService";
import React, {Component} from "react";
<<<<<<< Updated upstream

=======
import {Link} from "react-router-dom";
>>>>>>> Stashed changes

const categoryService = new CategoryService();

class CategoryLocalDisplay extends Component {
<<<<<<< Updated upstream
    constructor(props) {
        super(props);
        this.path = this.props.location.pathname
        this.state = {
            category: []
        }
    }

    update() {
        var self = this;
        categoryService.listCategories_local(this.path).then(result => {
            if (result.data !== null && result.data !== undefined) {
                self.setState({category: result.data});
            } else {
                self.setState({category: []});
            }
        })
=======
    url;

    constructor(props) {
        super(props);
        this.path = this.props.location.pathname
        this.urlElements = window.location.href.split('/')
        this.state = {
            category: []
        }
        this.delete = this.delete.bind(this)
    }

    update() {
        if (window.location.href.split('/')[5] !== '/create') {
            categoryService.listCategories_local_without(window.location.href.split('/')[4]).then(result => {
                if (result.data !== null && result.data !== undefined) {
                    this.setState({category: result.data});
                } else {
                    this.setState({category: []});
                }
            })
        }
>>>>>>> Stashed changes
    }

    componentDidMount() {
        this.update()
<<<<<<< Updated upstream
    }

    render() {
        if (this.state.category.length > 0) {
            return (
                <div>
                    {this.state.category.map(c =>
                        <div>
                            <a href={this.path + '/' + c.slug}>{c.name} {c.category__name === null ? <a></a> :
                                <a>Category - {c.category__name}</a>}</a>
=======
        document.title = 'Category`s'
    }

    delete(id) {
        categoryService.deleteCatalog(id).then(rs => this.update())
    }

    render() {
        this.urlElements = window.location.href.split('/')
        console.log(window.location.href.split('/')[4] !== 'create')
        console.log(window.location.href.split('/')[5] === undefined || window.location.href.split('/')[4] !== 'create')
        if (this.state.category.length > 0) {
            return (
                <div>
                    {window.location.href.split('/')[5] === undefined && window.location.href.split('/')[4] !== 'create' ? (
                        <div className='header'>
                            <Link style={{'fontSize': '30px', 'color': 'white', 'margin-right': '30px'}}
                                  to={this.urlElements[4] + "/create/"}>
                                Новый каталог </Link>
                            <Link style={{'fontSize': '30px', 'color': 'white'}} to='/catalog'> Home</Link>
                        </div>
                    ) : (<div/>)}
                    {this.state.category.map(c =>
                        <div className='catalog_button'>
                            <a className='element' href={this.path + '/' + c.slug}>{c.name}</a>
                            <button className='delete_button' style={{
                                'color': 'darkred',
                                'border': 'none',
                                'background-color': 'rgba(255,255,255,0.0)',
                                'cursor': 'pointer'
                            }} onClick={zr => this.delete(c.id)}>X
                            </button>
>>>>>>> Stashed changes
                        </div>
                    )}
                </div>
            )
        } else {
<<<<<<< Updated upstream
            return (
                <div/>
            )
=======
            return (window.location.href.split('/')[5] === undefined && window.location.href.split('/')[4] !== 'create' ?
                (<div className='header'>
                    <Link style={{'fontSize': '30px', 'color': 'white'}} to={this.urlElements[4] + "/create/"}>
                        Новый каталог   </Link>
                    <Link style={{'fontSize': '30px', 'color': 'white'}}
                          to='/catalog'>  Home</Link>
                </div>) : (
                    <div className='header'><Link style={{'fontSize': '30px', 'color': 'white'}}
                                                  to='/catalog'> Home</Link>
                    </div>))
>>>>>>> Stashed changes
        }
    }
}

export default CategoryLocalDisplay;