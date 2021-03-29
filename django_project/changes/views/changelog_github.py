# coding=utf-8
import os
import re
import requests
import markdown
import warnings

from urllib.parse import urljoin

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse
from braces.views import LoginRequiredMixin
from rest_framework import serializers
from rest_framework.views import APIView, Response
from base.models.project import Project
from changes.models.category import Category
from changes.models.entry import Entry
from changes.models.version import Version
from changes.utils.github_pull_request import parse_funded_by

try:
    from core.settings.secret import GIT_TOKEN
except ImportError:
    GIT_TOKEN = ''
    warnings.warn(
        "Be careful, the GIT_TOKEN is not set. Using the GitHub API will "
        "fail.")


def create_entry_from_github_pr(version, category, data, user):
    """Function to create entry objects from github PR.

    :return:
    """

    existing_entries = Entry.objects.filter(
        github_PR_url__isnull=False).values_list('github_PR_url', flat=True)
    for item in data:
        response = requests.get(
            item['user']['url'],
            headers={'Authorization': 'token {}'.format(GIT_TOKEN)})

        name = ''
        developer_url = ''
        if response.status_code == 200:
            developer_url = response.json()['html_url']
            name = response.json()['name']
            if not name:
                name = response.json()['login']

        content, funded_by, funded_by_url = parse_funded_by(item['body'])

        if item['html_url'] not in existing_entries:
            # Create new entry from data.
            Entry.objects.create(
                category=category,
                title=item['title'],
                description=content,
                developer_url=developer_url,
                developed_by=name,
                funded_by=funded_by,
                funder_url=funded_by_url,
                author=user,
                version=version,
                github_PR_url=item['html_url']
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

        if not GIT_TOKEN:
            return Response({
                'status': 'failed',
                'reason': 'The GitHub token is not set.'
            })

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


class ImgExtractor(Treeprocessor):
    def run(self, doc):
        """Find all images and append to markdown.images."""
        self.markdown.images = []
        for image in doc.findall('.//img'):
            self.markdown.images.append(image.get('src'))


class ImgExtExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        img_ext = ImgExtractor(md)
        md.treeprocessors.add('imgext', img_ext, '>inline')


def download_all_referenced_images(request, **kwargs):
    """Function to download all referenced images from other site."""

    project_slug = kwargs.get('project_slug', None)
    version_slug = kwargs.get('slug', None)

    try:
        version = \
            Version.objects.get(project__slug=project_slug, slug=version_slug)
    except Version.DoesNotExist:
        JsonResponse({
            'status': 'failed',
            'reason': 'Version does not exist'
        })

    try:
        entries = Entry.objects.filter(version=version)
        request.session['total_entries'] = entries.count()
        request.session['progress_entries'] = 0
        num_entry = 0
        for entry in entries:
            content = entry.description
            md = markdown.Markdown(extensions=[ImgExtExtension()])
            html = md.convert(content)
            try:
                images = md.images
                if len(images) > 0:
                    for i, image in enumerate(images):
                        filename = image.rsplit('/', 1)[-1]
                        # Take the first image in the pull request
                        # and set it as default for the entry and remove
                        # it from the body
                        if i == 0:
                            response = requests.get(image)
                            if response.status_code == 200:
                                entry.image_file.save(
                                    filename,
                                    ContentFile(response.content), save=True)
                                rgx = f'<img.*?{image}.*?/>'
                                html = re.sub(rgx, '', html, 1)
                                continue
                        folder_path = os.path.join(
                            settings.MEDIA_ROOT,
                            'images/entries')
                        file_path = os.path.join(
                            folder_path, '{}'.format(filename))
                        found = os.path.exists(file_path)
                        if found:
                            # file_path
                            # e.g /home/web/media/images/entries/img.png
                            file_path_original = file_path
                            n = 0
                            while found:
                                n += 1
                                img_name, ext = file_path_original.rsplit(
                                    '.', 1)
                                # create a unique filename:
                                # add sufix -n in filename prior to extension
                                # e.g /home/web/media/images/entries/img-1.png
                                file_path = f'{img_name}-{n}.{ext}'
                                found = os.path.exists(file_path)
                        with open(file_path, 'wb+') as handle:
                            response = requests.get(image, stream=True)
                            if not response.ok:
                                print('downloading file failed')
                                print(image)
                                pass
                            for block in response.iter_content(1024):
                                if not block:
                                    break
                                handle.write(block)

                            # get image name from relative path
                            # e.g image_name = images/entries/img-1.png
                            image_name = os.path.relpath(
                                file_path,
                                settings.MEDIA_ROOT)
                            # reconstruct img_url
                            # path e.g img_url: /media/images/entries/img-1.png
                            img_url = urljoin(settings.MEDIA_URL, image_name)
                            html = html.replace(image, img_url)
                            html = re.sub(r"alt=\".*?\"", "", html)

                entry.description = html
                entry.save()
                num_entry += 1
                request.session['progress_entries'] = num_entry
            except AttributeError:
                pass
    except Entry.DoesNotExist:
        JsonResponse({
            'status': 'failed',
            'reason': 'Entry does not exist'
        })

    del request.session['total_entries']
    del request.session['progress_entries']
    return JsonResponse({'status': 'success'})
