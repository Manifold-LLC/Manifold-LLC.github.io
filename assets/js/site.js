/* Manifold LLC - site script. No dependencies. */
(function () {
  "use strict";

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());

  // Contact form
  var form = document.getElementById("contact-form");
  if (!form) return;

  var status = form.querySelector(".status");
  var button = form.querySelector('button[type="submit"]');
  var key = (form.getAttribute("data-access-key") || "").trim();
  var keyConfigured = key && key.indexOf("REPLACE_WITH") !== 0;
  var TO = "info@teammanifold.com";

  function say(msg, cls) {
    if (!status) return;
    status.textContent = msg;
    status.className = "status" + (cls ? " " + cls : "");
  }

  function value(name) {
    var el = form.elements[name];
    return el ? String(el.value || "").trim() : "";
  }

  function validate() {
    var missing = [];
    if (!value("name")) missing.push("your name");
    var email = value("email");
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) missing.push("a valid email address");
    if (!value("message")) missing.push("a message");
    if (missing.length) {
      say("Please add " + missing.join(", ") + ".", "err");
      return false;
    }
    return true;
  }

  function mailtoFallback() {
    var subject = "Inquiry from manifold-llc.com";
    var body =
      "Name: " + value("name") + "\n" +
      "Email: " + value("email") + "\n" +
      (value("organization") ? "Organization: " + value("organization") + "\n" : "") +
      "\n" + value("message") + "\n";
    window.location.href =
      "mailto:" + TO +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
    say("Your mail client should open with the message filled in. If it does not, write to " + TO + ".", "ok");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validate()) return;

    // Honeypot: real visitors never see or tick this box.
    if (form.elements.botcheck && form.elements.botcheck.checked) {
      say("Thanks. Your message was sent.", "ok");
      return;
    }

    if (!keyConfigured || typeof window.fetch !== "function") {
      mailtoFallback();
      return;
    }

    var payload = {
      access_key: key,
      subject: value("subject") || "Inquiry from manifold-llc.com",
      from_name: value("from_name") || "manifold-llc.com contact form",
      name: value("name"),
      email: value("email"),
      organization: value("organization"),
      message: value("message"),
      botcheck: false
    };

    button.disabled = true;
    say("Sending…");

    fetch(form.action, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, json: j }; }); })
      .then(function (res) {
        if (res.ok && res.json && res.json.success !== false) {
          form.reset();
          say("Thanks. Your message was sent. A principal will reply by email.", "ok");
        } else {
          say("The form service did not accept the message. Please email " + TO + " directly.", "err");
        }
      })
      .catch(function () {
        say("Could not reach the form service. Please email " + TO + " directly.", "err");
      })
      .finally(function () { button.disabled = false; });
  });
})();
