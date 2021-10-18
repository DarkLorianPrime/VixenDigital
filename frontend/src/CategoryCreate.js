import CategoryService from "./CategoryService";
import React, {Component} from "react";


const categoryService = new CategoryService();

class CategoryCreate extends Component {
    x;
    token;
    d;

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.send_create = this.send_create.bind(this);
        this.state = {error: [], sended: ''}
    }

    componentDidMount() {
        document.title = 'Add new catalog'
    }

    send_create() {
        this.setState({error: ''})
        categoryService.getToken().then(rs => {
            if (rs.data.token !== undefined) {
                categoryService.createCategory(this.state.sended, rs.data.token).then(z => {
                    if (z.data.error === 'already exists') {
                        this.setState({error: 'Catalog already exists!'})
                        return true
                    } else {
                        this.setState({error: 'Catalog successfully created!'})
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
                <a>{this.state.error}</a>
                <form onSubmit={this.handleSubmit} action='' method='POST'>
                    <p>
                        <label>Product name</label>
                        <input id='catalog_name' type='text' onChange={this.handleChange}/>
                    </p>
                    <button type='submit'>Submit</button>
                </form>
            </div>
        )
    }
}

export default CategoryCreate;