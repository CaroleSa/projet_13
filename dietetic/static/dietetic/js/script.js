//     return card if the user click

var $dietetic_text = $('#dietetic_text');
$dietetic_text.hide();

var $card = $('#card');
$card.on('click', function() {
    $dietetic_text.show();
    $card.css('background-image', "url('../../static/dietetic/img/back_face.jpg')");
});


//     logo nav animation

var $button = $('#button_nav');
$button.on('mouseover', function(event) {
  var $id_elt = "#"+event.target.id;
  var $logo = $(''+$id_elt+'');
  $logo.css('color', "rgb(30,20,200)");
});
$button.on('mouseleave', function(event) {
    var $id_elt = "#"+event.target.id;
    var $logo = $(''+$id_elt+'');
    $logo.css('color', "rgb(0,0,0)");
});
