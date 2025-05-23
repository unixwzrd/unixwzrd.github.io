---
title: "Emergency Resources"
layout: page
permalink: /resources/emergency-resources/
image: /assets/images/default-og-image.png
excerpt: "A comprehensive list of emergency resources and contact numbers by country."
---

#### If you or someone you know is in immediate danger or experiencing a crisis, in the United States, **CALL 911** or go to the nearest emergency room immediately.

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
      <!-- First service row for the country -->
      <tr class="{{ row_class }}">
        <td rowspan="{{ service_count }}"><strong>{{ country.name }}</strong></td>
        <td>{{ country.services[0].service }}</td>
        <td>{{ country.services[0].contact }}</td>
      </tr>

      <!-- Additional services for the country -->
      {% for service in country.services offset:1 %}
        <tr class="{{ row_class }}">
          <td>{{ service.service }}</td>
          <td>{{ service.contact }}</td>
        </tr>
      {% endfor %}

      <!-- Alternate row classes -->
      {% if row_class == "odd" %}
        {% assign row_class = "even" %}
      {% else %}
        {% assign row_class = "odd" %}
      {% endif %}
    {% endfor %}
  </tbody>
</table>

_Note_: In case of a mental health emergency, please seek immediate professional help.

_Note_: If you notice any information missing or inaccurate on this page, please [contact us](/contact).