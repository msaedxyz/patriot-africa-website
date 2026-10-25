/* Patriot Africa site script. No dependencies. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");

  /* header: menu toggle and scrolled state */
  var header = document.querySelector(".site-header");
  var menuBtn = document.querySelector(".menu-btn");
  if (menuBtn && header) {
    menuBtn.addEventListener("click", function () {
      var open = header.hasAttribute("data-open");
      if (open) header.removeAttribute("data-open"); else header.setAttribute("data-open", "");
      menuBtn.setAttribute("aria-expanded", String(!open));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && header.hasAttribute("data-open")) {
        header.removeAttribute("data-open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }
  var mobileCta = document.querySelector(".mobile-cta");
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) { if (y > 24) header.setAttribute("data-scrolled", ""); else header.removeAttribute("data-scrolled"); }
    if (mobileCta) { if (y > 520) mobileCta.setAttribute("data-show", ""); else mobileCta.removeAttribute("data-show"); }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* reveal: only elements below the first screen get the lift, so the first frame is complete */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if ("IntersectionObserver" in window && !reduce) {
    var items = [].slice.call(document.querySelectorAll("[data-reveal]"));
    var vh = window.innerHeight || 800;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove("pre"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top > vh) { el.classList.add("pre"); io.observe(el); }
    });
  }

  /* fleet tabs */
  [].slice.call(document.querySelectorAll("[data-tabs]")).forEach(function (root) {
    var tabs = [].slice.call(root.querySelectorAll('[role="tab"]'));
    var panels = [].slice.call(root.querySelectorAll('[role="tabpanel"]'));
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i, false); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, n = tabs.length;
        if (k === "ArrowRight") { e.preventDefault(); select((i + 1) % n, true); }
        if (k === "ArrowLeft") { e.preventDefault(); select((i - 1 + n) % n, true); }
        if (k === "Home") { e.preventDefault(); select(0, true); }
        if (k === "End") { e.preventDefault(); select(n - 1, true); }
      });
    });
    select(0, false);
  });

  /* corridor map highlight */
  [].slice.call(document.querySelectorAll("[data-corridors]")).forEach(function (root) {
    var map = root.querySelector(".map");
    var btns = [].slice.call(root.querySelectorAll("[data-corridor]"));
    function set(id) {
      btns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-corridor") === id)); });
      [].slice.call(map.querySelectorAll(".route")).forEach(function (r) {
        r.classList.toggle("is-active", r.getAttribute("data-route") === id);
      });
      if (id) map.setAttribute("data-active", id); else map.removeAttribute("data-active");
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        set(b.getAttribute("data-corridor"));
      });
      b.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) set(b.getAttribute("data-corridor")); });
    });
    var start = root.getAttribute("data-start");
    if (start) set(start);
  });

  /* copy buttons */
  function copyText(text, btn) {
    var done = function () { var t = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = t; }, 1600); };
    try {
      navigator.clipboard.writeText(text).then(done, function () { selectFallback(btn); });
    } catch (e) { selectFallback(btn); }
  }
  function selectFallback(btn) {
    var target = document.getElementById(btn.getAttribute("data-copy-target") || "");
    if (!target) return;
    var r = document.createRange(); r.selectNodeContents(target);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
    btn.textContent = "Selected, press copy";
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("[data-copy]");
    if (!btn) return;
    var val = btn.getAttribute("data-copy");
    if (!val && btn.getAttribute("data-copy-target")) {
      var el = document.getElementById(btn.getAttribute("data-copy-target"));
      val = el ? el.textContent : "";
    }
    copyText(val, btn);
  });

  /* quote form */
  var form = document.getElementById("quote-form");
  if (form) {
    var result = document.getElementById("quote-result");
    var summaryEl = document.getElementById("quote-summary");
    var mailLink = document.getElementById("quote-mail");
    var email = form.getAttribute("data-email") || "";
    var endpoint = form.getAttribute("data-endpoint") || "";

    var params = new URLSearchParams(window.location.search);
    ["origin", "destination", "cargo"].forEach(function (k) {
      var v = params.get(k); var f = form.elements[k];
      if (v && f) f.value = v;
    });

    function fieldOf(el) { return el.closest(".field"); }
    function setError(el, msg) {
      var f = fieldOf(el); if (!f) return;
      var e = f.querySelector(".err");
      if (msg) {
        f.setAttribute("data-invalid", "");
        if (!e) { e = document.createElement("p"); e.className = "err"; e.id = el.id + "-err"; f.appendChild(e); }
        e.textContent = msg;
        el.setAttribute("aria-invalid", "true");
        el.setAttribute("aria-describedby", e.id);
      } else {
        f.removeAttribute("data-invalid");
        if (e) e.remove();
        el.removeAttribute("aria-invalid");
        el.removeAttribute("aria-describedby");
      }
    }
    function messageFor(el) {
 if (el.validity.valueMissing && el.tagName === "SELECT") return "Select a " + (el.getAttribute("data-label") || "option").toLowerCase() + ".";
      if (el.validity.valueMissing) return "Enter " + (el.getAttribute("data-label") || "this detail").toLowerCase() + ".";
      if (el.validity.typeMismatch && el.type === "email") return "Enter an email address in the format name@company.com.";
      if (el.validity.rangeUnderflow || el.validity.badInput) return "Enter a weight in tonnes, for example 32.";
      return "";
    }
    [].slice.call(form.querySelectorAll("input, select, textarea")).forEach(function (el) {
      el.addEventListener("blur", function () { if (el.value) setError(el, messageFor(el)); });
      el.addEventListener("input", function () { if (fieldOf(el) && fieldOf(el).hasAttribute("data-invalid")) setError(el, messageFor(el)); });
    });

    function summary() {
      var d = new FormData(form);
      var g = function (k) { return (d.get(k) || "").toString().trim(); };
      var lines = [
        "QUOTE REQUEST",
        "",
        "Name: " + g("name"),
        "Company: " + (g("company") || "-"),
        "Email: " + g("email"),
        "Phone: " + (g("phone") || "-"),
        "",
        "Origin: " + g("origin"),
        "Destination: " + g("destination"),
        "Collection date: " + (g("date") || "Flexible"),
        "",
        "Cargo: " + g("cargo"),
        "Load: " + (g("load") || "Not sure"),
        "Approx. weight: " + (g("weight") ? g("weight") + " t" : "-"),
        "Hazardous: " + (g("hazardous") || "No"),
        "",
        "Notes: " + (g("notes") || "-")
      ];
      return lines.join("\n");
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var first = null;
      [].slice.call(form.querySelectorAll("input, select, textarea")).forEach(function (el) {
        if (el.type === "hidden" || el.closest(".hp")) return;
        var m = messageFor(el);
        setError(el, m);
        if (m && !first) first = el;
      });
      if (first) { first.focus(); return; }
      var text = summary();
      var showResult = function (sent) {
        summaryEl.textContent = text;
        var subject = "Quote request: " + form.elements.origin.value + " to " + form.elements.destination.value;
        if (mailLink) mailLink.href = "mailto:" + email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(text);
        result.querySelector("[data-sent]").hidden = !sent;
        result.querySelector("[data-unsent]").hidden = sent;
        form.hidden = true;
        result.hidden = false;
        result.focus();
        if (window.dataLayer) window.dataLayer.push({ event: "quote_submit", sent: sent });
      };
      if (endpoint) {
        var btn = form.querySelector('[type="submit"]');
        btn.disabled = true; btn.textContent = "Sending";
        fetch(endpoint, {
          method: "POST",
          headers: { Accept: "application/json", "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(new FormData(form)).toString()
        })
          .then(function (r) { showResult(r.ok); })
          .catch(function () { showResult(false); });
      } else {
        showResult(false);
      }
    });

    var again = document.getElementById("quote-again");
    if (again) again.addEventListener("click", function () { result.hidden = true; form.hidden = false; form.elements.name.focus(); });
  }

  /* an image that fails to load hides itself, so its frame shows the background colour */
  function hideBroken(im) { im.style.visibility = "hidden"; }
  document.addEventListener("error", function (e) { if (e.target && e.target.tagName === "IMG") hideBroken(e.target); }, true);
  [].slice.call(document.images).forEach(function (im) { if (im.complete && im.naturalWidth === 0) hideBroken(im); });

  /* footer year */
  var y = document.getElementById("year");
  if (y) y.textContent = String(new Date().getFullYear());
})();
