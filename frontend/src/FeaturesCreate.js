import CategoryService from "./CategoryService";
import React, {Component} from "react";


const categoryService = new CategoryService();

class FeaturesCreate extends Component {
    x;
    token;
    d;

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.send_create = this.send_create.bind(this);
        this.urlElements = window.location.href.split('/')
        this.state = {error: [], sended: '', required: false}
    }

    componentDidMount() {
        document.title = 'Add new feature'
    }

    send_create() {
        this.setState({error: ''})
        console.log(this.urlElements)
        categoryService.getToken().then(rs => {
            if (rs.data.token !== undefined) {
                categoryService.productFeaturesCreate(this.state.sended, this.state.required, rs.data.token, this.urlElements[4], this.urlElements[5]).then(z => {
                    alert(z.data.error)
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
                        <label>Feature name</label>
                        <input id='catalog_name' type='text' onChange={this.handleChange}/>
                        <label> Required:</label><input id='catalog_name' defaultChecked={this.state.required} type='checkbox' onChange={r => this.setState({required: !this.state.required})}/>
                    </p>
                    <button type='submit'>Submit</button>
                </form>
            </div>
        )
    }
}

export default FeaturesCreate;