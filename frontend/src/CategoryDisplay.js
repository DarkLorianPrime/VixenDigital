import CategoryService from "./CategoryService";
import React, {Component} from "react";
<<<<<<< Updated upstream
=======
import {Link} from "react-router-dom";
>>>>>>> Stashed changes


const categoryService = new CategoryService();
let returnobj = []

class CategoryDisplay extends Component {
    constructor(props) {
        super(props);
        this.state = {
<<<<<<< Updated upstream
            category: []
        }
=======
            category: [],
            temporary: [],
            temporary_slug: ''
        }
        this.delete = this.delete.bind(this)
>>>>>>> Stashed changes
    }


    update() {
        categoryService.listCategories().then(result => {
            if (result.data !== null && result.data !== undefined) {
                this.setState({category: result.data});
            } else {
                this.setState({category: []});
            }
        })
    }

    componentDidMount() {
        this.update()
<<<<<<< Updated upstream
    }

    render_dop(slug) {
        if (this.state[slug] === undefined) {
            categoryService.listCategories_local(slug).then(result => {
                if (result.data !== null && result.data !== undefined) {
                    returnobj[slug] = result.data
                    this.setState({[slug]: returnobj[slug]})
                } else {
                    this.setState({[slug]: [this.state[slug]]})
                }

            });
        } else {
            this.setState({[slug]: returnobj[slug]})
        }
    }

    disrender_dop(slug) {
        this.setState({[slug]: []})
    }

    render() {
        if (this.state.category.length > 0) {
            return (
                <div>
                    <div class='header'>
                        <a style={{'font-size': '80px'}}>Каталог</a>
                    </div>
                    {this.state.category.map(c =>
                        <div>
                            <div class='main_button' onMouseEnter={event => this.render_dop(c.slug)}
                                 onMouseLeave={event => this.disrender_dop(c.slug)}>
                                <a class='react_func' href={c.slug}>{c.name}</a>
                                {this.state[c.slug] !== undefined ? this.state[c.slug].map(c =>
                                    <div style={{'float': 'right'}} class='left-window'>
                                        <a>{c.name}</a>
                                    </div>
                                ) : <a></a>}
                            </div>
                        </div>
                    )}
=======
        document.title = 'Catalogs'
    }

    render_dop(slug) {
        if (returnobj[slug] === undefined) {
            if (this.state.temporary_slug !== slug) {
                categoryService.listCategories_local(slug).then(r => {
                        if (r.data !== null && r.data !== undefined && r.data !== this.state.temporary) {
                            returnobj[slug] = r.data
                            this.setState({temporary: r.data});
                            this.setState({temporary_slug: slug})
                        }
                    }
                )
            }
        } else {
            this.setState({temporary: returnobj[slug]});
            this.setState({temporary_slug: slug})
        }
    }

    delete(id) {
        categoryService.deleteCatalog(id).then(rs => this.update())
    }

    render() {
        this.fz = 0
        if (this.state.category.length > 0) {
            return (
                <div>
                    <div className='header'>
                        <Link style={{'fontSize': '30px', 'color': 'white'}} to="/catalog/create">Новый каталог</Link>
                    </div>
                    <div style={{'marginRight': '50px', 'width': '50%', 'display': 'inline-block'}}>
                        {this.state.category.map(c => (
                            <div className='catalog_button' onMouseEnter={zr => this.render_dop(c.slug)}>
                                <a className='react_func' href={'/catalog/' + c.slug}>{c.name} </a>
                                <button className='delete_button' style={{
                                    'color': 'darkred',
                                    'border': 'none',
                                    'background-color': 'rgba(255,255,255,0.0)',
                                    'cursor': 'pointer'
                                }} onClick={zr => this.delete(c.id)}>X
                                </button>
                            </div>
                        ))}
                    </div>
                    <div style={{'display': 'inline-block'}} className='content-catalogs'>
                        <a><p>Самые популярные категории</p></a>
                        {this.state.temporary.map(c => (this.fz <= 8 ?

                            (this.fz = this.fz + 1, <p><a href={this.state.temporary_slug + '/' + c.slug}
                                                          className='element'>>{c.name}</a></p>) : (<a/>)))}
                    </div>

>>>>>>> Stashed changes
                </div>
            )
        } else {
            return (
<<<<<<< Updated upstream
                <div/>
=======
                <div className='header'>
                    <Link style={{'fontSize': '30px', 'color': 'white'}} to="/create">Новый каталог</Link>
                </div>
>>>>>>> Stashed changes
            )
        }

    }
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
}

export default CategoryDisplay;