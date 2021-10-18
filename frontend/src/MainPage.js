import React, {Component} from "react";
import {Link} from "react-router-dom";

class MainPage extends Component {

    constructor(props) {
        super(props);
    }
    componentDidMount() {
        document.title = 'Main Page'
    }
    render() {
        return (
            <div>
                <Link style={{'fontSize': '30px', 'color': 'Black'}} to="/catalog">Каталог</Link>
            </div>
        )
    }
}

export default MainPage;