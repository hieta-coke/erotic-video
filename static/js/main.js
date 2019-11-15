(function($) {
    $(window).on("load", function() {
        $(".overlay_btn").on("click", function() {
            var overlay = $(".overlay");
            if($(this).attr("id") == "search_btn") {
                overlay.css("transform", "scale(1)");
            } else {
                overlay.css("transform", "scale(0)");
            }
        });
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $("#good,#bad").on("click", function() {
            var btn = "";
            var pk = $("#pk").text();
            var csrf_token = getCookie("csrftoken");
            var eval_ajax = () => {
                $.ajax({
                    url: location.protocol + "//" + location.hostname + ":8000/movie/" + pk + "/eval",
                    type:'POST',
                    data:{ "eval": btn, },
                    contentType: "application/json",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrf_token);
                        }
                    },
                }).done((data) => {
                    $("#" + btn + "_cnt").text(data["cnt"]);
                }).fail((data) => {
                    console.log(data);
                });
            };
            if($(this).attr("id") == "good") {
                btn ="good";
                eval_ajax();
            } else {
                btn = "bad";
                eval_ajax();
            }
        });
    });
}(jQuery));