---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

![image-home](/assets/me.jpg)

## About Me 
{% include_relative about.md %}

{% capture position_content %}
  {% include_relative position.md %}
{% endcapture %}

{% assign trimmed_position_content = position_content | strip %}

  {% if trimmed_position_content != "" %}
  <div class="site-alert">
  {{ "## Open Positions" | markdownify }}
    {{ trimmed_position_content | markdownify }}
  </div>
  {% endif %}

## Publications
{% include_relative publication.md %}

<br />

## Talks
{% include_relative talk.md %}

<br />

## Student Supervision
{% include_relative student.md %}

<br />

## Teaching
{% include_relative teaching.md %}
