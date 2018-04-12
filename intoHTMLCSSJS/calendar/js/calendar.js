
function mouse(element){
	element.onmouseover = function() {
		if (element.style.backgroundColor !== 'silver'){
			element.style.backgroundColor = 'red';
		}
	};

	element.onmouseout = function() {
		if (element.style.backgroundColor !== 'silver'){
			element.style.backgroundColor = 'gold';
		}
	};
	element.onclick = function() {
		elements = document.getElementsByClassName("day");
    	for (var i = 0; i < elements.length; i++) {
        	elements[i].style.backgroundColor="gold";
    	}
		element.style.backgroundColor = 'silver';

	};
}
var monthList = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

function main() {


	var yearDrop = document.createElement("select");
	yearDrop.id = "yeardrop";
	yearDrop.options.length = 2017-1900+1;
	var j = 0
	for (var i=2017;i>=1900;i--){
		yearDrop.options[j].innerHTML = i;
		j++;
	}
	yearDrop.onchange = updateS
	document.body.insertBefore(yearDrop, document.body.childNodes[1]);


	var monthDrop = document.createElement("select");
	monthDrop.id = "monthdrop";
	monthDrop.options.length = 12;
	monthDrop.options[0].innerHTML = monthList[0];
	monthDrop.options[1].innerHTML = monthList[1];
	monthDrop.options[2].innerHTML = monthList[2];
	monthDrop.options[3].innerHTML = monthList[3];
	monthDrop.options[4].innerHTML = monthList[4];
	monthDrop.options[5].innerHTML = monthList[5];
	monthDrop.options[6].innerHTML = monthList[6];
	monthDrop.options[7].innerHTML = monthList[7];
	monthDrop.options[8].innerHTML = monthList[8];
	monthDrop.options[9].innerHTML = monthList[9];
	monthDrop.options[10].innerHTML = monthList[10];
	monthDrop.options[11].innerHTML = monthList[11];
	monthDrop.onchange = updateS
	document.body.insertBefore(monthDrop, document.body.childNodes[2]);
	document.getElementById("monthdrop").value = "Sept";
	updateS();




	
}



function updateS(){
	var monthNum = monthList.indexOf(document.getElementById("monthdrop").value)
	var d = new Date(document.getElementById("yeardrop").value,monthNum,1);
	console.log(d);
	var f = new Date(document.getElementById("yeardrop").value,monthNum+1,0);
	console.log(f.getDate());

	while (document.getElementById("month").firstChild) {
    	document.getElementById("month").removeChild(document.getElementById("month").firstChild);
	}

	make(d.getDay(),f.getDate());
}


function make(numBlank,numDay){
	for(var i=0;i<7;i++){
		var element = document.createElement("div");
		element.className = "dayLabel";
		var h = document.createElement("H1")                // Create a <h1> element
		switch(i) {
    		case 0:
    			h.appendChild(document.createTextNode("Sun"));
        	break;
    		case 1:
        		h.appendChild(document.createTextNode('Mon'));
        	break;
        	case 2:
        		h.appendChild(document.createTextNode('Tue'));
        	break;
        	case 3:
        		h.appendChild(document.createTextNode('Wed'));
        	break;
        	case 4:
        		h.appendChild(document.createTextNode('Thu'));
        	break;
        	case 5:
        		h.appendChild(document.createTextNode('Fri'));
        	break;
        	case 6:
        		h.appendChild(document.createTextNode('Sat'));
        	break;
    		default:
        		alert("Error 1");
		}
		element.appendChild(h);
		document.getElementById("month").appendChild(element);

	}
	for(var num=0; num < numBlank; num++){
		var element = document.createElement("div");
		element.className = "emptyday";
		document.getElementById("month").appendChild(element);
	}

	for(var day=0;day<numDay;day++){
		var element = document.createElement("div");
		element.className = "day";
		var h = document.createElement("H1");
		h.appendChild(document.createTextNode(day+1)); 
		element.appendChild(h);
		mouse(element);

		document.getElementById("month").appendChild(element);


	}
}


window.onload = main();








