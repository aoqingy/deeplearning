var MnistObj = function() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');

    HORIZONTAL_AXIS_MARGIN = 10,
    VERTICAL_AXIS_MARGIN = 10,

    AXIS_ORIGIN = { x: canvas.width/2, y: canvas.height/2 },

    AXIS_LEFT   = HORIZONTAL_AXIS_MARGIN,
    AXIS_RIGHT  = canvas.width-HORIZONTAL_AXIS_MARGIN,
    AXIS_TOP    = VERTICAL_AXIS_MARGIN,
    AXIS_BOTTOM = canvas.height-VERTICAL_AXIS_MARGIN,

    HORIZONTAL_TICK_SPACING = 10,
    VERTICAL_TICK_SPACING = 10,

    AXIS_WIDTH  = AXIS_RIGHT - AXIS_LEFT,
    AXIS_HEIGHT = AXIS_BOTTOM - AXIS_TOP,

    NUM_VERTICAL_TICKS   = AXIS_HEIGHT / VERTICAL_TICK_SPACING,
    NUM_HORIZONTAL_TICKS = AXIS_WIDTH  / HORIZONTAL_TICK_SPACING,

    TICK_WIDTH = 10,

    SPACE_BETWEEN_LABELS_AND_AXIS =  20;

    function windowToCanvas(canvas, x, y) {
        var bbox = canvas.getBoundingClientRect();
        var orgx = x - bbox.left * (canvas.width  / bbox.width);
        var orgy = y - bbox.top  * (canvas.height / bbox.height);
        return { x: orgx, y: orgy };
    }

    function drawAxes() {
        context.save(); 
        context.lineWidth = 1.0;
        context.fillStyle = 'rgba(100, 140, 230, 0.8)';
        context.strokeStyle = 'navy';

        drawHorizontalAxis();
        drawVerticalAxis();

        context.lineWidth = 0.5;
        context.strokeStyle = 'navy';

        context.strokeStyle = 'darkred';
        drawVerticalAxisTicks();
        drawHorizontalAxisTicks();

        context.restore();
    }

    function drawVerticalAxisTicks() {
        var deltaY;
   
        for (var i=1; i < NUM_VERTICAL_TICKS / 2; ++i) {
            if (i % 5 === 0) deltaX = TICK_WIDTH;
            else             deltaX = TICK_WIDTH/2;
              
            context.beginPath();
            context.moveTo(AXIS_ORIGIN.x - deltaX, AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
            context.lineTo(AXIS_ORIGIN.x + deltaX, AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
            context.stroke();
        }
        for (var i=1; i < NUM_VERTICAL_TICKS / 2; ++i) {
            if (i % 5 === 0) deltaX = TICK_WIDTH;
            else             deltaX = TICK_WIDTH/2;

            context.beginPath();
            context.moveTo(AXIS_ORIGIN.x - deltaX, AXIS_ORIGIN.y + i * VERTICAL_TICK_SPACING);
            context.lineTo(AXIS_ORIGIN.x + deltaX, AXIS_ORIGIN.y + i * VERTICAL_TICK_SPACING);
            context.stroke();
        }
    }

    function drawHorizontalAxisTicks() {
        var deltaY;
   
        for (var i=1; i < NUM_HORIZONTAL_TICKS / 2; ++i) {
             if (i % 5 === 0) deltaY = TICK_WIDTH;
             else             deltaY = TICK_WIDTH/2;
              
             context.beginPath();
             context.moveTo(AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y - deltaY);
             context.lineTo(AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y + deltaY);
             context.stroke();
        }
        for (var i=1; i < NUM_HORIZONTAL_TICKS / 2; ++i) {
            if (i % 5 === 0) deltaY = TICK_WIDTH;
            else             deltaY = TICK_WIDTH/2;

            context.beginPath();
            context.moveTo(AXIS_ORIGIN.x - i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y - deltaY);
            context.lineTo(AXIS_ORIGIN.x - i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y + deltaY);
            context.stroke();
        }
    }

    function drawHorizontalAxis() {
        context.beginPath();
        context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
        context.lineTo(AXIS_RIGHT,    AXIS_ORIGIN.y)
        context.stroke();
        context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
        context.lineTo(AXIS_LEFT,     AXIS_ORIGIN.y)
        context.stroke();
    }

    function drawVerticalAxis() {
        context.beginPath();
        context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
        context.lineTo(AXIS_ORIGIN.x, AXIS_TOP);
        context.stroke();
        context.moveTo(AXIS_ORIGIN.x, AXIS_ORIGIN.y);
        context.lineTo(AXIS_ORIGIN.x, AXIS_BOTTOM);
        context.stroke();
    }

    function drawAxisLabels() {
        context.fillStyle = 'blue';
        drawHorizontalAxisLabels();
        drawVerticalAxisLabels();
    }

    function drawHorizontalAxisLabels() {
        context.textAlign = 'center';
        context.textBaseline = 'top';
   
        for (var i=0; i <= NUM_HORIZONTAL_TICKS / 2; ++i) {
            if (i % 5 === 0) {
                context.fillText(i/100.0, AXIS_ORIGIN.x + i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y + SPACE_BETWEEN_LABELS_AND_AXIS);
            }
        }
        for (var i=0; i <= NUM_HORIZONTAL_TICKS / 2; ++i) {
            if (i % 5 === 0) {
                context.fillText(-i/100.0, AXIS_ORIGIN.x - i * HORIZONTAL_TICK_SPACING, AXIS_ORIGIN.y + SPACE_BETWEEN_LABELS_AND_AXIS);
            }
        }
    }

    function drawVerticalAxisLabels() {
        context.textAlign = 'right';
        context.textBaseline = 'middle';

        for (var i=0; i <= NUM_VERTICAL_TICKS / 2; ++i) {
            if (i % 5 === 0) {
                context.fillText(i/100.0, AXIS_ORIGIN.x - SPACE_BETWEEN_LABELS_AND_AXIS, AXIS_ORIGIN.y - i * VERTICAL_TICK_SPACING);
            }
        }
        for (var i=0; i <= NUM_VERTICAL_TICKS / 2; ++i) {
            if (i % 5 === 0) {
                context.fillText(-i/100.0, AXIS_ORIGIN.x - SPACE_BETWEEN_LABELS_AND_AXIS, AXIS_ORIGIN.y + i * VERTICAL_TICK_SPACING);
            }
        }
    }

    function drawGrid(color, stepx, stepy) {
        context.save()

        context.strokeStyle = color;
        context.fillStyle = '#ffffff';
        context.lineWidth = 0.5;
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);

        for (var i = stepx + 0.5; i < context.canvas.width; i += stepx) {
            context.beginPath();
            context.moveTo(i, 0);
            context.lineTo(i, context.canvas.height);
            context.stroke();
        }

        for (var i = stepy + 0.5; i < context.canvas.height; i += stepy) {
            context.beginPath();
            context.moveTo(0, i);
            context.lineTo(context.canvas.width, i);
            context.stroke();
        }

        context.restore();
    }

function sampleDot(scb, ecb, x1, x2, y) {
    $.ajax({
        url      : '/logistic/sampleDot/',
        type     : 'POST',
        data     : {'x1': x1, 'x2': x2, 'y': y},
        dataType : 'json',
        success  : function (response) {
            if (response.code == "True") {
                scb(response);
            } else {
                ecb(response);
            }
        },
        error    : function() {
            alert('获取终端列表失败！');
        }
    });
}

var scb_sampleDot = function(response) {
    var data = response.message;
    var x1 = parseFloat(data.x1)*100.0+1024/2;
    var x2 = parseFloat(data.x2)*100.0+768/2;
    context.beginPath();
    context.arc(x1, x2, 5, 0, Math.PI*2, false);
    if (parseInt(data.y) == 1) {
        context.fillStyle = 'blue';
    } else {
        context.fillStyle = 'red';
    }
    context.fill();
    context.closePath();
}


var ecb_sampleDot = function(response) {
    alert("Failed");
}

function trainDot(scb, ecb, w1, w2, b) {
    $.ajax({     
        url      : '/logistic/trainDot/',
        type     : 'POST',
        data     : {'w1': w1, 'w2': w2, 'b': b},
        dataType : 'json',
        success  : function (response) { 
            if (response.code == "True") {
                scb(response);
            } else {
                ecb(response);
            }
        },
        error    : function() {
            alert('获取终端列表失败！');
        }
    });
}

var scb_trainDot = function(response) {
    var data = response.message;
    $('#pid-w1').val(data.w1);
    $('#pid-w2').val(data.w2);
    $('#pid-b').val(data.b);
    $('#pid-cost').val(data.cost);
    repaint();
    //w1*x1+w2*x2*b=0
    context.beginPath();
    sx = -1024/2;
    sy = parseInt(-(sx/100.0*parseFloat(data.w1)+parseFloat(data.b))*100.0/parseFloat(data.w2));
    context.moveTo(sx+AXIS_ORIGIN.x, sy+AXIS_ORIGIN.y);
    sx = 1024/2;
    sy = parseInt(-(sx/100.0*parseFloat(data.w1)+parseFloat(data.b))*100.0/parseFloat(data.w2));
    context.lineWidth = 5;
    context.lineTo(sx+AXIS_ORIGIN.x, sy+AXIS_ORIGIN.y);
    context.stroke();
    context.closePath();
}


var ecb_trainDot = function(response) {
    alert("Failed");
}

function listDots(scb, ecb) {
    $.ajax({
        url      : '/logistic/listDots/',
        type     : 'POST',
        data     : {},
        dataType : 'json',
        success  : function (response) {
            if (response.code == "True") {
                scb(response);
            } else {
                ecb(response);
            }
        },
        error    : function() {
            alert('获取终端列表失败！');
        }
    });
}

var scb_listDots = function(response) {
    var data = response.message;
    for (var i = 0; i < data.length; i++) {
        var x1 = parseFloat(data[i].x1)*100.0+1024/2;
        var x2 = parseFloat(data[i].x2)*100.0+768/2;
        context.beginPath();
        context.arc(x1, x2, 5, 0, Math.PI*2, false);
        if (parseInt(data[i].y) == 1) {
            context.fillStyle = 'blue';
        } else {
            context.fillStyle = 'red';
        }
        context.fill();
        context.closePath();
    }
}

var ecb_listDots = function(response) {
    alert('Failed!');
}

function deleteDot(scb, ecb, x, y) {
    $.ajax({
        url      : '/logistic/clearDots/',
        type     : 'POST',
        data     : {},
        dataType : 'json',
        success  : function (response) {
            if (response.code == "True") {
                scb(response);
            } else {
                ecb(response);
            }
        },
        error    : function() {
            alert('获取终端列表失败！');
        }
    });
}

var scb_deleteDot = function(response) {
    var data = response.message;
    repaint();
}


var ecb_deleteDot = function(response) {
    alert("Failed");
}

var scb_listDots2 = function(response) {
    var data = response.message;
    var dots = '';
    for (var i = 0; i < data.length; i++) {
        if (dots != '') {
            dots += '\n';
        }
        dots += data[i].x1 + ',' + data[i].x2 + ',' + data[i].y;
    }
    alert(dots);
}

var ecb_listDots2 = function(response) {
    alert("Failed");
}

    var handleActions = function() {
        $('body')
        .on('mousedown', '#canvas',
        function(e) {
            e.preventDefault();
            var loc = windowToCanvas(canvas, e.clientX, e.clientY);
            var y   = $('#ptd-class').val();
            if (y == '') {
                return;
            }
            var x1 = (loc.x - 1024/2) / 100.0;
            var x2 = (loc.y - 768/2) / 100.0;
            sampleDot(scb_sampleDot, ecb_sampleDot, x1, x2, y);
        })
        .on('click', '#ptd-train',
        function(e) {
            e.preventDefault();
            var w1 = $('#pid-w1').val();
            var w2 = $('#pid-w2').val();
            var b  = $('#pid-b').val();
            trainDot(scb_trainDot, ecb_trainDot, w1, w2, b);
        })
        .on('click', '#ptd-clear',
        function(e) {
            e.preventDefault();
            deleteDot(scb_deleteDot, ecb_deleteDot);
        })
        .on('click', '#ptd-predict',
        function(e) {
            e.preventDefault();
            listDots(scb_listDots2, ecb_listDots2);
        })
    };

    var drawBackground = function() {
        context.font = '13px Arial';
        drawGrid('lightgray', 10, 10);
        context.shadowColor = 'rgba(100, 140, 230, 0.8)';
        context.shadowOffsetX = 3;
        context.shadowOffsetY = 3;
        context.shadowBlur = 5;
        drawAxes();
        drawAxisLabels();
    };

    var repaint = function() {
        drawBackground();
        listDots(scb_listDots, ecb_listDots);
    }

    return {
        init: function() {
            $('#pid-w1').val('');
            $('#pid-w2').val('');
            $('#pid-b').val('');
            $('#pid-cost').val('');
            repaint();
            handleActions();
        }
    };
} ();
