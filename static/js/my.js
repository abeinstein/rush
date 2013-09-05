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
        console.log("navbar rush clicked")
        var $rush = $(this).attr('id');
        var $profile = $("#" + $rush + "-profile"); // TODO: This is ghetto
        $profile.toggleClass('active');
        $displayed_profile.toggleClass('active');
        $displayed_profile = $profile;
    });
});