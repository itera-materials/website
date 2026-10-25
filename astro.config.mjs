// Static site, English at /, French at /fr/ (D017). No integrations, no client JavaScript.
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://iteramaterials.com",
  trailingSlash: "always",
  i18n: {
    defaultLocale: "en",
    locales: ["en", "fr"],
    routing: { prefixDefaultLocale: false },
  },
  build: { inlineStylesheets: "always" },
  devToolbar: { enabled: false },
});
