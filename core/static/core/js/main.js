$(function(){
    $("#lobby-navbar-leave").click(function(e){
        e.preventDefault();
        activateModal("Are you sure you want to leave the lobby?", function(){
            window.location.href = $(e.target).attr("href");
        });
    });
});

function activateModal(content, confirm){
    var modal = $('.modal');
    modal.find('.modal-close').click(function(){
        modal.removeClass('is-active');
    });
    var modal_content = modal.find('.modal-content');
    modal_content.find('.content').html(content);
    modal_content.find('.modal-confirm').click(confirm);
    modal.addClass('is-active');
}