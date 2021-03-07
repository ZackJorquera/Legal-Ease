const express = require('express');
const bodyParser = require('body-parser');
const router = express.Router();
const ejs = require('ejs');
const fetch = require("node-fetch");


const port = process.env.PORT || 8080
const app = express()
app.set('view engine', 'ejs');
app.use(bodyParser.json());

app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
  res.render('index');
});

// app.post("/", function (req, res) {
//     res.render('load');
// });

app.get('/contract', function(req, res) {
  async function fetchData() {
    const response = await fetch("http://localhost:5000/processpdf");
    const data = await response.text();
    return data;
  }
  fetchData().then(data => res.render('return', {data} ));
  // let data = "The Parties, as of the date Eclipse formally approves the Project, Party shall cause any related Domain Names (including all sub-domains and related URLs) to redirect directly to the URLs designated by Eclipse with no interstitial content. Within ten (10) days of the Project Effective Date, Party shall transfer to Eclipse Partys entire right, title and interest to the Domain Names. PARTY MAKES NO WARRANTIES, EXPRESS OR IMPLIED, TO ANY PERSON OR ENTITY WITH RESPECT TO THE TRADEMARKS OR ANY RELATED MATERIALS PROVIDED HEREUNDER, ALL OF WHICH ARE PROVIDED AS IS, AND DISCLAIMS ALL IMPLIED WARRANTIES, INCLUDING WITHOUT LIMITATION WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NONINFRINGEMENT. Eclipse may not assign this Agreement or any of its rights or obligations un. this Agreement without the prior written consent of Party. Each party represents and warrants that it has full right, power and authority to enter into this Agreement and perform all of its obligations hereunder. IN WITNESS WHEREOF, the parties hereto have each caused this Agreement to be executed by their authorized rep";
});

app.get('/loading', function(req, res) {
  res.render('load');
});

app.listen(port)
console.log(`Server listening at http://localhost:${port}`)
