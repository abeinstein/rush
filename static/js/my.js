$(document).ready(function(){
    console.log("ready");

    // Display first rush profile on list
    var $displayed_profile = $('.rush-profile .active');

    $('.rush-row').click(function(){
        // First, find out which row it 
        var $rush = $(this).attr('id');
        var profileid = $rush + "-profile";
        $(profileid).toggleClass('active');
        $displayed_profile.toggleClass('active');
        $displayed_profile = $(profileid);

    })
});