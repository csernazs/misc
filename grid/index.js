
var express = require('express')
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http)


var fill = function(rows, cols) {
  var retval = Array(rows);
  for (rowidx = 0; rowidx<rows; rowidx++) {
    var row = Array(cols).fill(0);
    retval[rowidx] = row;
  }
  return retval;
}

var grid = fill(20, 20);

var flip = function(rowidx, colidx) {
  var cell = grid[rowidx][colidx];
  if (cell == 0) {
    grid[rowidx][colidx] = 1;
  } else {
    grid[rowidx][colidx] = 0;
  }
}

app.get('/', function(req, res){
  res.sendFile(__dirname + "/index.html")
});

app.get('/state', function(req, res){
  res.setHeader('Content-Type', 'application/json');
  res.send(JSON.stringify(grid));
});

app.use('/assets/spectre', express.static(__dirname + '/node_modules/spectre.css/dist'));

io.on('connection', function(socket) {
  console.log('a user connected');

  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
  socket.on('flip', function(msg) {
    console.log('message: ' + msg);
    flip(msg[0], msg[1]);
    socket.broadcast.emit('flip', msg);
  });
})

http.listen(3000, function(){
  console.log('listening on *:3000');
});
