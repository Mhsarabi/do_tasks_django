{% extends 'mail_templated/base.tpl'%}

{% block subject %}
reset password confirm
{% endblock %}

{% block html %}

for reset your password please click button
<a href="{{ reset_url }}">reset your password</a>

{% endblock %}