
var size = view.size;
var circles = [];
var screen_center = new Point(size.width / 2, size.height / 2);

function rand(start, end) {
    return Math.random() * (end - start) + start;
}

function createCircle(center, radius) {
    var circle = new Shape.Circle(center, radius);
    circle.fillColor = "white";
//    circle.fillColor.brightness = 1 - (radius / 100);
    circle.strokeColor = "gray";
    return circle;
}


for (var i = 0; i < 1000; i++) {

    var tries = 0;
    while (tries < 20) {
        tries += 1;
        var center = new Point(size.width, size.height) * Point.random();
        var radius = null;
        var required_radius = (1000 - screen_center.getDistance(center))  / 50;
        console.log(required_radius);
        var skip = false;
        circles.forEach(function (other) {
            if (skip) {
                return;
            }
            var distance = other.position.getDistance(center) - other.radius - 2;
            if (radius == null || distance < radius) {
                radius = distance;
            }
            if (radius < required_radius) {
                skip = true;
            }
        });

/*        if (radius > 100) {
            radius = 100;
        }
*/
        if (radius == null) {
            radius = required_radius;
        } else if (radius < required_radius) {
            continue;
        } else {
            radius = required_radius;
        }
        console.log("new");
        circles.push(createCircle(center, radius));
        break;
    }
}
