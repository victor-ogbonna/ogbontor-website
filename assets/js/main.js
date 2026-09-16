/* Ogbontor Engineering Enterprise — site behaviour
   No dependencies. Every feature degrades gracefully if its markup is absent. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Theme ---------- */
  var THEME_KEY = "ogbontor-theme";
  function applyTheme(t) {
    // Light (blue on white) is the brand default; dark is the opt-in navy variant.
    if (t === "dark") document.documentElement.setAttribute("data-theme", "dark");
    else document.documentElement.removeAttribute("data-theme");
  }
  function storedTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }
  // Initial theme is set by an inline script in <head> to avoid a flash.
  var themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      themeBtn.setAttribute("aria-label", "Switch to " + (next === "light" ? "dark" : "light") + " theme");
    });
  }

  /* ---------- Header shadow on scroll ---------- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobile nav ---------- */
  var navToggle = document.querySelector("[data-nav-toggle]");
  var navLinks = document.getElementById("primary-nav");
  if (navToggle && navLinks) {
    var setNav = function (open) {
      navLinks.classList.toggle("is-open", open);
      navToggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open && window.innerWidth <= 900 ? "hidden" : "";
    };
    navToggle.addEventListener("click", function () {
      setNav(!navLinks.classList.contains("is-open"));
    });
    navLinks.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setNav(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) setNav(false);
    });
  }

  /* ---------- Active nav link ---------- */
  var here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("#primary-nav a[href]").forEach(function (a) {
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) === "#" || /^https?:/.test(href)) return;
    if (href.split("#")[0] === here) a.classList.add("is-active");
  });

  /* ---------- Reveal on scroll ---------- */
  var revealables = document.querySelectorAll(".reveal");
  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealables.forEach(function (el) { el.classList.add("is-in"); });
    } else {
      var ro = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          var delay = parseFloat(el.getAttribute("data-delay") || "0");
          setTimeout(function () { el.classList.add("is-in"); }, delay * 1000);
          ro.unobserve(el);
        });
      }, { rootMargin: "0px 0px -60px 0px", threshold: 0.08 });
      revealables.forEach(function (el) { ro.observe(el); });
    }
  }

  /* ---------- Animated stat counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length) {
    var run = function (el) {
      var target = parseFloat(el.getAttribute("data-count"));
      var suffix = el.getAttribute("data-suffix") || "";
      var prefix = el.getAttribute("data-prefix") || "";
      if (reduceMotion || isNaN(target)) { el.textContent = prefix + target + suffix; return; }
      var dur = 1400, t0 = null;
      var step = function (ts) {
        if (t0 === null) t0 = ts;
        var p = Math.min((ts - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        var val = target < 10 ? (target * eased).toFixed(1) : Math.round(target * eased);
        el.textContent = prefix + val + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if (!("IntersectionObserver" in window)) {
      counters.forEach(run);
    } else {
      var co = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { run(en.target); co.unobserve(en.target); }
        });
      }, { threshold: 0.4 });
      counters.forEach(function (el) { co.observe(el); });
    }
  }

  /* ---------- Gallery lightbox ---------- */
  var lb = document.querySelector("[data-lightbox]");
  if (lb) {
    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector(".lightbox-cap");
    var lastFocus = null;
    var open = function (src, alt, cap) {
      lastFocus = document.activeElement;
      lbImg.src = src; lbImg.alt = alt || "";
      lbCap.textContent = cap || "";
      lb.classList.add("is-open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lightbox-close").focus();
    };
    var close = function () {
      lb.classList.remove("is-open");
      lbImg.removeAttribute("src");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };
    document.querySelectorAll("[data-zoom]").forEach(function (fig) {
      var img = fig.querySelector("img");
      if (!img) return;
      fig.setAttribute("tabindex", "0");
      fig.setAttribute("role", "button");
      var cap = fig.querySelector("figcaption");
      var fire = function () {
        open(img.getAttribute("data-full") || img.src, img.alt, cap ? cap.textContent.trim() : "");
      };
      fig.addEventListener("click", fire);
      fig.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fire(); }
      });
    });
    lb.addEventListener("click", function (e) {
      if (e.target === lb || e.target.closest(".lightbox-close")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && lb.classList.contains("is-open")) close();
    });
  }

  /* ---------- Forms (no backend yet — compose an email) ---------- */
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      var to = form.getAttribute("data-mailto");
      var data = new FormData(form);
      var subject = form.getAttribute("data-subject") || "Website enquiry";
      var lines = [];
      data.forEach(function (v, k) {
        if (String(v).trim()) lines.push(k.replace(/_/g, " ").replace(/\b\w/g, function (c) { return c.toUpperCase(); }) + ": " + v);
      });
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var href = "mailto:" + to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n\n"));
      window.location.href = href;
      if (status) {
        status.className = "form-status is-ok";
        status.textContent = "Opening your email app with this message ready to send. If nothing happens, email " + to + " directly.";
      }
    });
  });


  /* ---------- Hero carousel ---------- */
  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll("[data-slide]"));
    if (slides.length < 2) return;
    var dotsBox = root.querySelector("[data-carousel-dots]");
    var idx = 0, timer = null, DELAY = 5200;

    var dots = slides.map(function (_, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-label", "Slide " + (i + 1));
      b.addEventListener("click", function () { go(i); restart(); });
      if (dotsBox) dotsBox.appendChild(b);
      return b;
    });

    function go(n) {
      idx = (n + slides.length) % slides.length;
      slides.forEach(function (s, i) {
        var on = i === idx;
        s.classList.toggle("is-active", on);
        s.setAttribute("aria-hidden", String(!on));
        // keep hidden slides out of the tab order
        s.querySelectorAll("a, button").forEach(function (el) {
          if (on) el.removeAttribute("tabindex"); else el.setAttribute("tabindex", "-1");
        });
      });
      dots.forEach(function (d, i) {
        d.classList.toggle("is-active", i === idx);
        d.setAttribute("aria-selected", String(i === idx));
      });
    }
    function next() { go(idx + 1); }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() { if (!timer && !reduceMotion) timer = setInterval(next, DELAY); }
    function restart() { stop(); start(); }

    var prev = root.querySelector("[data-carousel-prev]");
    var nxt  = root.querySelector("[data-carousel-next]");
    if (prev) prev.addEventListener("click", function () { go(idx - 1); restart(); });
    if (nxt)  nxt.addEventListener("click",  function () { go(idx + 1); restart(); });

    // pause while the visitor is interacting or the tab is hidden
    root.addEventListener("mouseenter", stop);
    root.addEventListener("mouseleave", start);
    root.addEventListener("focusin", stop);
    root.addEventListener("focusout", start);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else start();
    });

    // swipe on touch
    var x0 = null;
    root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; stop(); }, { passive: true });
    root.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) go(idx + (dx < 0 ? 1 : -1));
      x0 = null; start();
    });

    go(0);
    start();
  });


  /* ---------- Registration -> Google Sheet ----------
     Posts as text/plain so the request stays "simple" and never triggers a CORS
     preflight, which Apps Script web apps do not answer. If the endpoint is not
     configured yet, or the network call fails, we fall back to composing an email
     so a registration is never silently lost. */
  document.querySelectorAll("form[data-register]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    var button = form.querySelector('button[type="submit"]');

    function say(kind, msg) {
      if (!status) return;
      status.className = "form-status is-" + kind;
      status.textContent = msg;
    }

    function collect() {
      var data = {}, tracks = [], events = [];
      new FormData(form).forEach(function (v, k) {
        v = String(v).trim();
        if (!v) return;
        if (k === "tracks") tracks.push(v);
        else if (k === "events") events.push(v);
        else data[k] = v;
      });
      data["Attending"] = events.join(", ");
      data["Tracks of interest"] = tracks.join(", ");
      data["Submitted at"] = new Date().toISOString();
      data["Source"] = location.hostname || "local";
      return data;
    }

    // a checkbox group cannot be "required" in HTML, so enforce at-least-one here
    function requireOne() {
      var group = form.querySelector("[data-require-one]");
      if (!group) return true;
      var name = group.getAttribute("data-require-one");
      var boxes = form.querySelectorAll('input[name="' + name + '"]');
      var any = Array.prototype.some.call(boxes, function (b) { return b.checked; });
      if (!any) {
        say("err", "Please tick at least one thing you want to attend.");
        group.scrollIntoView({ block: "center", behavior: "smooth" });
        if (boxes[0]) boxes[0].focus();
      }
      return any;
    }

    function mailtoFallback(data) {
      var lines = Object.keys(data).map(function (k) { return k + ": " + data[k]; });
      var to = form.getAttribute("data-fallback-email");
      window.location.href = "mailto:" + to +
        "?subject=" + encodeURIComponent("Bootcamp registration — " + (data["Full name"] || "")) +
        "&body=" + encodeURIComponent(lines.join("\n\n"));
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (!requireOne()) return;

      var endpoint = (form.getAttribute("data-endpoint") || "").trim();
      var data = collect();

      if (!endpoint) {
        say("ok", "Opening your email app with your registration ready to send. (The organisers can also connect this form directly to their sheet.)");
        mailtoFallback(data);
        return;
      }

      var original = button ? button.innerHTML : "";
      if (button) { button.disabled = true; button.textContent = "Submitting…"; }
      say("ok", "Sending your registration…");

      var body = JSON.stringify(data);
      var done = function (msg, kind) {
        if (kind !== "err") form.reset();
        say(kind || "ok", msg);
        if (button) { button.disabled = false; button.innerHTML = original; }
      };

      // Apps Script cold-starts can take 30s+, so allow generous headroom before
      // giving up — aborting early would throw away a submission that was fine.
      var controller = ("AbortController" in window) ? new AbortController() : null;
      var timer = setTimeout(function () {
        if (controller) controller.abort();
      }, 60000);
      var slowNote = setTimeout(function () {
        say("ok", "Still sending… the registration server can take up to a minute to wake up. Please don't close this page.");
      }, 6000);

      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=utf-8" },
        body: body,
        signal: controller ? controller.signal : undefined
      }).then(function (r) {
        clearTimeout(timer); clearTimeout(slowNote);
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.text();
      }).then(function () {
        done("You are registered. We will email you with the dates and what to bring — check your spam folder if you don't see it.");
      }).catch(function () {
        clearTimeout(timer); clearTimeout(slowNote);
        // The response may have been unreadable (CORS/redirect/timeout) even though
        // the row would have been written. Retry once fire-and-forget: an opaque
        // no-cors POST still reaches Apps Script, we just cannot read the reply.
        try {
          fetch(endpoint, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: body
          }).then(function () {
            done("Your registration has been sent. If you don't hear from us within a few days, email " +
                 form.getAttribute("data-fallback-email") + " so we can check.");
          }).catch(function () {
            done("We could not reach the registration server. Opening your email app instead so your registration still reaches us.", "err");
            mailtoFallback(data);
          });
        } catch (e) {
          done("We could not reach the registration server. Opening your email app instead so your registration still reaches us.", "err");
          mailtoFallback(data);
        }
      });
    });
  });


  /* ---------- Pre-warm the registration endpoint ----------
     Apps Script has no process running between requests: the first call after a
     quiet spell pays ~30s of container start-up, Sheets binding and auth. But
     there is always a gap between someone heading for the form and submitting
     it. We use that gap — a cheap GET on intent wakes the container so the real
     POST lands on a warm one.

     Fired on: hovering or tapping any link to the register page, and on the
     register page itself (load, first interaction, then a slow heartbeat while
     the form is being filled in). Throttled so it can never spam the quota. */
  (function () {
    var meta = document.querySelector('meta[name="register-endpoint"]');
    var endpoint = meta ? (meta.getAttribute("content") || "").trim() : "";
    if (!endpoint) return;

    var MIN_GAP = 45000;     // never warm more than once every 45s
    var HEARTBEAT = 90000;   // while filling the form
    var MAX_WARMS = 12;      // hard ceiling per page view
    var last = 0, count = 0, beat = null;

    function warm() {
      var now = Date.now();
      if (count >= MAX_WARMS || now - last < MIN_GAP) return;
      last = now; count++;
      try {
        // no-cors: we do not need the reply, only the wake-up. Errors are
        // irrelevant here — this is best-effort and must never surface.
        fetch(endpoint, { method: "GET", mode: "no-cors", cache: "no-store" })
          .catch(function () {});
      } catch (e) {}
    }

    // 1. Intent: someone is heading for the register page
    var seen = false;
    function onIntent() {
      if (seen) return;
      seen = true;
      warm();
    }
    document.querySelectorAll('a[href*="register"]').forEach(function (a) {
      a.addEventListener("pointerenter", onIntent, { once: true, passive: true });
      a.addEventListener("focus", onIntent, { once: true });
      a.addEventListener("pointerdown", warm, { passive: true });
    });

    // 2. On the register page itself
    var form = document.querySelector("form[data-register]");
    if (!form) return;

    warm();                                   // they have arrived — wake it now
    form.addEventListener("focusin", warm);   // and again once they start typing

    function stopBeat() { if (beat) { clearInterval(beat); beat = null; } }
    beat = setInterval(function () {
      // only keep it warm while the tab is actually in front of someone
      if (!document.hidden) warm();
      if (count >= MAX_WARMS) stopBeat();
    }, HEARTBEAT);

    form.addEventListener("submit", stopBeat);
    window.addEventListener("pagehide", stopBeat);
  })();

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
