/**
 * Created by Dimas Ciputra <dimas@kartoza.com> on 01/08/16.
 */
var GithubRepo = (function(){

    // Elements
    var github_list_container = $('#github-list-container');
    var org_list_container = $('#org-list-container');
    var github_modal_container = $('#modal-github-container');

    // Vars
    var org_repo_active = '';
    var github_repo_json = {};

    // Urls
    var urls = {};

    var bindFunctions = function () {
        github_list_container.on('click', '.add-project', addRepoClick);
        org_list_container.on('click', '.org-list', orgClick);
        $('#modal-submit').click(submitRepoClick);
        $('#confirmation-modal').on('hidden.bs.modal', modalOnClose);
    };

    // Event functions
    var orgClick = function(event) {
        if(!$(this).hasClass('disabled')) {
            if(!$(this).hasClass('active')) {
                $(this).parent().children().removeClass('active');
                $(this).addClass('active');

                org_repo_active = $(this).data('name');

                github_list_container.children().hide();
                $('#repo-'+org_repo_active).show();
            }
        }
    };
    
    var modalOnClose = function (event) {
        $('#project-not-saved').hide();
        $('#project-saved').hide();
        $('#modal-submit').prop('disabled', false);
    };

    var addRepoClick = function (event) {
        var data_id = $(this).data('id');
        github_modal_container.empty();
        github_modal_container.append(
            create_repo_div(github_repo_json['repo-'+org_repo_active][data_id], true)
        );
        $('#confirmation-modal').modal(
            {backdrop: 'static', keyboard: false}
        );
        return false;
    };

    var submitRepoClick = function (event) {
        $('#modal-submit').prop('disabled', true);
        $('#modal-close').prop('disabled', true);
        $('#loading-bar').show();
        var data_id = $(this)
            .parent()
            .siblings('.modal-body')
            .children('#modal-github-container')
            .children('.github-list')
            .data('id');
        $.ajax({
            url: urls.repo_submit_url,
            type: 'POST',
            data: JSON.stringify({
                'full_name': data_id
            }),
            success: function (response) {
                if(response=="") {
                    $('#project-saved').show();
                    set_repo_div_added(data_id);
                } else {
                    $('#project-not-saved').show();
                }
            },
            error: function () {
                $('#project-not-saved').show();
            },
            complete: function () {
                $('#loading-bar').hide();
                $('#modal-close').prop('disabled', false);
            }
        });
        return false;
    };

    // Get
    function get_orgs() {
        org_list_container.append(
            create_loading_div('loading-view', 'Getting List..')
        );

        $.ajax({
            url: urls.org_url,
            type: "GET",
            success: function(response) {
                org_list_container.empty();
                for(var i=0; i < response.length;i++) {
                    // create div
                    var $container_div;
                    if(response[i]['is_user']) {
                        org_list_container.append(create_organizations_div(response[i], true));
                        $container_div = $('<div class="list-group" id="repo-'+response[i]['login']+'"></div>');
                        org_repo_active = response[i]['login'];
                    } else {
                        org_list_container.append(create_organizations_div(response[i], false));
                        $container_div = $('<div class="list-group" id="repo-'+response[i]['login']+'" hidden></div>');
                    }
                    $container_div.append(create_loading_div('loading-view', 'Getting Repositories..'));
                    github_list_container.append($container_div);
                    get_repositories($container_div, response[i]['login'], response[i]['is_user']);
                }
            },
            error: function (response) {
                console.log(response);
            },
            complete: function() {
            }
        })
    }

    function get_repositories(repo_container, repo_org_name, is_user) {
        var the_url = '';
        if(is_user) {
            the_url = urls.repo_url;
        } else {
            the_url = urls.repo_from_org_url.replace('org_name', repo_org_name);
        }
        $.ajax({
            url: the_url,
            type: "GET",
            success: function (response) {
                github_repo_json['repo-'+repo_org_name] = {};
                for(var i=0; i < response.length; i++) {
                    github_repo_json['repo-'+repo_org_name][response[i]['full_name']] = response[i];
                    repo_container.append(create_repo_div(response[i], false));
                    repo_container.children('.loading-view').hide();
                }
            },
            error: function (response) {
                console.log(response);
            },
            complete: function() {
               //  enable_all_elm();
            }
        });
    }

    // HTML element creation //
    function create_organizations_div(github_data, is_active) {
        return  '<p class="list-group-item org-list '+ ((is_active==true) ? 'active': '') +'" data-name="'+
                    github_data['login']+
                '">'+
                '<img class="profile-pic" src='+github_data['avatar_url']+'  />'+
                    github_data['login']+
                '</p>';
    }

    function create_loading_div(classname, message) {
        return '<div class="'+classname+'">'+
                    '<img src="/static/gif/loading.gif" width="50px"/>'+
                    '<p style="margin-top: 10px;">'+ message +'</p>'+
                '</div>';
    }

    function create_repo_div(github_data, is_modal) {
        var element =   '<div class="row github-list list-group-item" data-id='+ github_data['full_name'] +'>'+
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

    function set_repo_div_added(repo_name) {
        $('#repo-'+org_repo_active).children().each(function(){
            if($(this).data('id')==repo_name) {
                $(this)
                    .children('.col-lg-3')
                    .children('.list-repo-button')
                    .children('.btn')
                        .removeClass('add-project')
                        .removeClass('btn-default')
                        .addClass('btn-success')
                        .addClass('disabled')
                    .children('.glyphicon')
                        .removeClass('glyphicon-plus')
                        .addClass('glyphicon-ok');
            }
        });
    }

    // Initialization
    var init = function (_urls) {
        bindFunctions();

        // _urls.org_url
        // _urls.repo_url
        // _urls.repo_from_org_url
        // _urls.repo_submit_url
        urls = _urls;
        get_orgs();

        org_list_container.stick_in_parent({
            offset_top: 60,
            inner_scrolling: true,
            parent: $('#container')
        });
    };

    return {
        init: init
    };

})();