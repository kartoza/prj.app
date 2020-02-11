# coding=utf-8
import requests
from braces.views import LoginRequiredMixin
from rest_framework import serializers
from rest_framework.views import APIView, Response
from core.settings.secret import GIT_TOKEN
from base.models.project import Project
from changes.models.category import Category
from changes.models.entry import Entry
from changes.models.version import Version


def create_entry_from_github_pr(version, category, data, user):
    """Function to create entry objects from github PR.

    :return:
    """

    for item in data:
        response = requests.get(
            item['user']['url'],
            headers={'Authorization': 'token {}'.format(GIT_TOKEN)})

        name = ''
        if response.status_code == 200:
            name = response.json()['name']
            if not name:
                name = response.json()['login']

        entry = Entry.objects.create(  #noqa
            category=category,
            title=item['title'],
            description=item['body'],
            developer_url=item['user']['url'],
            developed_by=name,
            author=user,
            version=version
        )
    return True


class FetchGithubPRs(APIView):
    """
    API to fetch PRs from Github repository.
    """

    def post(self, request, project_pk):
        user = request.user
        repo = request.POST.get('repo', None)
        category_pk = request.POST.get('category', None)
        version_slug = request.POST.get('version_slug', None)

        if not repo or not category_pk or not version_slug:
            return Response({
                'status': 'failed',
                'reason': 'Repository or category or version'
                          ' parameter is not found.'
            })

        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            return Response({
                'status': 'failed',
                'reason': 'This project is not found.'
            })

        try:
            category = Category.objects.get(pk=category_pk, project=project)
        except Category.DoesNotExist:
            return Response({
                'status': 'failed',
                'reason': 'This category is not found.'
            })

        try:
            version = Version.objects.get(slug=version_slug, project=project)
        except Version.DoesNotExist:
            return Response({
                'status': 'failed',
                'reason': 'This version is not found.'
            })

        results = []

        repo = repo.replace('https://github.com/', '')
        query = request.POST.get('query', None)

        url = 'https://api.github.com/search/issues?' \
              'q=is:pr+repo:{}+{}&per_page=100'.format(repo, query)

        response = requests.get(
            url,
            headers={'Authorization': 'token {}'.format(GIT_TOKEN)})

        try:
            results.extend(response.json()['items'])
        except:
            return Response([])

        header_link = response.links
        if header_link:
            while 'next' in response.links.keys():
                next_url = response.links['next']['url']
                response = requests.get(
                    next_url,
                    headers={
                        'Authorization': 'token {}'.format(GIT_TOKEN)})
                try:
                    results.extend(response.json()['items'])
                except:
                    pass

        create_entry_from_github_pr(version, category, results, user)
        return Response({
            'status': 'success',
            'reason': ''
        })


class FetchRepoLabels(LoginRequiredMixin, APIView):
    """
    API to fetch list of labels on the repo.
    """

    def get(self, request, project_pk):
        repo = request.GET.get('repo')

        if not repo:
            return Response([])

        results = []
        repo = repo.replace('https://github.com/', '')
        url = 'https://api.github.com/repos/{}/labels?per_page=100'.format(
            repo)
        response = requests.get(
            url, headers={'Authorization': 'token {}'.format(GIT_TOKEN)})
        if response.status_code == 200:
            results.extend(response.json())

        header_link = response.links
        if header_link:
            while 'next' in response.links.keys():
                next_url = response.links['next']['url']
                response = requests.get(
                    next_url,
                    headers={
                        'Authorization': 'token {}'.format(GIT_TOKEN)})
                try:
                    results.extend(response.json())
                except:
                    pass
        return Response(results)


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        model = Category
        fields = ['id', 'name']


class FetchCategory(LoginRequiredMixin, APIView):
    """
    API to fetch Category.
    """

    def get(self, request, project_pk):
        try:
            project = Project.objects.get(pk=project_pk)
            categories = Category.objects.filter(project=project)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except:
            return Response([])
