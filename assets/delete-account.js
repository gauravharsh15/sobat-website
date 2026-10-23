// Web account deletion. The visitor signs in with the same method as the app
// (phone OTP or Google), then we call the same delete_own_account() database
// function the app's Profile screen uses. That function only ever deletes the
// signed-in account (auth.uid()), so nobody can delete someone else's.
// Talks to Supabase's REST endpoints with fetch; no client library needed.
// The session lives in memory only and is never stored in the browser.
(function () {
  const API = window.SOBAT.supabaseUrl;
  const KEY = window.SOBAT.publishableKey;
  const $ = (id) => document.getElementById(id);

  let accessToken = null;
  let userId = null;
  let pendingPhone = null;

  function showStep(step) {
    ["step-signin", "step-code", "step-confirm", "step-done"].forEach((id) => { $(id).hidden = id !== step; });
  }

  function setStatus(id, text, kind) {
    const el = $(id);
    el.textContent = text;
    el.dataset.kind = kind || "";
  }

  async function call(path, { method = "POST", body, token } = {}) {
    const headers = { apikey: KEY, "Content-Type": "application/json" };
    if (token) headers.Authorization = "Bearer " + token;
    const res = await fetch(API + path, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
    let data = null;
    try { data = await res.json(); } catch (e) { /* empty body */ }
    if (!res.ok) {
      const err = new Error((data && (data.msg || data.message || data.error_description || data.error)) || "Request failed");
      err.status = res.status;
      err.code = data && (data.error_code || data.code);
      throw err;
    }
    return data;
  }

  // Same rule as normalizePhone in the app (lib/types.ts): numbers without a
  // country code are Indian (+91), and a 12-digit number starting 91 already
  // has it. Returns null if it can't be a phone number.
  function normalizePhone(raw) {
    let n = String(raw).replace(/[^\d+]/g, "");
    if (n.startsWith("00")) n = "+" + n.slice(2);
    if (!n.startsWith("+")) {
      n = n.replace(/^0+/, "");
      n = n.length === 12 && n.startsWith("91") ? "+" + n : "+91" + n;
    }
    if (n.startsWith("+91")) return /^\+91[6-9]\d{9}$/.test(n) ? n : null;
    return /^\+\d{8,15}$/.test(n) ? n : null;
  }

  function maskPhone(p) {
    if (!p) return "";
    const s = p.startsWith("+") ? p : "+" + p;
    return s.slice(0, 3) + " ••••• " + s.slice(-4);
  }

  function maskEmail(e) {
    if (!e || e.indexOf("@") < 1) return e || "";
    const [name, domain] = e.split("@");
    return name[0] + "•••@" + domain;
  }

  async function showSignedIn() {
    try {
      const user = await call("/auth/v1/user", { method: "GET", token: accessToken });
      userId = user.id;
      const label = user.phone ? maskPhone(user.phone) : maskEmail(user.email);
      $("identity").textContent = label || "your Sobat account";
      $("confirm-text").value = "";
      $("delete-btn").disabled = true;
      setStatus("confirm-status", "");
      showStep("step-confirm");
    } catch (err) {
      accessToken = null;
      showStep("step-signin");
      setStatus("signin-status", "Your sign-in expired. Please sign in again.", "error");
    }
  }

  // Phone: send a code. create_user is false so this page never creates new accounts.
  $("phone-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const phone = normalizePhone($("phone").value);
    if (!phone) {
      setStatus("signin-status", "Enter the phone number on your Sobat account.", "error");
      $("phone").focus();
      return;
    }
    $("send-code").disabled = true;
    setStatus("signin-status", "Sending code…");
    try {
      await call("/auth/v1/otp", { body: { phone, create_user: false } });
    } catch (err) {
      let problem = null;
      if (err.status === 429) problem = "Too many attempts. Wait a minute, then try again.";
      else if (/invalid phone/i.test(err.message)) problem = "That doesn't look like a valid phone number.";
      else if (err.status >= 500 || /provider|sms/i.test(err.message)) problem = "Phone sign-in isn't available right now. Try Google, delete in the app, or email us.";
      if (problem) {
        setStatus("signin-status", problem, "error");
        $("send-code").disabled = false;
        return;
      }
      // Anything else, including a number with no account, gets the same message
      // as a success, so this page can't reveal whether a number has an account.
    }
    pendingPhone = phone;
    $("code-phone").textContent = maskPhone(phone);
    $("code").value = "";
    setStatus("code-status", "If this number has a Sobat account, a 6-digit code is on its way.");
    $("send-code").disabled = false;
    setStatus("signin-status", "");
    showStep("step-code");
    $("code").focus();
  });

  $("code-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const token = $("code").value.replace(/\D/g, "");
    if (token.length !== 6) {
      setStatus("code-status", "Enter the 6-digit code from the SMS.", "error");
      return;
    }
    $("verify-code").disabled = true;
    setStatus("code-status", "Checking…");
    try {
      const session = await call("/auth/v1/verify", { body: { type: "sms", phone: pendingPhone, token } });
      accessToken = session.access_token;
      await showSignedIn();
    } catch (err) {
      setStatus("code-status", "That code didn't work. Check it, or request a new one.", "error");
    } finally {
      $("verify-code").disabled = false;
    }
  });

  $("change-number").addEventListener("click", () => {
    pendingPhone = null;
    setStatus("code-status", "");
    showStep("step-signin");
    $("phone").focus();
  });

  // Google: Supabase sends the visitor back here with the session in the URL fragment.
  $("google").addEventListener("click", () => {
    const back = window.location.origin + window.location.pathname;
    window.location.assign(API + "/auth/v1/authorize?provider=google&redirect_to=" + encodeURIComponent(back));
  });

  $("confirm-text").addEventListener("input", (e) => {
    $("delete-btn").disabled = e.target.value.trim().toUpperCase() !== "DELETE";
  });

  $("cancel-btn").addEventListener("click", () => {
    accessToken = null;
    pendingPhone = null;
    showStep("step-signin");
    setStatus("signin-status", "Cancelled. Nothing was deleted.", "ok");
  });

  $("delete-btn").addEventListener("click", async () => {
    if (!accessToken || $("confirm-text").value.trim().toUpperCase() !== "DELETE") return;
    $("delete-btn").disabled = true;
    $("cancel-btn").disabled = true;
    setStatus("confirm-status", "Deleting your account…");
    try {
      // The profile photo lives in Storage, which the database function can't
      // reach, so remove it first. No photo is fine; carry on either way.
      if (userId) {
        await call("/storage/v1/object/avatars", { method: "DELETE", body: { prefixes: [userId + "/avatar.jpg"] }, token: accessToken }).catch(() => {});
      }
      await call("/rest/v1/rpc/delete_own_account", { body: {}, token: accessToken });
      accessToken = null;
      userId = null;
      pendingPhone = null;
      showStep("step-done");
    } catch (err) {
      setStatus("confirm-status", "We couldn't delete the account. Please try again, or email us.", "error");
      $("delete-btn").disabled = false;
    } finally {
      $("cancel-btn").disabled = false;
    }
  });

  // Returning from Google sign-in (or a failed attempt).
  function readReturn() {
    const params = new URLSearchParams(window.location.hash.slice(1) || window.location.search.slice(1));
    const token = params.get("access_token");
    const error = params.get("error_description") || params.get("error");
    if (token || error) history.replaceState(null, "", window.location.pathname);
    if (token) {
      accessToken = token;
      showSignedIn();
    } else if (error) {
      setStatus("signin-status", "Google sign-in didn't complete. Please try again.", "error");
    }
  }

  readReturn();
})();
