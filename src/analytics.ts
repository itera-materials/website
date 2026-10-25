// GoatCounter (D022, replaces Plausible from D021): free, open source, cookieless, EU-hosted.
// Site code from https://<code>.goatcounter.com. Empty = analytics off (no script on the pages, no
// statistics paragraph in the privacy notice).
export const GOATCOUNTER_CODE = "itera";

// count.js pinned to a versioned file with its published integrity hash
// (https://www.goatcounter.com/help/countjs-versions); scripts/check_site.py allows exactly this.
export const GOATCOUNTER_SCRIPT = "https://gc.zgo.at/count.v5.js";
export const GOATCOUNTER_INTEGRITY = "sha384-atnOLvQb9t+jTSipvd75X2yginT4PjVbqDdlJAmxMm+wYElFmeR6EmLP5bYeoRVQ";

export const goatcounterEndpoint = GOATCOUNTER_CODE ? `https://${GOATCOUNTER_CODE}.goatcounter.com/count` : null;
