
var size = view.size;
var circles = [];
var hovering = null;
var mouse_action = null;
var mouse_selected = null;
var separation = 10;
var minimum_radius = 10;

function rand(start, end) {
    return Math.random() * (end - start) + start;
}

function onMouseDown(event) {
    if (mouse_selected == null && hovering == null) {
        var max_radius = get_max_radius(null, event.point);
        if (max_radius > minimum_radius) {
            circles.push(createCircle(event.point, max_radius));
        }
    }
}

function onMouseUp() {
    mouse_action = null;
    mouse_selected = null;
}

function get_max_radius(circle, position) {
    var max_radius = null;

    console.log(position);
    if (position == undefined) {
        position = circle.position;
    }

    circles.forEach(function (other) {
        if (other === circle) {
            return;
        }
        var local_max_radius = other.position.getDistance(position) - other.radius - separation;
        if (max_radius == null || local_max_radius < max_radius) {
            max_radius = local_max_radius;
        }
    });
    return max_radius;
}
function set_radius(circle, radius) {
    var max_radius = get_max_radius(circle);
    if (max_radius >= radius) {
        circle.radius = radius;
    } else {
        circle.radius = max_radius;
    }

};

function set_position(circle, position) {
    var max_radius = get_max_radius(circle, position);
    if (max_radius <= circle.radius) {
        if (max_radius > minimum_radius) {
            circle.radius = max_radius * 0.99;
        }
    } else {
        circle.position = position;
    }
}

function createCircle(center, radius) {
    var circle = new Shape.Circle(center, radius);
    circle.fillColor = "white";

    function hover() {
        circle.strokeColor = "red";
        circle.strokeWidth = 2;
        hovering = circle;
    }

    function idle() {
        circle.strokeColor = "white";
        circle.strokeWidth = 2;
        hovering = null;
    }

    idle();

    circle.onMouseEnter = function (event) {
        if (mouse_selected == null || mouse_selected == circle) {
            hover();
        }
    }

    circle.onMouseLeave = function (event) {
        if (mouse_selected == null || mouse_selected != circle) {
            idle();
        }
    }

    circle.onDoubleClick = function (event) {
        set_radius(circle, 80000);
        event.stopPropagation();
    }

    circle.onMouseDrag = function (event) {
        if (mouse_selected == null) {
            mouse_selected = circle;
        }
        if (mouse_selected != circle) {
            return;
        }
        if (mouse_action == null) {
            if (event.point.getDistance(mouse_selected.position) > mouse_selected.radius * 0.8) {
                mouse_action = "resize";
            } else {
                mouse_action = "move";
            }

        }
        if (mouse_action == "resize") {
            set_radius(mouse_selected, event.point.getDistance(mouse_selected.position));
        } else if (mouse_action == "move") {
            set_position(mouse_selected, mouse_selected.position + event.delta);
        }
    }
    return circle;
}


circles = [
    createCircle(new Point(size.width / 2 - 150, size.height / 2), 50),
    createCircle(new Point(size.width / 2 + 150, size.height / 2), 50),
];