/**
 * Created with PyCharm.
 * User: timlinux
 * Date: 12/08/13
 * Time: 21:45
 * To change this template use File | Settings | File Templates.
 */

$(function () {

    $('.tooltip-toggle').tooltip(
        {container: 'body'}
    );

});

$( "#id_version" ).change(function() {
  update_category_list($(this).val());
});

function update_category_list(version_id)
{
    $.getJSON("/json-category/list/" + version_id + "/", function (data) {
        var items = [];
        $.each(data, function(key, val) {
            items.push('<option value="' + key + '">' + val + '</option>');
        });
        $( "#id_category" ).empty().append(items);
    });
}

