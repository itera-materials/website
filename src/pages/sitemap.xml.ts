// sitemap.xml for search engines: every page with its language alternates; lastmod = build date.
import type { APIRoute } from "astro";

const PAGES = [
  { en: "/", fr: "/fr/" },
  { en: "/privacy/", fr: "/fr/confidentialite/" },
];

export const GET: APIRoute = ({ site }) => {
  const url = (path: string) => new URL(path, site).href;
  const today = new Date().toISOString().slice(0, 10);
  const entries = PAGES.flatMap((page) =>
    (["en", "fr"] as const).map(
      (lang) => `  <url>
    <loc>${url(page[lang])}</loc>
    <lastmod>${today}</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="${url(page.en)}"/>
    <xhtml:link rel="alternate" hreflang="fr" href="${url(page.fr)}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="${url(page.en)}"/>
  </url>`,
    ),
  );
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${entries.join("\n")}
</urlset>
`;
  return new Response(body, { headers: { "Content-Type": "application/xml" } });
};
