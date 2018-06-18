
var earth = new Path.Circle(new Point(400, 400), 50);
earth.fillColor = "blue";
earth.mass = 5000.0;

var moon = new Path.Circle(new Point(400, 100), 10);
moon.vector = new Point(0.5, 0);
moon.fillColor = "black";
moon.mass = 1.0;

var trace = new Path();
trace.strokeColor = "red";

function onFrame(event) {
    if ((earth.position - moon.position).length > 0.1) {
        gravity = ((earth.mass * moon.mass) / ((earth.position - moon.position).length ^ 2)) * 0.0001;
        force = (earth.position - moon.position).normalize(gravity);
        if (!isNaN(force.x) && isFinite(force.x) && !isNaN(force.y) && isFinite(force.y)) {
            moon.vector += force;
        } else {
            console.log("error");
        }

    }
    moon.position += moon.vector;
    if (moon.vector.length>0.1) {
        trace.add(moon.position);
    }

//            console.log(moon.vector);
}

