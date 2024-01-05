# Logging

With timestamps

1. Authentication request sent
2. Authentication with AI Engine successful. In case of failure, the error message.
3. Sent PDF <filename> for digitalisation.
4. Digitalisation success/failure. If failure, error_msg.
5. Success of JSON creation.
6. Start of JSON file downloand, with file-name, or session_id.
7. Write to Odoo model/fields.

For version 0.9, we log above events to /var/log/odoo/odoo-server.log on the Docker.
