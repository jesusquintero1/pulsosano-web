// pulsosano.org -> pulsosano.com (301 permanent, preserva path + query)
// Worker minimo solo para SEO y defensa de marca.

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const target = "https://pulsosano.com" + url.pathname + url.search;
    return Response.redirect(target, 301);
  }
};
