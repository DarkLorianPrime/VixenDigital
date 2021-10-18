import CategoryService from "./CategoryService";
import React, {Component} from "react";
import {Link} from "react-router-dom";

const categoryService = new CategoryService();

class ProductDisplay extends Component {
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
        if (window.location.href.split('/')[5] !== 'create') {
            categoryService.productList(window.location.href.split('/')[4], window.location.href.split('/')[5]).then(result => {
                if (result.data !== null && result.data !== undefined) {
                    this.setState({category: result.data});
                } else {
                    this.setState({category: []});
                }
            })
        }
    }

    componentDidMount() {
        this.update()
        document.title = 'Category`s'
    }

    delete(id) {
        categoryService.deleteCatalog(id).then(rs => this.update())
    }

    render() {
        this.urlElements = window.location.href.split('/')
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
                        </div>
                    )}
                </div>
            )
        } else {
            return (window.location.href.split('/')[5] !== 'create' && window.location.href.split('/')[4] !== 'create' ?
                (<div className='header'>
                    <Link style={{'fontSize': '30px', 'color': 'white'}} to={this.urlElements[5] + "/create/"}>
                        Новый продукт   </Link>
                    <Link style={{'fontSize': '30px', 'color': 'white'}} to={this.urlElements[5] + "/features/"}>
                        Новые фичи   </Link>
                    <Link style={{'fontSize': '30px', 'color': 'white'}}
                          to='/catalog'>  Home</Link>
                </div>) : (
                    <div className='header'><Link style={{'fontSize': '30px', 'color': 'white'}}
                                                  to='/catalog'> Home</Link>
                    </div>))
        }
    }
}

export default ProductDisplay;