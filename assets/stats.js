// Sobat's own page counter (the admin console's Analytics). Sends one small
// request per page: the path, the site that linked here (domain only) and
// the kind of device. No cookies, nothing stored in the browser except a
// flag for "first page in this tab", and the server keeps no IP addresses
// (track_page_view in the app repo's 002_website.sql). The URL and
// publishable key are the public ones from config.js.
(function () {
  if (navigator.webdriver || !/(^|\.)getsobat\.in$/.test(location.hostname)) return;
  var ref = "";
  try { var r = new URL(document.referrer); if (r.hostname !== location.hostname) ref = r.hostname; } catch (e) {}
  var w = Math.min(screen.width || 0, window.innerWidth || 0);
  var device = w && w < 768 ? "mobile" : w < 1100 ? "tablet" : "desktop";
  var first = false;
  try { if (!sessionStorage.getItem("sobat-visit")) { sessionStorage.setItem("sobat-visit", "1"); first = true; } } catch (e) {}
  fetch("https://wgdehmtpyrbrwaqyimeo.supabase.co/rest/v1/rpc/track_page_view", {
    method: "POST",
    keepalive: true,
    headers: { apikey: "sb_publishable_bml0WO8M88PcwSrR9-HGUg_qRaNWHJG", "Content-Type": "application/json" },
    body: JSON.stringify({ p_path: location.pathname, p_referrer: ref, p_device: device, p_new_visit: first })
  }).catch(function () {});
})();
