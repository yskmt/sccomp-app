namespace = '/scc'; 

var socket = io.connect('http://' + document.domain + ':' 
                        + location.port + namespace);

socket.on('connect', function() {
    socket.emit('app event', {data: 'I\'m connected!'});
    return false;
});

socket.on('completed image url', function(msg) {
    console.log(msg.img_url + " received");
    $('#result_imgs').append('<img src="' + msg.img_url + '" />');
    $('#status').empty();
    $('#status').append('<br>Calculating (' + msg.status + '/6) ...');

    if (msg.status == 7){
        $('#status').empty();
    }
    return false;
});


window.addEventListener("load", function(){

    $('#myCanvas').css('background-color', 'rgba(255, 255, 255, 1)');

    var drawData = {
        drawFlag : false,
        oldX : 0, // save x-position
        oldY : 0, // save y-position
        brushSize : 1,
        penColor : "rgba(0,0,0, 1)"
    }
    var can = document.getElementById("myCanvas");
    var ctx = can.getContext("2d");

    can.addEventListener("mousemove", function draw(e){
        if (!drawData.drawFlag) return;
        var x = e.clientX;
        var y = e.clientY;
        var can = document.getElementById("myCanvas");
        var context = can.getContext("2d");
        context.strokeStyle = drawData.penColor;
        context.lineWidth = drawData.brushSize;
        context.lineJoin= "round";
        context.lineCap = "round";
        context.beginPath();
        context.moveTo(drawData.oldX, drawData.oldY);
        context.lineTo(x, y);
        context.stroke();
        context.closePath();
        drawData.oldX = x;
        drawData.oldY = y;
    }
    , true);
    can.addEventListener("mousedown", function(e){
        drawData.drawFlag = true;
        drawData.oldX = e.clientX;
        drawData.oldY = e.clientY;
    }, true);
    window.addEventListener("mouseup", function(){  // キャンバスでなくウィンドウに
        drawData.drawFlag = false;
    }, true);
    
    // Slider to change brush size
    $("#slider").slider({
        min: 0,
        max: 100,
        value : 20,
        slide : function(evt, ui){
            drawData.brushSize = ui.value;
        }
    });

    var selected_scene;
    var $scene_images = $('select.images');
    var target_img;
    var img_files = $.getJSON( "static/img_files.json", function(result) {
        $("select.scene")
            .change(function () {
                selected_scene = $("select option:selected").val();

                $scene_images.empty().append(function() {
                    var output = '';
                    $.each(result[selected_scene], function(key, value) {
                        output += '<option>' + key + '</option>';
                    });
                    return output;
                });

                $("select.images").change();

            }).change();

        $("select.images").change(
            function(){
                img_file = result[$("select.scene").val()][$("select.images").val()]
                console.log(img_file);
                loadBackGround(img_file);
                target_img = img_file;
            }
        ).change();

    });

    $("#clear_button").click(function(){
        ctx.clearRect(0, 0, can.width, can.height);
    });
    $("#run_button").click(function(){
        socket.emit('app event', {data: 'run_button_clicked'});
        runCalc(target_img);
        return false;
    });

}, true);


function loadBackGround(img_dir) {
    console.log("url("+img_dir+")");
    $('#myCanvas').css("background-image",
                       "url("+img_dir+")");
}


function runCalc(target_img){
    var can = document.getElementById("myCanvas");
    var d = can.toDataURL("image/png");
    console.log(target_img)
    $('#result_imgs').empty();
    $('#status').append("<br>Calculating (1/6)...");

    socket.emit('mask image',
                {type: "POST",
                 url: "/calculate",
                 data: { 
                     imgBase64: d, 
                     img: target_img
                 }});

    console.log("POST message sent.")

}
