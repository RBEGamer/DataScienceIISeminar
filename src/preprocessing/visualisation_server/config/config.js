var dotenv = null;
var STATIC_CONFIG = require('./config.json'); //LOAD OUR STATIC CONFIG FROM THE LOCAL FILESYSTEM


var config = {};

//INIT CONFIG OBJECT = STATIC_CONFIG + ENV VARIABLES
function init_config() {
    console.log("init_config");
    console.log(process.env);
    //LOAD A STATIC CONFIG FROM THE config.json
    config = STATIC_CONFIG;
    dotenv = require('dotenv').config();

    //IF WE ARE NOT IN PRODUCTION USE THE .env FILE
    if (process.env.data_server_url) {
        config['data_server_url'] = process.env.data_server_url;
    }




    console.log(config);

}

function set_key(_key, _value) {
    config[String(_key)] = _value;
}

function get_key(_key) {
    return config[String(_key)];
}

module.exports = {
    getConfig: function () {
        return config;
    },
    init_config,
    get_key,
    set_key

}