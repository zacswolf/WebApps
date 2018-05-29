var http = require('http'); var server = http.createServer(function(request, response) {
    response.writeHead(200,{"Content-Type": "text/plain"});
    response.end("Hello, World!\n");
});
server.listen(2981);
console.log("Server running at http:\/\/localhost:2481");
