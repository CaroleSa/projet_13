//     return card if the user click

var $dietetic_text = $('#dietetic_text');
$dietetic_text.css('visibility', "hidden");
var $card = $('#card');
$card.on('click', function() {
$dietetic_text.css('visibility', "");
$card.css('background-image', "url('../../static/dietetic/img/back_face.jpg')");
});


//     logo nav animation

const color = {
  	user: ["/account/my_account/", "52, 151, 49"],
  	poll: ["/dietetic/my_results/", "222, 32, 101"],
  	home: ["/", "31, 148, 229"],
  	clipboard: ["/dietetic/dietetic_space/", "236, 131, 19"],
  	program: ["/dietetic/program/", "190, 120, 50"]
};
for (const elt in color){
    var $logo_url = color[elt][0];
    var $url = window.location.pathname;
    if ($url == $logo_url) {
        var $logo = $("#"+elt+"");
  	    var $color = color[elt][1];
  	    $logo.css('color', "rgb("+$color+")");
  	    $logo.css('background-color', "rgb(233,226,218)");
    }
}
