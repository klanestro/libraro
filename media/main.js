function gotopage(pages, url){
	s = $('#page_input').val();
	try{
		n = eval(s); // Is a number
		if(n <= pages){
			window.location = url + n;	
		}else{
			bdsadasd(); // Raise error if number too big
		}
	}catch(err){
		$('#page_input').val("");
		return;
	}
}

var vortaro = function(){};
vortaro.findword = function(){
	if(vortaro.word == ""){
		return;
	}
	$("#load").css("visibility", "visible");
	//rand = Math.floor(Math.random()*1000001)
	$.getJSON('/dictionary/'+vortaro.word+'/?callback=?', function(data){
		$("#load").css("visibility", "hidden");		
		$("#vortaro-definition").html(data.text);
	});
}
vortaro.close = function(){
	clearTimeout(vortaro.timeout);
	vortaro.timeout = setTimeout(function(){
		$("#vortaro").stop().animate(
		{bottom:"-"+($("#vortaro").height()+1)+"px"},"fast");
	},500);
}
vortaro.timeout = setTimeout("",1);
vortaro.word = "";
vortaro.ready = function(){
	$("#vortaro").mouseenter(function(){
		clearTimeout(vortaro.timeout);
	});
	$("#vortaro").mouseleave(vortaro.close);	
}
// vortaro.register takes a jquery selector and "registers" all of its elements to be
// dictionary clickable.
vortaro.register = function(selector){
	el = $(selector);
	el.click(vortaro.findword);
	el.mouseenter(function(){
		clearTimeout(vortaro.timeout);
		$("#vortaro").stop().animate({bottom:"0px"},"fast");
	});
	el.mouseleave(vortaro.close);
	$(selector + " i").mouseenter(function(){
		vortaro.word = $(this).html();
		$(this).css("background-color","#FFFD9E");
	});
	$(selector + " i").mouseleave(function(){
		vortaro.word = ""
		$(this).css("background-color","white");
	});
}

$(document).ready(function(){vortaro.ready();vortaro.register(".esp");})
