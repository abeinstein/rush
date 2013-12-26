$(document).ready(function(){
    console.log("ready");

    // Display first rush profile on list
    var $displayed_profile = $('.active');

    $('.rush-row').click(function(){
        // First, find out which row it 
        var $rush = $(this).find("td div").attr('id');
        var $profile = $("#" + $rush + "-profile"); // TODO: This is ghetto
        $profile.toggleClass('active');
        $displayed_profile.toggleClass('active');
        $displayed_profile = $profile;

    });

    $('.navbar-rush').click(function(){
        // First, find out which row it 
        console.log("navbar rush clicked");
        var $rush = $(this).attr('id');
        var $profile = $("#" + $rush + "-profile"); // TODO: This is ghetto
        $profile.toggleClass('active');
        $displayed_profile.toggleClass('active');
        $displayed_profile = $profile;
    });

    $(".comment-form-inner").submit(function(event) {
        event.preventDefault();
        $target = $(event.target);
        console.log(event);

        var rush_id = $target.attr("data-rush-id");
        var prof_id = $target.attr("data-prof-id");
        var comment = $target.find("textarea").val();
        var profile_name = $target.attr("data-prof-name");

        var url = "/api/v1/comment/add/";
        var data = {
            "rush_id": parseInt(rush_id, 10),
            "prof_id": parseInt(prof_id, 10),
            "body": comment
        };

        console.log(url);
        console.log(data);

        post = $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
            //dataType: 'json',
            contentType: 'application/json'
        });

        console.log(post);

        post.done(function(data) {

            // Create a new comment div, put in the DOM
            var comments = $target.closest(".rush-profile").find(".comments");
            var comment_div = $('<div class="right-comment" />').appendTo(comments);
            $('<div class="left-comment-text" />').html(comment).appendTo(comment_div);
            $('<div class="comment-name" />').html(profile_name).appendTo(comment_div);

            // Clear the text field
            $target.find("textarea").val("");




        });
    });


});