$(document).ready(function() {
	$('#theRedButton').click(function(){
		$("h1,h2,h3").css("color","red");
	})
	$('#theSpeakersButton').click(function(){
		$("#speakerHeading").fadeOut();
	})
})