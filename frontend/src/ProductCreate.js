import CategoryService from "./CategoryService";
import React, {Component} from "react";


const categoryService = new CategoryService();

class ProductCreate extends Component {
    x;
    token;
    d;

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.send_create = this.send_create.bind(this);
        this.urlElements = window.location.href.split('/')
        this.state = {error: [], features: [], sended: ''}
    }

    componentDidMount() {
        document.title = 'Add new product'
        categoryService.featuresList(this.urlElements[4], this.urlElements[5]).then(r => {
            if (r.data !== null && r.data !== undefined) {
                this.setState({features: r.data});
            } else {
                this.setState({features: []});
            }
        })
    }

    send_create() {
        this.setState({error: ''})
        const bodyFormData = new FormData();
        this.state.map((k, v) =>
            console.log(this.state.features))
        //bodyFormData.append(k, v))
        // categoryService.getToken().then(rs => {
        //     if (rs.data.token !== undefined) {
        //         categoryService.productCreate(this.state.Name, this.state.Stock, this.state.Desc, this.state.Price, this.features_list, rs.data.token, this.urlElements[4], this.urlElements[5]).then(z => {
        //             if (z.data.error === 'already exists') {
        //                 this.setState({error: 'Catalog already exists!'})
        //                 return true
        //             } else {
        //                 this.setState({error: 'Catalog successfully created!'})
        //                 return true
        //             }
        //         })
        //     } else {
        //         return false
        //     }
        // })
        // return false

    }

    handleSubmit(event) {
        this.send_create()
        event.preventDefault();
    }


    handleChange(event, name) {
        this.setState({features: {[name]: event.target.value}})
        const bodyFormData = new FormData();
        this.state.features.map((k, v) =>
            console.log(this.state.features))
        console.log(bodyFormData)
        event.preventDefault()

    }

    render() {
        return (
            <div>
                <a>{this.state.error}</a>
                <form onSubmit={this.handleSubmit} action='' method='POST'>
                    <p><label>Name:</label><input onChange={r => this.handleChange(r, 'Name')}/></p>
                    <p><label>Price:</label><input type='number' onChange={r => this.handleChange(r, 'Price')}/></p>
                    <p><label>Stock:</label><input type='number' onChange={r => this.handleChange(r, 'Stock')}/></p>
                    <p><label>Description:</label><input onChange={r => this.handleChange(r, 'Desc')}/></p>
                    {this.state.features.map(r =>
                        <p>{r.name}<input
                            onChange={z => this.handleChange(z, [r.name])}/>{r.required ? 'Обязательный:' : 'Необязательный:'}
                        </p>
                    )}
                    <button type='submit'>Submit</button>
                </form>
            </div>
        )
    }
}

export default ProductCreate;