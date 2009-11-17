var Base64 = {
 
	// private property
	_keyStr : "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
 
	// public method for encoding
	encode : function (input) {
		var output = "";
		var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
		var i = 0;
 
		input = Base64._utf8_encode(input);
 
		while (i < input.length) {
 
			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);
 
			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;
 
			if (isNaN(chr2)) {
				enc3 = enc4 = 64;
			} else if (isNaN(chr3)) {
				enc4 = 64;
			}
 
			output = output +
			this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) +
			this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);
 
		}
 
		return output;
	},
 
	// private method for UTF-8 encoding
	_utf8_encode : function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";
 
		for (var n = 0; n < string.length; n++) {
 
			var c = string.charCodeAt(n);
 
			if (c < 128) {
				utftext += String.fromCharCode(c);
			}
			else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			}
			else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}
 
		}
 
		return utftext;
	}
 
}
var ajax;
if(window.XMLHttpRequest){
	// code for IE7+, Firefox, Chrome, Opera, Safari
	ajax = new XMLHttpRequest();
}else if(window.ActiveXObject){
	// code for IE6, IE5
	ajax = new ActiveXObject("Microsoft.XMLHTTP");
}else{
	alert("Your browser does not support XMLHTTP!");
}

function gotopage(pages, url){
	s = document.getElementById('page_input').value;
	try{
		n = eval(s); // Is a number
		if(n <= pages){
			window.location = url + n		
		}else{
			bdsadasd(); // Raise error if number too big
		}
	}catch(err){
		document.getElementById('page_input').value = "";
		return;
	}
}

var showdef = function(){
if(ajax.readyState==4){
  document.getElementById('vortaro-definition').innerHTML = ajax.responseText;
  document.getElementById("load").style.visibility = "hidden";
}}

function askdef(t){
	document.getElementById("load").style.visibility = "visible";
	ajax.open('GET', '/dictionary/'+t, true);
	ajax.onreadystatechange = showdef;
	ajax.send(null);
}

function vortaro(){
if(navigator.appName!='Microsoft Internet Explorer'){
	var t = document.getSelection();
	askdef(t);
}else{
	var t = document.selection.createRange();
	if(document.selection.type == 'Text' && t.text>''){
		document.selection.empty();
		askdef(t.text);
	}
}
}

vortaro.register = function(el){
	el = $(el);
	el.dblclick(vortaro);
	el.mouseenter(function(){
		$("#vortaro").stop().animate({bottom:"0px"},"fast");
	});
	
	el.mouseleave(function(){
		$("#vortaro").stop().animate(
		{bottom:"-"+($("#vortaro").height()+1)+"px"},"fast"
		);
	});
}

$(document).ready(function(){vortaro.register(".esp");})
