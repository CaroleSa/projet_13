//     DISCUSSION-SPACE PAGE :
//     flip the card
//     if the user click on it

var $dietetic_text = $('#dietetic_text');
$dietetic_text.css('visibility', "hidden");
var $card = $('#card');
$card.css('overflow', 'hidden');
$card.on('click', function() {
$card.css('overflow', 'auto');
$dietetic_text.css('visibility', "");
$card.css('background-image', "url('../../static/dietetic/img/back_face.jpg')");
});


//     ALL PAGES :
//     color the logo clicked
//     by the user

const color = {
  	user: ["#my_account", "52, 151, 49"],
  	poll: ["#my_results", "222, 32, 101"],
  	home: [".step_home", "31, 148, 229"],
  	clipboard: ["#discussion_space", "236, 131, 19"],
  	program: ["#my_program", "190, 120, 50"]
};
for (const elt in color){
    var $element = $(color[elt][0]);
    if ($element.css('visibility') == "visible") {
        var $logo = $("#"+elt+"");
  	    var $color = color[elt][1];
  	    $logo.css('color', "rgb("+$color+")");
  	    $logo.css('background-color', "rgb(233,226,218)");
    }
}


//     ACCOUNT PAGE :
//     displays and removes the password
//     modification form
//     if user clicks on the button key

var $input = $("#form_password");
var $confirm_message = $("#confirm");
$confirm_message.css('visibility', "");
var $error = $(".error").text();
if ($error != "") {
    $input.css('visibility', "");
    }else {
  	$input.css('visibility', "hidden");
}

var $key = $(".fa-key");
var $error_text = $(".error");
$key.on('click', function() {
    if ($input.css('visibility') == "hidden") {
        $input.css('visibility', "");
        $confirm_message.hide();
        $error_text.hide();
    } else{
        $input.css('visibility', "hidden");
    }
});


//     RESULTS PAGE :
//     displays the graphic
//     of the results page

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    $.ajax({
        url: '/dietetic/my_results/',
        data: {
          "get_data": "True"
        },
        success: function (data) {
           var data = google.visualization.arrayToDataTable(data);

           var options = {
             title: 'Perte de poids',
             curveType: 'function',
             legend: 'none',
             pointsVisible: true,
             hAxis: {
                  title: 'Semaines'
               },
             vAxis: {
                  title: 'Poids'
               },
            };

        var chart = new google.visualization.LineChart(document.getElementById('graphic_my_results'));

        chart.draw(data, options);
        }
    });
}


//     RESPONSIVE PAGE :
//     displays and removes menu
//     if user clicks on the menu
//     logo responsive

var $nav_responsive = $("#responsive_menu");
var $menu_logo = $(".fa-bars");
$menu_logo.on('click', function(e) {
    if ($nav_responsive.css('display') == "block") {
        $nav_responsive.css('display', "none");
        } else{
        $nav_responsive.css('display', "block");
        }
});


//     RESPONSIVE PAGE :
//     displays and removes form
//     login and create account
//     if user clicks on the user logo

var $nav = $("#login_nav");
var $logo = $(".fa-user-circle");
var url = window.location.pathname;
if ($logo.css('display') == "block") {
    if (url == "/account/login/" || url == "/account/create_account/" && $logo.css('display') == "block") {
        $nav.css('display', "block");
    }
}

$logo.on('click', function() {
    if ($nav.css('display') == "block") {
        $nav.css('display', "none");} else{
        $nav.css('display', "block");
        }
});
