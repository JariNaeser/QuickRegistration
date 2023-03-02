/*
*   Little REST server user in the QuickRegistration Project.
*
*   Author: Jari Naeser, 2022
*/

// ------------------ VARIABLES AND IMPORTS ------------------

const PORT = 4000;

var express = require("express");
var mysql = require('mysql');
const cors = require("cors");
var app = express();

var connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "root",
    database: "QuickRegistrationDB"
});

// ------------------ CORS SETTINGS ------------------

app.use(cors({ origin: "*" }));

// ------------------ START APP ------------------

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}...`);
});

// ------------------ APP ROUTES ------------------

// Route HTTP di tipo GET
app.get("/getRegisteredUsers", (req, res, next) => {
    //Eseguo la query sul database
    connection.query("SELECT * FROM registeredUsers", function (err, result, fields) {
        if (err) throw err;
        //Ritorno il risultato della query
        res.json(result);
    });
});

app.get("/getUsersWithAccess", (req, res, next) => {
    connection.query("SELECT * FROM usersWithAccess", function (err, result, fields) {
        if (err) throw err;
        res.json(result);
    });
});

// Route HTTP di tipo DELETE
app.delete("/deleteRegisteredUsers", (req, res, next) => {
    connection.query("DELETE FROM registeredUsers", function (err, result, fields) {
        if (err) throw err;
        res.sendStatus(200);
    });
});