{% extends "mail_templated/base.tpl" %}
{{subject}}
{% block subject %}
Hello {{ name }}
{% endblock %}

{% block body %}
{{message}}
{% endblock %}

{% block html %}
This is an <strong>html</strong> part.
<a href ="{{message}}">{{message}}</a>
{% endblock %}