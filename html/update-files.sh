#!/bin/bash

# Create or append to .md files with appropriate content

echo "Appending placeholder content to files..."

# Emergency Resources page
if [ -f "emergency-resources.md" ]; then
    echo "Appending to emergency-resources.md"
else
    echo "Creating emergency-resources.md"
fi
cat <<EOL >> emergency-resources.md

---
title: "Emergency Resources"
layout: page
---

## Emergency Crisis Resources

If you or someone you know is in immediate danger or experiencing a crisis, **call 911** or go to the nearest emergency room.

### Global Crisis Hotlines
- **National Suicide Prevention Lifeline (USA)**: 1-800-273-8255
- **Crisis Text Line (USA)**: Text HOME to 741741
- **Samaritans (UK)**: 116 123
- **Lifeline (Australia)**: 13 11 14
- **Emergency Services (Canada)**: 911
- **Global Crisis Helplines Directory**: [Link to comprehensive resource]

_Note_: In case of a mental health emergency, please seek immediate professional help.
EOL

# Resources page
if [ -f "resources.md" ]; then
    echo "Appending to resources.md"
else
    echo "Creating resources.md"
fi
cat <<EOL >> resources.md

---
title: "Resources"
layout: page
---

## General Resources

### Mental Health Resources
- [Find a Therapist](https://www.psychologytoday.com/us/therapists)
- [BetterHelp](https://www.betterhelp.com)
- [Therapy Aid for Financial Assistance](https://therapyaid.com)

### Legal Resources
- [American Bar Association Lawyer Referral](https://www.americanbar.org)
- [National Legal Aid & Defender Association](https://www.nlada.org)
- [Legal Aid Society](https://www.legalaid.org)

For more information on crisis intervention, visit the [Emergency Resources](./emergency-resources) page.
EOL

# Contact page
if [ -f "contact.md" ]; then
    echo "Appending to contact.md"
else
    echo "Creating contact.md"
fi
cat <<EOL >> contact.md

---
title: "Contact Us"
layout: page
---

## Contact Us

For inquiries or to discuss a project, please use the following contact details:

- **Email**: [unixwzrd@unixwzrd.ai](mailto:unixwzrd@unixwzrd.ai)
- **Phone**: To be updated
- **Mailing Address**: To be updated

For matters outside our scope of work, please visit our [Resources](./resources) page for additional help.
EOL

# FAQ page
if [ -f "faq.md" ]; then
    echo "Appending to faq.md"
else
    echo "Creating faq.md"
fi
cat <<EOL >> faq.md

---
title: "Frequently Asked Questions"
layout: page
---

## Frequently Asked Questions

### What services do you provide?
We specialize in AI analysis, parental alienation case support, and high-conflict divorce insights, among other distributed computing services.

### How do I get a quote for your services?
Reach out via our [Contact page](./contact) to discuss your project and get a custom quote.

### How is confidentiality maintained?
We take privacy seriously and handle all data with strict confidentiality protocols. For more details, contact us directly.
EOL

# About page
if [ -f "about.md" ]; then
    echo "Appending to about.md"
else
    echo "Creating about.md"
fi
cat <<EOL >> about.md

---
title: "About Us"
layout: page
---

## About Distributed Thinking Systems

Distributed Thinking Systems is focused on AI-driven solutions for high-conflict divorce cases, parental alienation analysis, and other distributed computing services. We aim to offer valuable resources to families and professionals through cutting-edge technology and insights.

### Support Our Mission
This project is currently self-funded. If you'd like to help us keep the site running and support our outreach efforts, consider donating via [Ko-fi](https://ko-fi.com) or [Patreon](https://www.patreon.com).

Your support helps keep vital resources free and accessible to those in need.
EOL

echo "Placeholder content appended to files!"