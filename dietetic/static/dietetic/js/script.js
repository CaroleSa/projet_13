//     return card if the user click

var $dietetic_text = $('#dietetic_text');
$dietetic_text.css('visibility', "hidden");
var $card = $('#card');
$card.css('overflow', 'hidden');
$card.on('click', function() {
$card.css('overflow', 'auto');
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


//     display account option if user clicks on the button key

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
$key.on('click', function() {
    $input.css('visibility', "");
    $confirm_message.hide();
});


//     graphic

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


//     display menu if user clicks on the menu logo responsive
var $nav_responsive = $("#responsive_menu");
var $menu_logo = $(".fa-bars");
$menu_logo.on('click', function(e) {
    if ($nav_responsive.css('display') == "block") {
        $nav_responsive.css('display', "none");
        } else{
        $nav_responsive.css('display', "block");
        }
});


//     display account login and create account if user clicks on the user logo
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
