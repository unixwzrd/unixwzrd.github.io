document.addEventListener("DOMContentLoaded", function () {
 var form = document.getElementById("contact-form");
 if (!form) {
 return;
 }

 var status = document.getElementById("contact-form-status");
 var recipient = form.dataset.contactEmail || "";
 var subjectPrefix = form.dataset.subjectPrefix || "Inquiry";

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

 var formData = new FormData(form);
 var name = (formData.get("name") || "").toString().trim();
 var email = (formData.get("email") || "").toString().trim();
 var organization = (formData.get("organization") || "").toString().trim();
 var topic = (formData.get("topic") || "").toString().trim();
 var message = (formData.get("message") || "").toString().trim();
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
 "Timestamp: " + timestamp
 ];

 var mailtoUrl = "mailto:" + encodeURIComponent(recipient) +
 "?subject=" + encodeURIComponent(subjectParts.join(" | ")) +
 "&body=" + encodeURIComponent(bodyLines.join("\n"));

 setStatus(
 "Opening your mail client now. If nothing happens, email " +
 "<a href=\"" + mailtoUrl + "\">" + recipient + "</a> directly."
 );

 window.location.href = mailtoUrl;
 });
});
