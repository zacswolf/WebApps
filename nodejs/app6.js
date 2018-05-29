var express = require('express'), cons = require('consolidate'), app = express(); 
// creates an instance of our app 
app.engine('html',cons.swig); // set SWIG as the template engine 
app.set('view engine', 'html'); // set express view engine 
app.set('views',__dirname + '/views'); // set directory for views 
// handler for route (i.e. URL) '/' 
app.get('/', function(req, res){
    res.render('hello',{name: 'World from swig'});
});
// handler for any URL not previously handled 
app.get('*', function(req, res){
    res.status(404).send('What was that??? Page Not Found');
});
app.listen(2981);
console.log('Express server started on port 2981');
