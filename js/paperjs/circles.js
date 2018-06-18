
var size = view.size;
var circles = [];

function rand(start, end) {
    return Math.random() * (end - start) + start;
}

function createCircle(center, radius) {
    var circle = new Shape.Circle(center, radius);
    circle.fillColor = "white";
    circle.fillColor.brightness = 1 - (radius / 100);
    circle.strokeColor = "white";
    return circle;
}


for (var i = 0; i < 500; i++) {

    var tries = 0;
    while (tries < 20) {
        tries += 1;
        var center = new Point(size.width, size.height) * Point.random();
        var radius = null;
        circles.forEach(function (other) {
            var distance = other.position.getDistance(center) - other.radius - 2;
            if (radius == null || distance < radius) {
                radius = distance;
            }
        });
        if (radius == null) {
            radius = 20;
        }

        if (radius < 4) {
            continue;
        }
        if (radius > 200) {
            radius = rand(100, 200);
        }
        circles.push(createCircle(center, radius));
        break;
    }
}
