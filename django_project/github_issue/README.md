# To use:

1) Add something like this to your base template:

    {% if user.is_authenticated %}
    <i class="icon-wrench"></i><a href="#issue-modal" data-toggle="modal">
    Report an issue</a>
    {% endif %}

    <div id="issue-modal" class="modal hide fade">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h3>Submit an issue</h3>
      </div>
      <div class="modal-body">
        <form id="issue-form" class="form-horizontal">
          <div class="control-group">
            <label class="control-label" for="issue-title">Title</label>
            <div class="controls">
              <input type="text" id="issue-title" placeholder="Title">
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="issue-description">Description</label>
            <div class="controls">
              <textarea id="issue-description" rows="3" cols="10"></textarea>
            </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
        <button id="issue-submit-button" class="btn btn-primary" onclick="submitIssue()">Submit an issue</button>
      </div>
    </div>

2) Make sure you ship the github_issues.js in github-issue/static/js as part
    of your collectstatic process.

3) Create another github user account to be used solely for issue submission.
   You should keep this account private as it will have write permissions to
   your repo.

3) Ensure these settings are defined in your apache config (adjust as needed):

      # Define variables used to submit issues to github
      # These env vars will be 'unpackaed into django accessible vars
      # in wsgi.py
      SetEnv GIT_URL "%(github_repo)s"
      SetEnv GIT_USER "%(github_user)s"
      SetEnv GIT_PASSWORD "%(github_password)s"

Note that the GIT_URL should be the api url for your project e.g.

    GIT_URL = "https://api.github.com/repos/<user>/<repo>/issues"


4) Update your wsgi.py so that the env vars defined above are available to
    apache.

    # Customised by Tim so we can access env vars set in apache
    import django.core.handlers.wsgi
    _application = django.core.handlers.wsgi.WSGIHandler()

    def application(environ, start_response):
        """Factory for the application instance.

        Places env vars defined in apache conf into a context accessible by django.
        """
        os.environ['GIT_URL'] = environ['GIT_URL']
        os.environ['GIT_USER'] = environ['GIT_USER']
        os.environ['GIT_PASSWORD'] = environ['GIT_PASSWORD']
        return _application(environ, start_response)

5) Update your settings file to define the needed parameters:

    # Define variables used to submit issues to github
    # These are passed by customisations in wsgi.py
    # with original definitions in apache.conf
    GIT_URL = os.environ.get('GIT_USER')
    GIT_USER = os.environ.get('GIT_USER')
    GIT_PASSWORD = os.environ.get('GIT_PASSWORD')

6) Include github issue app in your urls:

    url(r'^', include('github_issue.urls')),

7) Restart your apache server and test.
