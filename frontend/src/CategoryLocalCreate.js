import CategoryService from "./CategoryService";
import React, {Component} from "react";
import {Link} from "react-router-dom";

const categoryService = new CategoryService();

class CategoryLocalCreate extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.send_create = this.send_create.bind(this);
        this.state = {error: [], sended: ''}
        this.path = this.props.location.pathname
    }
    urlElements = window.location.href.split('/')
    componentDidMount() {
        document.title = 'Add new category on ' + this.urlElements[4]
    }

    send_create() {
        this.setState({error: ''})
        categoryService.getToken().then(rs => {
            if (rs.data.token !== undefined) {
                console.log(window.location.href.split('/'))
                categoryService.createlocalCategory(this.state.sended, rs.data.token, window.location.href.split('/')[4]).then(z => {
                    if (z.data.error === 'already exists') {
                        this.setState({error: 'Category already exists!'})
                        return true
                    } else {
                        this.setState({error: 'Category successfully created!'})
                        return true
                    }
                })
            } else {
                return false
            }
        })
        return false

    }

    handleSubmit(event) {
        this.send_create()
        event.preventDefault();
    }


    handleChange(event) {
        this.setState({sended: event.target.value})
        event.preventDefault()

    }

    render() {

        return (
            <div>
                <div>
                    <Link style={{'font-size': '30px', 'text-align': 'right'}} to={"/catalog/" + this.urlElements[4]}>Home</Link>
                </div>
                <a>{this.state.error}</a>
                <form onSubmit={this.handleSubmit} action='' method='POST'>
                    <p><label>Category name</label> <input id='catalog_name' type='text' onChange={this.handleChange}/>
                    </p>
                    <button type='submit'>Submit</button>
                </form>
            </div>
        )
    }
}

export default CategoryLocalCreate;