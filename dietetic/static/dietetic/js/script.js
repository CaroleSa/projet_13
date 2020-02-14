//     return card if the user click

var $dietetic_text = $('#dietetic_text');
$dietetic_text.hide();

var $card = $('#card');
$card.on('click', function() {
    $dietetic_text.show();
    $card.css('background-image', "url('../../static/dietetic/img/back_face.jpg')");
});
