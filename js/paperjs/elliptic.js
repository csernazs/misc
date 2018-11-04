

function circle(center, radius) {
    var retval = new Path.Circle(center, radius);
    retval.fillColor = "white";
    return retval;
}

var a = -10;
var b = 5;

var y;

function onFrame() {


    project.activeLayer.removeChildren();
    a = a + 0.05;
    for (var x = -3; x < 3; x = x + 0.01) {
        y = Math.sqrt(a * x + b + Math.pow(x, 3));
        console.log(y);
        circle(new Point(200 + x * 50, view.size.height / 2 - y * 50), 1);
        circle(new Point(200 + x * 50, view.size.height / 2 + y * 50), 1);

    }
}
