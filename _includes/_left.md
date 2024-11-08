{% capture left_content %}
{% include_relative left_content.md %}
{% endcapture %}
{{ left_content | markdownify }}
