var express = require('express'),
    app = express(); // creates an instance of our app // handler for route (i.e. URL) '/'
app.get('/', function(req, res){
    res.send('Hello World from express');
});

// handler for any URL not previously handled
app.get('*', function(req, res){
    res.status(404).send('What was that??? Page Not Found');
});
app.listen(2981); console.log('Express server started on port 2981');
