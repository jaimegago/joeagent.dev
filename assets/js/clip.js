/*
  clip.js — overlay for the landing-page demonstration clips.

  Inline clips (layouts/_shortcodes/clip.html) autoplay once, muted, without
  controls, and rest on their final frame. Activating one opens the same sources
  here at up to their native 1280px width — big enough to actually read — picking
  up at the playhead the inline clip had reached, so enlarging reads as the same
  playback continuing. The overlay carries no controls either: it plays on and
  stops on its final frame, same as the inline clip.

  Loaded only on pages that use the clip shortcode — see custom/head-end.html.
  One overlay is built lazily and reused by every clip on the page. No focus-trap
  framework: focus moves to the close button on open and returns to the trigger
  on dismiss. No dependencies.
*/
(function () {
  "use strict";

  var overlay = null; // built on first open, then reused
  var overlayVideo = null;
  var lastTrigger = null;

  function build() {
    overlay = document.createElement("div");
    overlay.className = "joe-clip-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Enlarged demonstration clip");
    overlay.hidden = true;

    var frame = document.createElement("div");
    frame.className = "joe-clip-overlay__frame";

    overlayVideo = document.createElement("video");
    overlayVideo.className = "joe-clip-overlay__video";
    // No controls: the native control bar greys out the bottom of the frame,
    // which is exactly where these clips put their critical content — and its
    // download / playback-rate / picture-in-picture / volume affordances are all
    // irrelevant here. The overlay just plays the clip once, larger, and stops.
    overlayVideo.controls = false;
    overlayVideo.playsInline = true;
    overlayVideo.muted = true; // so the autoplay-on-open is never blocked
    overlayVideo.preload = "auto";

    var close = document.createElement("button");
    close.type = "button";
    close.className = "joe-clip-overlay__close";
    close.setAttribute("aria-label", "Close enlarged clip");
    close.innerHTML = "&times;";
    close.addEventListener("click", hide);

    frame.appendChild(overlayVideo);
    frame.appendChild(close);
    overlay.appendChild(frame);

    // Backdrop click — only when the press lands on the backdrop itself, so
    // dragging the scrub bar and releasing outside the video does not dismiss.
    // preventDefault stops the browser's own mousedown focus from landing on
    // the backdrop after hide() has already returned focus to the trigger.
    overlay.addEventListener("mousedown", function (e) {
      if (e.target !== overlay) return;
      e.preventDefault();
      hide();
    });

    document.body.appendChild(overlay);
    return close;
  }

  function show(figure) {
    var close = overlay ? overlay.querySelector(".joe-clip-overlay__close") : build();

    var inline = figure.querySelector("video");
    if (inline) inline.pause();

    // Pick the overlay up where the inline clip was, so enlarging feels like the
    // same playback continuing rather than a restart. The exception is a clip
    // that has already run out: resuming at its final frame would show nothing,
    // so that one replays from the top.
    var startAt = inline && !inline.ended ? inline.currentTime : 0;

    // Re-point the overlay video at this figure's sources, carrying the playhead
    // as a media fragment. Assigning currentTime on loadedmetadata instead loses
    // a race with the element's own resource selection — the pending seek is
    // clobbered and playback lands back at 0 — whereas #t= is honoured natively.
    overlayVideo.innerHTML = "";
    var sources = figure.querySelectorAll("source");
    for (var i = 0; i < sources.length; i++) {
      var s = document.createElement("source");
      s.src = sources[i].src.split("#")[0] + (startAt > 0.1 ? "#t=" + startAt : "");
      s.type = sources[i].type;
      overlayVideo.appendChild(s);
    }
    if (inline && inline.poster) overlayVideo.poster = inline.poster;
    overlayVideo.setAttribute(
      "aria-label",
      figure.getAttribute("data-joe-clip-label") || "Demonstration clip"
    );

    lastTrigger = figure.querySelector(".joe-clip__trigger");
    overlay.hidden = false;
    document.documentElement.classList.add("joe-clip-overlay-open");

    overlayVideo.load(); // pick up the swapped <source> list
    var played = overlayVideo.play();
    // A blocked autoplay is not worth handling: the clip is muted, which is the
    // case browsers allow.
    if (played && typeof played.catch === "function") played.catch(function () {});

    close.focus();
  }

  function hide() {
    if (!overlay || overlay.hidden) return;
    overlayVideo.pause();
    overlay.hidden = true;
    document.documentElement.classList.remove("joe-clip-overlay-open");
    if (lastTrigger) lastTrigger.focus();
    lastTrigger = null;
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && overlay && !overlay.hidden) hide();
  });

  document.addEventListener("DOMContentLoaded", function () {
    var figures = document.querySelectorAll("[data-joe-clip]");
    for (var i = 0; i < figures.length; i++) {
      (function (figure) {
        var trigger = figure.querySelector(".joe-clip__trigger");
        if (!trigger) return;
        // A real <button>, so Enter/Space already fire click.
        trigger.addEventListener("click", function () {
          show(figure);
        });
      })(figures[i]);
    }
  });
})();
