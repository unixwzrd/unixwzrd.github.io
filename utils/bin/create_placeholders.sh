
#!/bin/bash

# Create placeholder .md files with appropriate content

echo "Creating placeholder files..."

cat <<EOL > resources.md
---
layout: page
title: Resources
menu_item: Resources
---
This is a placeholder page for the Resources section. Content coming soon.
EOL

cat <<EOL > contact.md
---
layout: page
title: Contact
menu_item: Contact
---
This is a placeholder page for the Contact section. Content coming soon.
EOL

cat <<EOL > faq.md
---
layout: page
title: FAQ
menu_item: FAQ
---
This is a placeholder page for the FAQ section. Content coming soon.
EOL

echo "Placeholder pages created!"
