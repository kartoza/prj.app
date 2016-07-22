/**
 * Created by Dimas Ciputra <dimas@kartoza.com> on 22/07/16.
 */

var sortable_state = 'enabled';

$("#sortable").sortable({
    stop: onStopSortable
});

function onStopSortable(e, ui) {
    var categories = $.map($(this).find('li'), function(el, i){
        var cat = String(el.id).split('-');
        return {
            'sort_number' : i,
            'id': cat[0],
            'name': cat[1]
        }
    });
    sortableDisable();

    var data_url = $("#sortable").data("url");

    if(data_url) {
        $.ajax({
            url: data_url,
            type: "POST",
            data: JSON.stringify(categories),
            success: function (response) {
                sortableEnable();
                if($('#order-saved').is(":visible"))
                {
                    $('#order-saved').hide();
                    showOrderSaved();
                } else {
                    showOrderSaved();
                }
            },
            error: function (response) {
                console.log(response);
                sortableEnable();
                if($('#order-not-saved').is(":visible"))
                {
                    $('#order-not-saved').hide();
                    showOrderNotSaved();
                } else {
                    showOrderNotSaved();
                }
            }

        });
    }

}

function showOrderSaved() {
    $('#order-saved').fadeIn( "fast", function() {
        $('#order-saved').fadeOut(2000);
    });
}

function showOrderNotSaved() {
    $('#order-not-saved').fadeIn( "fast", function() {
        $('#order-not-saved').fadeOut(2000);
    });
}

function sortableEnable() {
    sortable_state = 'enabled';
    $("#sortable").sortable({
        stop: onStopSortable
    });
    $("#sortable").sortable("option", "disabled", false );
    $("#sortable").disableSelection();
    return false;
}
function sortableDisable() {
    sortable_state = 'disabled';
    $( "#sortable" ).sortable("disable");
    return false;
}