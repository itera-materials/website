// Plausible Analytics (D021): cookieless, EU-hosted. Paste the site's script id from Plausible →
// Site settings → Site installation: the part after "pa-" in https://plausible.io/js/pa-XXXX.js.
// Empty = analytics off (no script on the pages, no analytics paragraph in the privacy notice).
export const PLAUSIBLE_ID = "";

export const plausibleScript = PLAUSIBLE_ID ? `https://plausible.io/js/pa-${PLAUSIBLE_ID}.js` : null;

// Plausible's standard init line; scripts/check_site.py allows exactly this inline script.
export const PLAUSIBLE_INIT =
  "window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()";
