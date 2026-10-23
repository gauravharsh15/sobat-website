// Home page motion. The HTML's resting state is always the finished picture
// (3 riders, final numbers, routes drawn), so if this script fails or the
// visitor asks for reduced motion, the page still reads correctly.
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  // ── Example ride: riders join one by one, the fare split updates, and the
  //    departure countdown ticks. Replays every ~11 seconds.
  const card = document.querySelector(".ride-card");
  if (card) rideStory(card);

  function rideStory(card) {
    const FARE = 700;
    const seats = Array.from(card.querySelectorAll(".seat"));
    const riders = document.getElementById("riders-text");
    const splitN = document.getElementById("split-n");
    const splitEach = document.getElementById("split-each");
    const leaves = document.getElementById("leaves-in");
    let secondsLeft = 360;
    let timers = [];
    let ticker = null;

    const later = (ms, fn) => timers.push(setTimeout(fn, ms));
    const fmt = (s) => Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");

    function bump(el) {
      el.classList.remove("bump");
      void el.offsetWidth; // restart the animation
      el.classList.add("bump");
    }

    function setRiders(count, animate) {
      seats.forEach((seat, i) => {
        const wasOpen = seat.classList.contains("open");
        seat.classList.toggle("open", i >= count);
        if (animate && wasOpen && i < count) popSeat(seat);
      });
      const left = seats.length - count;
      riders.textContent = count === 1
        ? "1 rider · 3 seats left"
        : count + " verified riders · " + left + (left === 1 ? " seat left" : " seats left");
      splitN.textContent = "÷ " + count;
      splitEach.textContent = count === 1 ? "waiting for riders" : "about ₹" + Math.round(FARE / count) + " each";
      if (animate) { bump(splitN); bump(splitEach); }
    }

    function popSeat(seat) {
      seat.classList.remove("pop");
      void seat.offsetWidth;
      seat.classList.add("pop");
    }

    function cycle() {
      card.classList.remove("resetting");
      secondsLeft = 360;
      leaves.textContent = fmt(secondsLeft);
      setRiders(1, false);
      later(1600, () => setRiders(2, true));
      later(3800, () => setRiders(3, true));
      later(10200, () => card.classList.add("resetting"));
      later(10700, cycle);
    }

    function start() {
      stop();
      cycle();
      ticker = setInterval(() => {
        secondsLeft = Math.max(0, secondsLeft - 1);
        leaves.textContent = fmt(secondsLeft);
      }, 1000);
    }

    function stop() {
      timers.forEach(clearTimeout);
      timers = [];
      clearInterval(ticker);
    }

    // Don't run while the tab is in the background.
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    start();
  }

  // ── Below-the-fold pieces start when they scroll into view. Anything
  //    already on screen at load is left in its finished state.
  if (!("IntersectionObserver" in window)) return;
  const belowFold = (el) => el.getBoundingClientRect().top > window.innerHeight;

  const counters = Array.from(document.querySelectorAll("[data-count]")).filter(belowFold);
  const art = document.querySelector(".converge-art");
  const watchArt = art && belowFold(art);

  counters.forEach((el) => { el.textContent = "0"; });
  if (watchArt) art.classList.add("armed");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      if (entry.target === art) {
        art.classList.remove("armed");
        art.classList.add("play");
      } else {
        countUp(entry.target);
      }
    });
  }, { threshold: 0.35 });

  counters.forEach((el) => observer.observe(el));
  if (watchArt) observer.observe(art);

  function countUp(el) {
    const target = Number(el.dataset.count);
    const duration = 1300;
    const startTime = performance.now();
    function frame(now) {
      const p = Math.min(1, (now - startTime) / duration);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
})();
