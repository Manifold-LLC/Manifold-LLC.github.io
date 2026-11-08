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
  var endpoint = (form.getAttribute("data-endpoint") || "").trim();
  var keyConfigured = !!key && key.indexOf("REPLACE_WITH") !== 0 && !!endpoint;
  var TO = "info@teammanifold.com";

  function say(msg, cls) {
    if (!status) return;
    status.textContent = msg;
    status.className = "status" + (cls ? " " + cls : "");
  }

  function field(name) {
    return form.elements[name] || null;
  }

  function value(name) {
    var el = field(name);
    return el ? String(el.value || "").trim() : "";
  }

  function setError(name, msg) {
    var el = field(name);
    if (!el) return;
    var err = document.getElementById(el.id + "-err");
    if (msg) {
      el.setAttribute("aria-invalid", "true");
      if (err) err.textContent = msg;
    } else {
      el.removeAttribute("aria-invalid");
      if (err) err.textContent = "";
    }
  }

  function validate() {
    var first = null;
    var problems = {
      name: value("name") ? "" : "Please add your name.",
      email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value("email")) ? "" : "Please add a valid email address.",
      message: value("message") ? "" : "Please add a message."
    };
    Object.keys(problems).forEach(function (n) {
      setError(n, problems[n]);
      if (problems[n] && !first) first = field(n);
    });
    if (first) {
      say("Please fix the highlighted fields.", "err");
      first.focus();
      return false;
    }
    say("");
    return true;
  }

  ["name", "email", "message"].forEach(function (n) {
    var el = field(n);
    if (el) el.addEventListener("input", function () { setError(n, ""); });
  });

  function mailtoFallback() {
    var subject = "Inquiry from manifold-llc.com";
    var body =
      "Name: " + value("name") + "\r\n" +
      "Email: " + value("email") + "\r\n" +
      (value("organization") ? "Organization: " + value("organization") + "\r\n" : "") +
      "\r\n" + value("message") + "\r\n";
    window.location.href =
      "mailto:" + TO +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
    say("Your mail client should open with the message filled in. If it does not, write to " + TO + ".", "ok");
  }

  function done() {
    button.disabled = false;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (button.disabled) return;
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

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, json: j }; });
      })
      .then(function (res) {
        done();
        if (res.ok && res.json && res.json.success !== false) {
          form.reset();
          say("Thanks. Your message was sent. A principal will reply by email.", "ok");
        } else {
          say("The form service did not accept the message. Please email " + TO + " directly.", "err");
        }
      }, function () {
        done();
        say("Could not reach the form service. Please email " + TO + " directly.", "err");
      });
  });
})();
