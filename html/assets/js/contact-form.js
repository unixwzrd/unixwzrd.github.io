document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("contact-form");
    if (!form) {
        return;
    }

    var status = document.getElementById("contact-form-status");
    var recipient = form.dataset.contactEmail || "";
    var subjectPrefix = form.dataset.subjectPrefix || "Inquiry";

    var submit = form.querySelector(".contact-submit");
    var fields = {
        name: form.querySelector("#contact-name"),
        email: form.querySelector("#contact-email"),
        organization: form.querySelector("#contact-organization"),
        topic: form.querySelector("#contact-topic"),
        message: form.querySelector("#contact-message"),
    };

    if (!recipient || !submit || Object.keys(fields).some(function (key) {
        return !fields[key];
    })) {
        return;
    }

    function setStatus(message) {
        if (!status) {
            return;
        }

        status.innerHTML = message;
    }

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        if (!form.reportValidity()) {
            return;
        }

        var name = fields.name.value.trim();
        var email = fields.email.value.trim();
        var organization = fields.organization.value.trim();
        var topic = fields.topic.value.trim();
        var message = fields.message.value.trim();
        var referrer = document.referrer || "Direct visit";
        var pageUrl = window.location.href;
        var timestamp = new Date().toISOString();

        var subjectParts = [subjectPrefix, topic];
        if (name) {
            subjectParts.push(name);
        }

        var bodyLines = [
            "Name: " + name,
            "Email: " + email,
            "Organization/Role: " + (organization || "Not provided"),
            "Topic: " + topic,
            "",
            "Message:",
            message,
            "",
            "Submitted from: " + pageUrl,
            "Referrer: " + referrer,
            "Timestamp: " + timestamp,
        ];

        var mailtoUrl =
            "mailto:" +
            encodeURIComponent(recipient) +
            "?subject=" +
            encodeURIComponent(subjectParts.join(" | ")) +
            "&body=" +
            encodeURIComponent(bodyLines.join("\n"));

        setStatus(
            "Opening your mail client now. If nothing happens, email " +
                '<a href="' +
                mailtoUrl +
                '">' +
                recipient +
                "</a> directly."
        );

        window.location.href = mailtoUrl;
    });

    submit.disabled = false;
});

