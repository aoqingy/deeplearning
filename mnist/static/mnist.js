var MnistObj = function() {
    var canvas = document.getElementById('canvas');      //定义全局画布
    var context = canvas.getContext('2d');               //定义全局context
    var bbox = canvas.getBoundingClientRect();
    var canX = bbox.left;                    //画布左上角的x坐标
    var canY = bbox.top;                     //画布左上角的y坐标
    context.lineCap     = "round";           //线条起始和结尾样式
    context.lineJoin    = "round";           //线条转弯样式
    context.lineWidth   = '25';              //画笔粗细 
    context.strokeStyle = 'white';           //画笔颜色
    var painting = false;                    //初始化设置为不可画状态

function train(scb, ecb) {
    $.ajax({
        url      : '/mnist/train/',
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

var scb_train = function(response) {
    var data = response.message;
    $('#pid-accuracy').val(data.accuracy);
    alert('Succeed!');
}

var ecb_train = function(response) {
    alert('Failed!');
}


function predict(scb, ecb, data) {
    $.ajax({
        url      : '/mnist/predict/',
        type     : 'POST',
        data     : {'data': data},
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

var scb_predict = function(response) {
    var data = response.message;
    alert(data.predict);
}

var ecb_predict = function(response) {
    alert('Failed!');
}

    var handleActions = function() {
        $('body')
        .on('mousedown', '#canvas',
        function(e) {
            e.preventDefault();
            painting = true;                               //鼠标按下可以作画
            context.beginPath();                           //开始作画
            context.moveTo(e.pageX-canX,e.pageY-canY);     //画笔开始位置
            $('#canvas').css('cursor','pointer');           //将鼠标图形设置成小手
        })
        .on('mousemove', '#canvas',
        function(e) {
            e.preventDefault();
            if (painting===true) {                          //判断是否是可绘画状态
                context.lineTo(e.pageX-canX,e.pageY-canY);  //确定线的结束位置
                context.stroke();
            }
        })
        .on('mouseup', '#canvas',
        function(e) {
            e.preventDefault();
            painting = false;                                //鼠标松开，禁止作画
            context.closePath();                             //关闭画笔路径
            $('#canvas').css('cursor','');                    //消除鼠标小手
        })
        .on('mouseleave', '#canvas',
        function(e) {
            e.preventDefault();
            painting = false;                                //离开画布，禁止作画
            context.closePath();                             //关闭画笔路径
            $('#canvas').css('cursor','');                    //消除鼠标小手
        })
        .on('click', '#ptd-train',
        function(e) {
            e.preventDefault();
            var w1 = $('#pid-w1').val();
            var w2 = $('#pid-w2').val();
            var b  = $('#pid-b').val();
            train(scb_train, ecb_train, w1, w2, b);
        })
        .on('click', '#ptd-clear',
        function(e) {
            e.preventDefault();
            context.clearRect(0,0,canvas.width,canvas.height);
        })
        .on('click', '#ptd-predict',
        function(e) {
            e.preventDefault();
            var data = $('#canvas')[0].toDataURL('png');
            predict(scb_predict, ecb_predict, data);
        })
    };

    return {
        init: function() {
            $('#pid-accuracy').val('');
            handleActions();
        }
    };
} ();
