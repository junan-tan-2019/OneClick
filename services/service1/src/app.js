const express = require('express')
const bodyParser = require('body-parser')
const { check, validationResult } = require('express-validator')
const urlencodedParser = bodyParser.urlencoded({ extended: false })
const amqp = require('amqplib/callback_api')
require('dotenv').config();
const https = require('https')

const app = express();
const port = 3000;

//option config for sending to lambda function
const options = {
    host: 'yg4mh9htmh.execute-api.ap-southeast-1.amazonaws.com',
    path: '/default/lambda-deployment-production-lambda',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': 'snRBT6lIWo5OJX3URhmFb6aLtpv63hVR9aBBUzwu'
    }
}

//ESTABLISH CONNECTION
var mysql = require('mysql2')
const { stringify } = require('querystring')
// var connection = mysql.createConnection({
//     host: process.env.db_host,
//     user: process.env.db_user,
//     password: process.env.db_password,
//     database: 'registration',
//     port: process.env.db_port
// });
var pool = mysql.createPool({
    host: process.env.db_host,
    user: process.env.db_user,
    password: process.env.db_password,
    database: 'registration',
    port: process.env.db_port
});

process.on('uncaughtException', function (err) {
    console.log(err);
});


//listening on port 3000
app.listen(port, () => {
    console.log("listening on port " + port);
})

app.use(express.static('public'));
// Specific folder example
app.use('/css', express.static(__dirname + 'public/css'))
app.use('/js', express.static(__dirname + 'public/js'))
app.use('/img', express.static(__dirname + 'public/images'))

// // Set View's
app.set('views', './views');
app.set('view engine', 'ejs');

app.get('/health', (req, res) => {
    res.status(200).send('OK');
})

app.get('/register/registerComplete', (req, res) => {
    res.render('registerComplete', { text: 'registered' })
})

app.get('/register/registerIncomplete', (req, res) => {
    res.render('registerIncomplete', { text: 'registered' })
})

app.get('/register', (req, res) => {
    res.render('register', { text: 'registered' })
})

app.post('/register', urlencodedParser, [
    check('uni-ref', 'This uni-ref must be 20+ characters long')
        .exists()
    // .isLength({ min: 20 })
], (req, res) => {

    const errors = validationResult(req)
    if (!errors.isEmpty()) {
        const alert = errors.array()
        res.render('register', {
            alert
        })
    }


    const userJSON = req.body;
    const uniqueRefNum = userJSON['uni-ref'];
    const phoneNumber = userJSON['phone-num'];
    const maskLocation = userJSON['mask-loc'];
    const query = "SELECT UNQREF FROM registration WHERE UNQREF='" + uniqueRefNum + "';";
    console.log(uniqueRefNum);
    
    pool.getConnection(function(err, connection) {
        connection.query(query, function (err, result, fields) {
            if (result.length > 0) {
                if (err) {
                    res.send(err);
                }
                console.log("exists in database");
                res.redirect('/register/registerIncomplete');
            } else {
                console.log("does not exist in database");
                const query2 = "INSERT INTO `registration`(`PHONENUM`, `LOCATION`, `UNQREF`) VALUES (\"" + phoneNumber + "\",\"" + maskLocation + "\",\"" + uniqueRefNum + "\")";
                console.log(query2)
                connection.query(query2, function (err, result, fields) {
                    // if (err) throw err
                    console.log("inserted query")
                })
    
                const rabbitmq_link = process.env.rabbitmq_url_node
                amqp.connect(rabbitmq_link, function (error0, connection) {
                    if (error0) {
                        throw error0;
                    }
                    connection.createChannel(function (error1, channel) {
                        if (error1) {
                            throw error1;
                        }
                        var exchange = 'notifications';
                        channel.assertExchange(exchange, 'topic', {
                            durable: true
                        });
                        var queue = 'collection_num';
                        var msg = "{ \"unique_ref\": \"" + uniqueRefNum + "\", \"location\": \"" + maskLocation + "\", \"phone_number\": \"" + phoneNumber + "\" }";
    
                        channel.assertQueue(queue, {
                            durable: true
                        });
                        channel.bindQueue(queue, exchange, 'unique_ref');
    
                        channel.sendToQueue(queue, Buffer.from(msg));
                        console.log(" [x] Sent %s", msg);
                    });
                });
    
                // creating post request data
                var post_data = JSON.stringify({
                    unique_ref: uniqueRefNum,
                    phone_number: phoneNumber,
                    location: maskLocation
                });
                //creating post request
                var post_req = https.request(options, function (res) {
                    res.setEncoding('utf8');
                    res.on('data', function (chunk) {
                        console.log('Response: ' + chunk);
                    });
                });
                //show error if not working
                post_req.on('error', error => {
                    console.log(error);
                });
                post_req.write(post_data);
                post_req.end();
                console.log("Information send to Service 2");
    
                res.redirect('/register/registerComplete');
            }
    
        })
        pool.releaseConnection(connection);
    });
    
})

