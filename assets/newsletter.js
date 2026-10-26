// Newsletter sign-up. Posts to the "newsletter" Edge Function, which checks
// the Turnstile token with Cloudflare and then adds the email to the list;
// nothing on this site can read the list.
(function () {
  const form = document.getElementById("updates-form");
  if (!form) return;
  const input = document.getElementById("updates-email");
  const status = document.getElementById("updates-status");
  const button = form.querySelector('button[type="submit"]');
  const captcha = window.sobatCaptcha(document.getElementById("updates-captcha"), "newsletter");

  function show(text, kind) {
    status.textContent = text;
    status.dataset.kind = kind || "";
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = input.value.trim().toLowerCase();
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || email.length > 254) {
      show("Enter a valid email address.", "error");
      input.focus();
      return;
    }
    // Hidden field that only bots fill in.
    if (form.elements.website.value) {
      show("You're on the list.", "ok");
      return;
    }
    if (!captcha.token()) {
      show("One moment: checking you're not a bot. Try again in a few seconds.", "error");
      return;
    }
    button.disabled = true;
    show("Subscribing…");
    try {
      const res = await fetch(window.SOBAT.supabaseUrl + "/functions/v1/newsletter", {
        method: "POST",
        headers: { apikey: window.SOBAT.publishableKey, "Content-Type": "application/json" },
        body: JSON.stringify({ email, token: captcha.token() })
      });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      show("You're on the list. We'll email you when Sobat launches.", "ok");
    } catch (err) {
      show("Couldn't subscribe right now. Please try again in a minute.", "error");
    } finally {
      captcha.reset();
      button.disabled = false;
    }
  });
})();
