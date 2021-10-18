import axios from 'axios';

const URL = 'http://localhost:8000'
export default class CategoryService {
    constructor() {
    }

    listCategories() {
        const url_send = `${URL}/`
        return axios.get(url_send)
    }

    listCategories_local(l_url) {
        const url_send = `${URL}/${l_url}/`
        return axios.get(url_send)
    }
<<<<<<< Updated upstream
=======

    listCategories_local_without(l_url) {
        const url_send = `${URL}/${l_url}/`
        return axios.get(url_send)
    }

    getToken() {
        const url_send = `${URL}/`
        const bodyFormData = new FormData();
        bodyFormData.append('name', 'name')
        return axios({method: 'post', url: url_send, data: bodyFormData})
    }

    createCategory(name, token) {
        const url_send = `${URL}/`
        const bodyFormData = new FormData();
        bodyFormData.append('name', name)
        bodyFormData.append('token', token)
        return axios({method: 'post', url: url_send, data: bodyFormData})
    }

    createlocalCategory(name, token, l_url) {
        const url_send = `${URL}/${l_url}/`
        const bodyFormData = new FormData();
        bodyFormData.append('name', name)
        bodyFormData.append('token', token)
        return axios({method: 'post', url: url_send, data: bodyFormData})
    }

    deleteCatalog(id) {
        const url_send = `${URL}/${id}/`
        return axios({method: 'delete', url: url_send, data: {'id': id}})
    }

    productList(catalog, category) {
        const url_send = `${URL}/${catalog}/${category}/`
        return axios({method: 'get', url: url_send})
    }

    featuresList(catalog, category) {
        const url_send = `${URL}/${catalog}/${category}/features/`
        return axios({method: 'get', url: url_send})
    }

    productCreate(name, stock, description, price, features, token, catalog, category) {
        const url_send = `${URL}/${catalog}/${category}/`
        const bodyFormData = new FormData();
        bodyFormData.append('name', name)
        bodyFormData.append('token', token)
        bodyFormData.append('features', features)
        return axios({method: 'post', url: url_send, data: bodyFormData})
    }

    productFeaturesCreate(name, required, token, catalog, category) {
        const url_send = `${URL}/${catalog}/${category}/features/`
        const bodyFormData = new FormData();
        bodyFormData.append('name', name)
        bodyFormData.append('token', token)
        bodyFormData.append('required', required)
        return axios({method: 'post', url: url_send, data: bodyFormData})
    }

>>>>>>> Stashed changes
}