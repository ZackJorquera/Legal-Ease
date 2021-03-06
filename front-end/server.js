const express = require('express')
const bodyParser = require('body-parser')

const port = process.env.PORT || 8080
const app = express()
app.use(express.static(__dirname + '/src'));

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('', async (request, response) => {
  response.send( await readFile(__dirname + '/index.html', 'utf8'));
});

app.listen(port)
console.log(`Server listening at http://localhost:${port}`)
