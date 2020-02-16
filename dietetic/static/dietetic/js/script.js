//     return card if the user click

var $dietetic_text = $('#dietetic_text');
$dietetic_text.hide();

var $card = $('#card');
$card.on('click', function() {
    $dietetic_text.show();
    $card.css('background-image', "url('../../static/dietetic/img/back_face.jpg')");
});


//     logo nav animation

const color = {
  	user: ["/account/my_account/", "30,0,200"],
  	poll: ["/dietetic/my_results/", "30,0,200"],
  	home: ["/", "30,0,200"],
  	clipboard: ["/dietetic/dietetic_space/", "30,0,200"],
};
for (elt in color){
    var $logo_url = color.elt[0];
    var $url = window.location.pathname;
    if ($url == $logo_url) {
        alert(color.elt)
  	    var $logo = $("#"+color.elt+"");
  	    var $color = color.elt[1];
  	    $logo.css('color', "rgb("+$color+")");
  	    $logo.css('background-color', "rgb("+$color+")");
    }
}


//     works ok
var $url = window.location.pathname;
if ($url == "/account/my_account/") {
  	var $user = $('#user');
  	$user.css('color', "rgb(52, 151, 49)");
  	$user.css('background-color', "rgb( 241, 235, 228 )");
}



