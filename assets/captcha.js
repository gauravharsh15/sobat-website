// Cloudflare Turnstile: the "are you a person?" check on this site's forms
// (the newsletter, and phone codes on the delete-account page). Usually
// invisible; Cloudflare shows a checkbox only when it isn't sure. The token
// is checked server side: by the newsletter Edge Function, and by Supabase
// Auth for phone codes. Each token works once, so forms reset it after use.
(function () {
  const pending = [];
  window.sobatCaptcha = function (el, action) {
    const state = { id: null, token: "" };
    const mount = () => {
      state.id = window.turnstile.render(el, {
        sitekey: window.SOBAT.turnstileSiteKey,
        action,
        appearance: "interaction-only",
        callback: (t) => { state.token = t; },
        "expired-callback": () => { state.token = ""; },
        "error-callback": () => { state.token = ""; }
      });
    };
    if (window.SOBAT.turnstileSiteKey) {
      if (window.turnstile) mount(); else pending.push(mount);
    }
    return {
      token: () => state.token,
      reset: () => {
        state.token = "";
        if (state.id !== null && window.turnstile) window.turnstile.reset(state.id);
      }
    };
  };
  window.onSobatCaptchaReady = () => pending.splice(0).forEach((f) => f());
  const s = document.createElement("script");
  s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=onSobatCaptchaReady";
  s.async = true;
  s.defer = true;
  document.head.appendChild(s);
})();
