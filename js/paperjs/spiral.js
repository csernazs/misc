
var size = view.size;
var circles = [];
var screen_center = new Point(size.width / 2, size.height / 2);
var max_distance = screen_center.getDistance(new Point(-1000, -1000));

var a = 0;
var b = 0.5;

origin = new Point(0, 0);
var point = null;

var i = 0;
while (true) {
    var radius = a + b * i;
    if (radius > max_distance) {
        break;
    }
    var point = new Point(0, radius / 2);
    var rotated = point.rotate(i, origin);
    var absolute = rotated + screen_center;

    var line = Path.Line(new Point(absolute.x - i / 100, absolute.y), new Point(absolute.x + i / 100, absolute.y));
    line.rotate(i + 90, absolute);
    line.strokeColor = "white";
//    var circle = new Path.Circle(absolute, 5)
//    circle.strokeColor = "white";

    i += 1;

}
