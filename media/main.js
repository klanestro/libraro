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
	var word;
	if(window.getSelection){ // Real browsers
		word = window.getSelection();
	}else{ // Internet Explorer
		word = document.selection.createRange().text;
	}
	$("#load").css("visibility", "visible");
	$.get('/dictionary/'+word, function(data){
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
vortaro.register = function(el){
	el = $(el);
	el.dblclick(vortaro.findword);
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
}

$(document).ready(function(){vortaro.register(".esp");})
