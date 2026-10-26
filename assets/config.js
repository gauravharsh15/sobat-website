// Public by design: the Supabase project URL and its *publishable* key are
// the same values that ship inside the Sobat app. Row-level security and the
// database functions decide what this key can do. Never put a secret key here.
window.SOBAT = {
  supabaseUrl: "https://wgdehmtpyrbrwaqyimeo.supabase.co",
  publishableKey: "sb_publishable_bml0WO8M88PcwSrR9-HGUg_qRaNWHJG",
  // Cloudflare Turnstile site key (public by design; the secret key lives in
  // Supabase only). See assets/captcha.js.
  turnstileSiteKey: ""
};
