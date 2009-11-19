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
	$.get('/dictionary/',{"word":vortaro.word}, function(data){
		$("#load").css("visibility", "hidden");		
		$("#vortaro-definition").html(data);
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
vortaro.ready = false;
vortaro.word = "";
vortaro.register = function(el){
	el = $(el);
	el.click(vortaro.findword);
	el.mouseenter(function(){
		clearTimeout(vortaro.timeout);
		$("#vortaro").stop().animate({bottom:"0px"},"fast");
	});
	el.mouseleave(vortaro.close);
	if(!vortaro.ready){
		$("#vortaro").mouseenter(function(){
			clearTimeout(vortaro.timeout);
		});
		$("#vortaro").mouseleave(vortaro.close);
		vortaro.ready = true;
	}
	$("v").mouseenter(function(){
		vortaro.word = $(this).html();
		$(this).css("background-color","#FFFD9E");
	});
	$("v").mouseleave(function(){
		vortaro.word = ""
		$(this).css("background-color","white");
	});
}

$(document).ready(function(){vortaro.register(".esp");})
