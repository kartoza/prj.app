/**
 * Created by Dimas Ciputra <dimas@kartoza.com> on 30/07/16.
 */

var need_refresh = false;
var github_repo = {};
var repo_org = '';

// Column //

var loading_view = $('#loading-view');
var loading_bar_view = $('#loading-bar');
var loading_org_view = $('#loading-orgs-view');
var github_list_container = $('#github-list-container');
var org_list_container = $('#org-list-container');

// Modal Div //

var github_modal_container = $('#modal-github-container');
var confirmation_modal = $('#confirmation-modal');

// Button //

var modal_submit_button = $('#modal-submit');
var get_repo_button = $('#get-repo');
var modal_close_button = $('#modal-close');

// Messages //

var project_added_m = $('#project-saved');
var project_not_added_m = $('#project-not-saved');

// Init

var org_url = '';
var repo_url = '';
var repo_from_org_url = '';
var repo_submit_url = '';

var GithubRepo = {
    init: function (urls) {
        org_url = urls.org_url;
        repo_url = urls.repo_url;
        repo_from_org_url = urls.repo_from_org_url;
        repo_submit_url = urls.repo_submit_url;

        get_orgs();
    }
};

// Button Events //

github_list_container.on('click', '.add-project', function(){
    var g_id = $(this).data('id');
    github_modal_container.empty();
    github_modal_container.append(create_project_html(github_repo[g_id], true));
    confirmation_modal.modal({backdrop: 'static', keyboard: false});
    return false;
});

modal_submit_button.click(function(){
    modal_submit_button.prop('disabled', true);
    modal_close_button.prop('disabled', true);
    loading_bar_view.show();
    var g_id = $(this)
        .parent()
        .siblings('.modal-body')
        .children('#modal-github-container')
        .children('.github-list')
        .data('id');
    $.ajax({
        url: repo_submit_url,
        type: 'POST',
        data: JSON.stringify({
            'full_name': g_id
        }),
        success: function (response) {
            console.log(response);
            project_added_m.show();
            need_refresh = true;
        },
        error: function (response) {
            console.log(response);
            project_not_added_m.show();
        },
        complete: function () {
            loading_bar_view.hide();
            modal_close_button.prop('disabled', false);
        }
    });
    return false;
});

org_list_container.on('click', '.org-list', function(){
    // check if disabled
    if(!$(this).hasClass('disabled')) {
        // check if active
        if($(this).hasClass('active')) {
            // nothing
        } else {
            // remove all active
            $(this).parent().children().removeClass('active');
            $(this).addClass('active');
            repo_org = $(this).data('name');
            get_repositories();
        }
    }
});

get_repo_button.click(function() {
    get_repositories();
});

// Modal events //

confirmation_modal.on('hidden.bs.modal', function () {
    project_added_m.hide();
    project_not_added_m.hide();

    // if there is a project just added, refresh list
    if(need_refresh) {
        get_repositories();
    }
});

// HTML element creation //

function create_organizations_html(github_data) {
    return  '<p class="list-group-item org-list" data-name="'+
                ((github_data['is_user'] != true) ? github_data['login'] : '')+
            '">'+
                '<img class="profile-pic" src='+github_data['avatar_url']+'  />'+
                    github_data['login']+
            '</p>';
}

function create_project_html(github_data, is_modal) {
    var element = '<div class="row github-list list-group-item" data-id='+ github_data['full_name'] +'>'+
        '<div class="col-lg-9" >'+
        '<h4 class="list-repo-title">'+
        '<a href="'+ github_data['html_url'] +'" target="_blank">'+
        github_data['full_name']+
        '</a>'+
        '</h4>'+
        '<p class="list-repo-sub">'+
        github_data['description']+
        '</p>'+
        '</div>';

    if(!is_modal) {
        if(github_data['added']) {
            element +=  '<div class="col-lg-3">'+
                '<div class="btn-group pull-right list-repo-button">'+
                '<div disabled class="btn btn-success btn-mini"'+
                'data-id='+ github_data['full_name'] +'>'+
                '<span class="glyphicon glyphicon-ok"></span>'+
                '</div>'+
                '</div>'+
                '</div>';
        } else {
            element +=  '<div class="col-lg-3">'+
                '<div class="btn-group pull-right list-repo-button">'+
                '<div class="btn btn-default btn-mini add-project"'+
                'data-id='+ github_data['full_name'] +'>'+
                '<span class="glyphicon glyphicon-plus"></span>'+
                '</div>'+
                '</div>'+
                '</div>';
        }
    }
    element += '</div>';
    return element;
}

// GET Functions

function get_orgs() {
    loading_org_view.show();

    $.ajax({
        url: org_url,
        type: "GET",
        success: function(response) {
            for(var i=0; i < response.length;i++) {
                org_list_container.append(create_organizations_html(response[i]));
            }
        },
        error: function (response) {
            console.log(response);
        },
        complete: function() {
            loading_org_view.hide();
        }
    })
}

function get_repositories() {
    get_repo_button.prop('disabled', true);
    github_list_container.empty();
    loading_view.show();
    disable_orgs_list();

    var url = '';

    if(repo_org) {
        url = repo_from_org_url.replace('org_name', repo_org);
    } else {
        url = repo_url;
    }

    $.ajax({
        url: url,
        type: "GET",
        success: function (response) {
            github_repo = {};
            for(var i=0; i < response.length; i++) {
                github_repo[response[i]['full_name']] = response[i];
                github_list_container.append(create_project_html(response[i], false));
            }
        },
        error: function (response) {
            console.log(response);
        },
        complete: function() {
            enable_orgs_list();
            loading_view.hide();
            get_repo_button.prop('disabled', false);
        }
    });
}

$(org_list_container).stick_in_parent({
    offset_top: 60,
    inner_scrolling: true,
    parent: $('#container')
});

function disable_orgs_list() {
    org_list_container.children().addClass('disabled');
}

function enable_orgs_list() {
    org_list_container.children().removeClass('disabled');
}