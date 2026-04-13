---
title: "Emergency Resources"
layout: page
permalink: /resources/emergency-resources/
redirect_from:
  - /emergency-resources/
image: /assets/images/default-og-image.png
excerpt: "A comprehensive list of emergency resources and contact numbers by country."
---

#### If you or someone you know is in immediate danger or experiencing a crisis, **Emergency Services (Police/Ambulance)** for your country or **nearest Emergency Room** immediately.

Use the table below to find your country's emergency or crisis services.

If your country is not listed, dial your local emergency number or visit [National Suicide Hotline List](https://www.opencounseling.com/suicide-hotlines) for a list of national suicide hotlines.

If you are unsure, use the Global / International section first.

# Emergency Resources by Country

<table>
  <thead>
    <tr>
      <th>Country</th>
      <th>Service</th>
      <th>Contact Number</th>
    </tr>
  </thead>
  <tbody>
    {% assign row_class = "odd" %}
    {% for country in site.data.countries.countries %}
      {% assign service_count = country.services | size %}

      {% for service in country.services %}
        <tr class="{{ row_class }}">

          {% if forloop.first %}
            <td rowspan="{{ service_count }}"><strong>{{ country.name }}</strong></td>
          {% endif %}

          <td>{{ service.service }}</td>

          <td>

            {% case service.type %}

              {% when "url" %}
                <a href="{{ service.url }}" target="_blank" rel="noopener">
                  {{ service.url }}
                </a>

              {% when "phone" %}
                <a href="tel:{{ service.number }}">
                  {{ service.display }}
                </a>

              {% when "sms" %}
                <a href="sms:{{ service.number }}?body={{ service.message }}">
                  {{ service.display }}
                </a>

              {% when "multi" %}
                {% for opt in service.options %}

                  {% if opt.type == "phone" %}
                    <a href="tel:{{ opt.number }}">
                      {{ opt.display }}
                    </a>

                  {% elsif opt.type == "sms" %}
                    <a href="sms:{{ opt.number }}?body={{ opt.message }}">
                      {{ opt.display }}
                    </a>

                  {% endif %}

                  {% unless forloop.last %} / {% endunless %}

                {% endfor %}

            {% endcase %}

          </td>

      </tr>
      {% endfor %}

      {% if row_class == "odd" %}
        {% assign row_class = "even" %}
      {% else %}
        {% assign row_class = "odd" %}
      {% endif %}
    {% endfor %}
  </tbody>
</table>

_Note_: In case of a mental health emergency, please **seek immediate professional help.**

_Note_: If you notice any information missing or inaccurate on this page, please [contact us](/contact/).
