(function ($) {
    $(document).ready(function () {
        setTimeout(function () {
            var rolesJson = JSON.parse($('.all_roles_permissions').find(".grp-readonly").text());
            $("#id_groups_add_link").click(function () {
                renderRolePermissions()
            });
            $("#id_groups_remove_link").click(function () {
                renderRolePermissions()
            });
            function renderRolePermissions() {
                var permissions = [];
                $("#id_groups_to option").each(function (index, element) {
                    permissions = $.merge(permissions, rolesJson[$(element).text()]);
                });
                if (permissions.length > 0) {
                    $(".role_permissions .grp-readonly").html(permissions.join('<br>'));
                } else {
                    $(".role_permissions .grp-readonly").html('-');
                }
            }
        }, 500);

    });
})(django.jQuery);