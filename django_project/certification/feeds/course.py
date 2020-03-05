# coding=utf-8
from datetime import datetime
from django.contrib.gis.feeds import Feed
from django.http import Http404
from django.shortcuts import get_object_or_404
from .json_feed import CourseJSONFeed
from base.models.project import Project
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.models.course import Course


class UpcomingCourseFeed(Feed):
    """Feed for upcoming courses."""

    feed_type = CourseJSONFeed

    def get_object(self, request, *args, **kwargs):
        """Return the certifying organisation object that
        matches the project_slug and organisation slug.

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: certifying organisation
        :rtype: CertifyingOrganisation

        :raises: Http404
        """
        try:
            project_slug = kwargs.get('project_slug', None)
            project = get_object_or_404(Project, slug=project_slug)
            organisation_slug = kwargs.get('organisation_slug', None)
            certifying_organisation = (
                get_object_or_404(
                    CertifyingOrganisation,
                    slug=organisation_slug,
                    project=project
                ))
            certifying_organisation.uri = (
                self.get_absolute_obj_url(request, certifying_organisation))
            certifying_organisation.request = request
            return certifying_organisation
        except Http404:
            raise Http404(
                'Sorry! We could not find your '
                'project/certifying organisation!')

    def get_absolute_obj_url(self, request, obj):
        return request.build_absolute_uri(obj.get_absolute_url())

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'JSON Feed for upcoming course of {}'.format(obj.name)

    def link(self, obj):
        """Return the url of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: Url of the certifying organisation.
        :rtype: str
        """
        return obj.uri

    def feed_extra_kwargs(self, obj):
        """Return the homepage of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: Homepage of the certifying organisation.
        :rtype: str
        """
        return {
            'homepage': obj.url,
        }

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the upcoming courses ' \
               'of {}.'.format(obj.name)

    def items(self, obj):
        """Return upcoming course of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: List of course of a certifying organisation
        :rtype: list
        """
        today = datetime.today()
        courses = Course.objects.filter(
            certifying_organisation=obj, start_date__gte=today
        ).order_by('-start_date')
        for course in courses:
            course.link = self.get_absolute_obj_url(obj.request, course)
        return courses

    def item_title(self, item):
        """Return the title of the training center.

        :param item: Course object of a certifying organisation
        :type item: Course

        :returns: name of the course
        :rtype: str
        """
        return item.name

    def item_link(self, item):
        """Return the title of the training center.

        :param item: Course object of a certifying organisation
        :type item: Course

        :returns: url of the course
        :rtype: str
        """
        return item.link

    def item_extra_kwargs(self, item):
        if item.course_convener.degree:
            degree = ', {}'.format(item.course_convener.degree)
        else:
            degree = ''
        return {
            'start_date': item.start_date,
            'end_date': item.end_date,
            'trained_competence': item.trained_competence,
            'language': item.language,
            'course_type': item.course_type.name,
            'course_convener': '{} {}{}'.format(
                item.course_convener.user.first_name,
                item.course_convener.user.last_name,
                degree
            ),
            'training_center': item.training_center,
            'certifying_organisation': item.certifying_organisation
        }


class PastCourseFeed(UpcomingCourseFeed):
    """Feed for past courses."""

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'JSON Feed for past course of {}'.format(obj.name)

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the past courses ' \
               'of {}.'.format(obj.name)

    def items(self, obj):
        """Return upcoming course of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: List of course of a certifying organisation
        :rtype: list
        """
        today = datetime.today()
        courses = Course.objects.filter(
            certifying_organisation=obj, end_date__lte=today
        ).order_by('-start_date')
        for course in courses:
            course.link = self.get_absolute_obj_url(obj.request, course)
        return courses


class UpcomingCourseProjectFeed(UpcomingCourseFeed):
    """Feed for upcoming course within the project."""

    def get_object(self, request, *args, **kwargs):
        """Return the certifying organisation object that
        matches the project_slug and organisation slug.

        :param request: The incoming HTTP request object
        :type request: Request object

        :param args: Positional arguments
        :type args: tuple

        :param kwargs: Keyword arguments
        :type kwargs: dict

        :returns: project
        :rtype: Project

        :raises: Http404
        """
        try:
            project_slug = kwargs.get('project_slug', None)
            project = get_object_or_404(Project, slug=project_slug)
            project.uri = (
                self.get_absolute_obj_url(request, project))
            project.request = request
            return project
        except Http404:
            raise Http404(
                'Sorry! We could not find your project!')

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A project
         :type obj: Project

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'JSON Feed for upcoming course of {} project'.format(obj.name)

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the upcoming courses ' \
               'of {} project.'.format(obj.name)

    def items(self, obj):
        """Return upcoming course of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: List of course of a certifying organisation
        :rtype: list
        """
        today = datetime.today()
        courses = Course.objects.filter(
            certifying_organisation__project=obj, start_date__gte=today
        ).order_by('-start_date')
        for course in courses:
            course.link = self.get_absolute_obj_url(obj.request, course)
        return courses

    def feed_extra_kwargs(self, obj):
        """Return the homepage of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: Homepage of the certifying organisation.
        :rtype: str
        """
        return {
            'homepage': obj.project_url,
        }


class PastCourseProjectFeed(UpcomingCourseProjectFeed):
    """Feed for past courses."""

    def title(self, obj):
        """Return a title for the RSS.

         :param obj: A project
         :type obj: Project

         :returns: Title of the RSS Feed.
         :rtype: str
         """
        return 'JSON Feed for past course of {} project'.format(obj.name)

    def description(self, obj):
        """Return a description for the RSS.

         :param obj: A certifying organisation
         :type obj: CertifyingOrganisation

         :returns: Description of the RSS Feed.
         :rtype: str
         """
        return 'These are the past courses ' \
               'of {} project.'.format(obj.name)

    def items(self, obj):
        """Return upcoming course of the certifying organisation.

        :param obj: A certifying organisation
        :type obj: CertifyingOrganisation

        :returns: List of course of a certifying organisation
        :rtype: list
        """
        today = datetime.today()
        courses = Course.objects.filter(
            certifying_organisation__project=obj, end_date__lte=today
        ).order_by('-start_date')
        for course in courses:
            course.link = self.get_absolute_obj_url(obj.request, course)
        return courses
