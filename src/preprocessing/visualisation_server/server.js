var express = require('express');
var app = express();
var path = require('path');
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var express = require('express');
var session = require('express-session');//sessions
var bodyParser = require('body-parser');//sessions
var sessionstore = require('sessionstore'); //sessions
var config = require('./config.json'); //include the cofnig file
var uuidv1 = require('uuid/v1'); //gen random uuid times based
var got = require('got');
var randomstring = require("randomstring"); //gen random strings
var fs = require('fs');
var sanitizer = require('sanitizer');
var fileUpload = require('express-fileupload');
var cron = require('node-cron'); //some cronjobs
var listEndpoints = require('express-list-endpoints'); //for rest api explorer
var bcrypt = require('bcrypt'); //for pw hash



var port = process.env.PORT || config.webserver_default_port || 3016;
var hostname = process.env.HOSTNAME || config.hostname || "http://127.0.0.1:" + port + "/";
var appDirectory = require('path').dirname(process.pkg ? process.execPath : (require.main ? require.main.filename : process.argv[0]));
console.log(appDirectory);




//-------- EXPRESS APP SETUP --------------- //
app.set('trust proxy', 1);
app.use(function (req, res, next) {
    if (!req.session) {
        return next(); //handle error
    }
    next(); //otherwise continue
});
app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
// Routing
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
    secret: 'damdkfgnlesfkdgjerinsmegwirhlnks.m',
    store: sessionstore.createSessionStore(),
    resave: true,
    saveUninitialized: true
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(fileUpload());


app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

server.listen(port, function () {
    console.log('Server listening at port %d', port);
});
// ---------------- END EXPRESS SETUP -------------- //


//-------- HELPER FUNCTIONS ---------------//
function generate_random_string() {
    return randomstring.generate({
        length: 13,
        charset: String(Math.round(new Date().getTime() / 1000))
    });
}
//--------END HELPER FUNCTIONS ---------------//
var sess;






app.get('/', function (req, res) {
    res.redirect('/index');
});

app.get('/index', function (req, res) {
    res.render('index.ejs', {
        app_name: config.app_name
    });
});





//---------------- SOCKET IO START ------------- //

io.on('connection', function (socket) {
    console.log('a user connected');
    socket.on('msg', function (msg) {
        console.log(msg);
    });
});





//BROADCAST  socket.broadcast.emit('update', {});


//CRON JOB EVER MINUTE
cron.schedule('* * * * *', () => {
    console.log('running a task every minute');
});






















//---------------------- FOR REST ENDPOINT LISTING ---------------------------------- //
app.get('/rest', function (req, res) {
    res.redirect('/restexplorer.html');
});

//RETURNS A JSON WITH ONLY /rest ENPOINTS TO GENERATE A NICE HTML SITE
var REST_ENDPOINT_PATH_BEGIN_REGEX = "^\/rest\/(.)*$"; //REGEX FOR ALL /rest/* beginning
var REST_API_TITLE = config.app_name | "APP NAME HERE";
var rest_endpoint_regex = new RegExp(REST_ENDPOINT_PATH_BEGIN_REGEX);
var REST_PARAM_REGEX = "\/:(.*)\/"; // FINDS /:id/ /:hallo/test
//HERE YOU CAN ADD ADDITIONAL CALL DESCTIPRION
var REST_ENDPOINTS_DESCRIPTIONS = [
    { endpoints: "/rest/update/:id", text: "UPDATE A VALUES WITH ID" }

];

app.get('/listendpoints', function (req, res) {
    var ep = listEndpoints(app);
    var tmp = [];
    for (let index = 0; index < ep.length; index++) {
        var element = ep[index];
        if (rest_endpoint_regex.test(element.path)) {
            //LOAD OPTIONAL DESCRIPTION
            for (let descindex = 0; descindex < REST_ENDPOINTS_DESCRIPTIONS.length; descindex++) {
                if (REST_ENDPOINTS_DESCRIPTIONS[descindex].endpoints == element.path) {
                    element.desc = REST_ENDPOINTS_DESCRIPTIONS[descindex].text;
                }
            }
            //SEARCH FOR PARAMETERS
            //ONLY REST URL PARAMETERS /:id/ CAN BE PARSED
            //DO A REGEX TO THE FIRST:PARAMETER
            element.url_parameters = [];
            var arr = (String(element.path) + "/").match(REST_PARAM_REGEX);
            if (arr != null) {
                //SPLIT REST BY /
                var splittedParams = String(arr[0]).split("/");
                var cleanedParams = [];
                //CLEAN PARAEMETER BY LOOKING FOR A : -> THAT IS A PARAMETER
                for (let cpIndex = 0; cpIndex < splittedParams.length; cpIndex++) {
                    if (splittedParams[cpIndex].startsWith(':')) {
                        cleanedParams.push(splittedParams[cpIndex].replace(":", "")); //REMOVE :
                    }
                }
                //ADD CLEANED PARAMES TO THE FINAL JOSN OUTPUT
                for (let finalCPIndex = 0; finalCPIndex < cleanedParams.length; finalCPIndex++) {
                    element.url_parameters.push({ name: cleanedParams[finalCPIndex] });

                }
            }
            //ADD ENPOINT SET TO FINAL OUTPUT
            tmp.push(element);
        }
    }
    res.json({ api_name: REST_API_TITLE, endpoints: tmp });
});
