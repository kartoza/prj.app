/**
 * Created by Dimas Ciputra <dimas@kartoza.com> on 15/07/16.
 */

$(".pop-image").on("click", function() {
    $('#imagepreview').attr('src', $(this).children().attr('id'));
    $('#image-url').attr('href', $(this).children().attr('id'));
    $('#imagemodal').modal('show');
    return false;
});

$(".pop-gif").on("click", function() {
    $('#imagepreview').attr('src', $(this).siblings().attr('id'));
    $('#image-url').attr('href', $(this).siblings().attr('id'));
    $('#imagemodal').modal('show');
    return false;
});

$('.sidebar-offcanvas').stick_in_parent({
    offset_top: 60,
    inner_scrolling: true,
    bottoming: false
});
