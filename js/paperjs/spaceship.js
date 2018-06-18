
var size = view.size;
var circle;
var mouse_position = new Point(0, 0);
var push_state = false;

var circle = new Path.Circle(new Point(size.width / 2, size.height / 2), 20);
circle.fillColor = "white";
circle.strokeColor = "red";
circle.strokeWidth = 2;
circle.vector = new Point(0, 0);

var thrust = new Path(circle.position, new Point(100, 100));
thrust.strokeColor = "red";
thrust.strokeWidth = 2;

var text = new PointText(new Point(10, 20));
text.justification = 'left';
text.fillColor = 'white';

function update(circle_position, mouse_position) {
    circle.position = circle_position;
    thrust.segments[0].point = circle.position;
    thrust.segments[1].point = circle.position + ((mouse_position - circle.position).normalize(20));
}

function push(event) {
    var thrust_vector = (mouse_position - circle.position).normalize(-0.05);
    circle.vector += thrust_vector;

    if (event.count % 5 == 0) {
        var bubble = new Path.Circle(circle.position - thrust_vector.normalize(20), 4);
        //    bubble.fillColor = "black";
        bubble.strokeColor = "red";
        bubble.strokeWidth = 2;
        bubble.data.count = 100;
        bubble.vector = thrust_vector * -30;
        bubble.data.update = function () {
            bubble.strokeColor.brightness -= 0.01;
        }
    }

}

function onMouseMove(event) {
    mouse_position = event.point;
}

function onMouseDown(event) {
    push_state = true;
}

function onMouseUp(event) {
    push_state = false;
}

function onKeyDown(event) {
    if (event.key == "w") {
        push_state = true;
    }
}

function onKeyUp(event) {
    if (event.key == "w") {
        push_state = false;
    }
}

function onFrame(event) {
    if (push_state) {
        push(event);
    }

    project.activeLayer.children.forEach(function (item) {
        if (item.hasOwnProperty("vector")) {
            item.position += item.vector;
/*
            if (item.position.x <= 0) {
                item.position.x = size.width + item.position.x;
            }
            if (item.position.y <= 0) {
                item.position.y = size.height + item.position.y;
            }
            if (item.position.x >= size.width) {
                item.position.x = item.position.x - size.width;
            }
            if (item.position.y >= size.height) {
                item.position.y = item.position.y - size.height;
            }
*/
        }
        if (item.data.update != null) {
            item.data.update();
        }

        if (item.data.count != null) {
            item.data.count -= 1;
            if (item.data.count <= 0) {
                item.remove();
            }
        }
    });

    update(circle.position, mouse_position);

    text.content = "Speed: " + (circle.vector.length * 10).toFixed(0);
}

