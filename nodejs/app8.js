var express = require('express'),
    app = express(),
    cons = require('consolidate'),
    crypto = require('crypto'),
    MongoClient = require('mongodb').MongoClient; 

app.engine('html', cons.swig); 
app.set('view engine', 'html'); 
app.set('views', __dirname + '/views'); 

MongoClient.connect('mongodb:\/\/localhost:2481\/mydb', function(err, db) {
    if(err) throw err;
    app.get('/', function(req, res){
        db.collection('greeting').findOne(function(err, doc) {
            if(err) throw err;
            if (!doc) {
                console.dir("No document found");
                return db.close();
            }
            return res.render('hello',{name: doc['location']});
        });
    });
    app.get('*', function(req, res){
        return res.send('Page Not Found', 404);
    });
    app.listen(2981);
    console.log('Express server started on port 2981');
});
