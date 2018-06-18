
var size = view.size;
var circles = [];
var circle;

function rand(start, end) {
    return Math.random() * (end-start) + start;
}

for (var i=0; i<400; i++) {
    var radius = (i /20) + 5;
    circle = new Path.Circle(new Point(rand(0, size.width), rand(0, size.height)), radius);
    circle.fillColor = "white";
    circle.strokeColor = "black";
    circle.vector = new Point(radius / 5, 0);
    circle.radius = radius;
//    circle.fillColor.hue = rand(0, 360);
    circles.push(circle);
}

function onFrame(event) {
    circles.forEach(function(circle) {
//        circle.fillColor.hue += 1;
//        circle.fillColor.brightness = 1- (circle.position.x / size.width);
        circle.position += circle.vector;
        if (circle.position.x > (size.width + circle.radius)) {
            circle.position.x = 0-circle.radius;
        }
    });

}
