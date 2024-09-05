function displayEmail() {
    var email = "moc.drzxwunix@drzxwunix".split("").reverse().join(""); // Reversed email
    var link = document.getElementById("contact-link");
    link.href = "mailto:" + email;
    link.innerText = "Send us a note";
}