const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
let { User } = require('./user');
const crypto = require('crypto');
const path = require('path')

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

const tmp_user = {}

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader;
    if (tmp_user.secretKey == undefined) {
        tmp_user.secretKey = crypto.randomBytes(16).toString('hex');
    }
    if (!token) {
        return res.redirect('/login');
    }
    try {
        const decoded = jwt.verify(token, tmp_user.secretKey);
        req.user = decoded;
        next();
    } catch (ex) {
        return res.status(400).send('Invalid token.');
    }
}

const merge = (a, b) => {
    for (var c in b) {
        console.log(JSON.stringify(b[c]));
        if (check(b[c])) {
            if (a.hasOwnProperty(c) && b.hasOwnProperty(c) && typeof a[c] === 'object' && typeof b[c] === 'object') {
                merge(a[c], b[c]);
            } else {
                a[c] = b[c];
            }
        } else {
            return 0
        }
    }
    return a
}

console.log(tmp_user.secretKey)

var check = function (str) {
    let input = /const|var|let|return|subprocess|Array|constructor|load|push|mainModule|from|buffer|process|child_process|main|require|exec|this|eval|while|for|function|hex|char|base|"|'|\\|\[|\+|\*/ig;
    
    if (typeof str === 'object' && str !== null) {
        for (let key in str) {
            if (!check(key)) {
                return false;
            }
            if (!check(str[key])) {
                return false;
            }
        }
        return true;
    } else {
        return !input.test(str);
    }
};

app.get('/login', (req, res) => {
    res.render('login')
});

app.post('/login', (req, res) => {
    if (merge(tmp_user, req.body)) {
        if (tmp_user.secretKey == undefined) {
            tmp_user.secretKey = crypto.randomBytes(16).toString('hex');
        }
        if (User.verifyLogin(tmp_user.password)) {
            const token = jwt.sign({ username: tmp_user.username }, tmp_user.secretKey);
            res.send(`Login successful! Token: ${token}\nBut nothing happend~`);
        } else {
            res.send('Login failed!');
        }
    } else {
        res.send("Hacker denied!")
    }
});

app.get('/', (req, res) => {
    authenticateToken(req, res, () => {
        backcode = eval(tmp_user.code)
        res.send("something happend~")
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});