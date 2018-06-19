
var earth = new Path.Circle(new Point(400, 400), 50);
earth.fillColor = "blue";
earth.mass = 50000.0;

var moon_radius = 10;
var moon = new Path.Circle(new Point(400, 100), moon_radius);
moon.vector = new Point(0.3, 0);
moon.fillColor = "black";
moon.mass = 1.0;

var moon_vector = new Path(moon.position, new Point(100, 100));
moon_vector.strokeColor = "blue";
moon_vector.strokeWidth = 3;

var force_vector = new Path(moon.position, new Point(100, 100));
force_vector.strokeColor = "green";
force_vector.strokeWidth = 5;

var connection = new Path(earth.position, moon.position);
connection.strokeColor = "grey";
connection.strokeWidth = 1;


var trace = new Path();
trace.strokeColor = "red";

var paused = false;

function onMouseDown() {
    paused = ! paused;
}
function onFrame(event) {
    if (paused) {
        return;
    }

    if ((earth.position - moon.position).length > 0.1) {
        gravity = ((earth.mass * moon.mass) / (Math.pow(earth.position.getDistance(moon.position), 2))) * 0.001;
        force = (earth.position - moon.position).normalize(gravity);
        if (!isNaN(force.x) && isFinite(force.x) && !isNaN(force.y) && isFinite(force.y)) {
            moon.vector += force;
        } else {
            console.log("error");
        }

    } else {
        console.log("collision?");
    }

    moon.position += moon.vector;

    moon_vector.segments[0].point = moon.position;
    moon_vector.segments[1].point = moon.position + moon.vector.normalize(moon.vector.length * 10);

    force_vector.segments[0].point = moon.position;
    force_vector.segments[1].point = moon.position + force.normalize(force.length * 10);

    connection.segments[1].point = moon.position;

    if (moon.vector.length > 0.1) {
        trace.add(moon.position);
    }
}

