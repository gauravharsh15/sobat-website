// Newsletter sign-up. Calls the subscribe_newsletter() database function,
// which only adds an email to the list; nothing on this site can read the list.
(function () {
  const form = document.getElementById("updates-form");
  if (!form) return;
  const input = document.getElementById("updates-email");
  const status = document.getElementById("updates-status");
  const button = form.querySelector('button[type="submit"]');

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
    button.disabled = true;
    show("Subscribing…");
    try {
      const res = await fetch(window.SOBAT.supabaseUrl + "/rest/v1/rpc/subscribe_newsletter", {
        method: "POST",
        headers: { apikey: window.SOBAT.publishableKey, "Content-Type": "application/json" },
        body: JSON.stringify({ p_email: email })
      });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      show("You're on the list. We'll email you when Sobat launches.", "ok");
    } catch (err) {
      show("Couldn't subscribe right now. Please try again in a minute.", "error");
    } finally {
      button.disabled = false;
    }
  });
})();
