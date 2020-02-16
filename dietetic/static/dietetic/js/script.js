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
const color = {
  	user: "30,0,200",
  	poll: "30,100,200",
  	home: "40,70,200",
  	clipboard: "30,20,80",
};
$button.on('click', function(event) {



  var $id_name = event.target.id;

  var $id_elt = "#"+$id_name;

  var $logo = $(''+$id_elt+'');

  var $color = $id_name.css(color);
  alert($color)
});
