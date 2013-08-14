{% load thumbnail %}
{% if version.project.image_file %}
{{ version.project.image_file|thumbnail_url:'medium-entry' }}\n
{% endif %}

Project: {{ version.project }}\n
Changelog for version: {{ version.name }}\n
Description: {{ version.description }}\n
{% if version.image_file %}
![]({{ version.image_file|thumbnail_url:'medium-entry' }})\n
{% endif %}

{% for row in version.categories %}
{{row.category.name }}\n\
---------------------------------------------------------\n
{% for entry in row.entries %}
Feature: **{{ entry.title }}**\n
.........................................................\n
{{ entry.description }}\n
{% if entry.image_file %}
![]({{ entry.image_file|thumbnail_url:'large-entry' }})\n
{% endif %}
{% endfor %}{# entry loop #}
{% endfor %}{# row loop #}
