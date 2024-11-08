{% capture left %}
{% include_relative left.md %}
{% endcapture %}
{{ left | markdownify }}
