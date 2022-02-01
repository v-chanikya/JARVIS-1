$(function() {
    let session_id = getCookie("session_id");
    if (session_id != undefined){
        $(".nav_bar_user_not_logged_in").css({"display":"none"});
        $(".nav_bar_user_logged_in").css({"display":"block"});
        $("#user_name_nav_bar").text(getCookie("user"));
    };

    let api_prefix = "/api"

    $("#logout_nav_bar").click(function(){
        let session_id = getCookie("session_id");
        $.post(domain + api_prefix + "/logout",
            {"session_id" : session_id}).done(function (data){
                sessionCleanup();
            });
    })
});
