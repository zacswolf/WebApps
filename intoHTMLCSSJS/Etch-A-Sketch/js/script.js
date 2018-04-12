// builds grid of numRows x numCols <div> elements
var c = "black";

var buildEtch = function(sz) {
    $(".container").empty();
	var boxSize = $('.container').height() / sz;
	console.log("boxSize =",boxSize);

	

    
    for(var i = 0; i < sz;i++){
        $('.container').append("<div class = 'row'></div>");
    }
    for(var j = 0; j < sz;j++){
        $('.row').append("<div class = 'cell'></div>");
    }
    $(".row").css("height", boxSize);
    $(".cell").css("height", boxSize);
    $(".cell").css("width", boxSize);
    $(".cell").css("float", "left");
    $(".cell").hover(function(){
        if (c === "rand"){
            $(this).css("background-color","#"+((1<<24)*Math.random()|0).toString(16));
        } else {
            $(this).css("background-color", c);
        }
    })
};

$(document).ready(function() {
    $(".buttons").append('<button type="button" class="newButt" id="black"></button>');
    $(".buttons").append('<button type="button" class="newButt" id="red"></button>');
    $(".buttons").append('<button type="button" class="newButt" id="blue"></button>');
    $(".buttons").append('<button type="button" class="newButt" id="yellow"></button>');
    $(".buttons").append('<button type="button" class="newButt" id="rand">Random<br>Colors</button>');
    $("#black").css("background-color", "black");
    $("#red").css("background-color", "red");
    $("#blue").css("background-color", "blue");
    $("#yellow").css("background-color", "yellow");

    $("button").click(function(){
        if ($(this).attr('id') === "rand"){
            c = "rand";
        } else {
            c = $(this).css("background-color");
        }
    })

    $('#resChange').click(function() {
        haveSize = false;
        while (haveSize === false) {
            oldSize = size;
            size = prompt("Please enter a grid size from 1-128");
            if (size > 0 && size <= 128) {
                haveSize = true
            } else if (size === null) {
                size = oldSize;
                haveSize = true
            } else {
                alert("The number you entered is outside the range!")
            };
        };
        c = "black";
        buildEtch(size);
    });

    size = 50;
    buildEtch(size)
})
