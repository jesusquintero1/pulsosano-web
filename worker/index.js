// PulsoSano — Worker principal.
// Sirve los assets estáticos de ./dist y expone una API mínima bajo /api/*:
//   POST /api/newsletter  -> alta en la lista (KV NEWSLETTER)
//   GET  /api/health      -> {"ok":true}
// Cualquier otra ruta /api/* devuelve la página 404 de los assets.
//
// La lista de suscriptores es un activo monetizable propio (patrocinios de
// newsletter, tráfico recurrente que no depende de Google). Se guarda en KV con
// clave `sub:<email>`; exportable con `wrangler kv key list --binding NEWSLETTER`.

const EMAIL_RX = /^[^\s@]{1,64}@[^\s@]{1,255}\.[a-zA-Z]{2,24}$/;
const RATE_LIMIT_TTL = 60; // segundos entre altas por IP

function json(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });
}

async function readInput(request) {
  const ct = request.headers.get("content-type") || "";
  if (ct.includes("application/json")) {
    return await request.json().catch(() => ({}));
  }
  if (ct.includes("form")) {
    const fd = await request.formData().catch(() => null);
    return fd ? Object.fromEntries(fd.entries()) : {};
  }
  return {};
}

async function handleNewsletter(request, env) {
  if (request.method !== "POST") {
    return json({ error: "Método no permitido" }, 405, { allow: "POST" });
  }
  if (!env.NEWSLETTER) {
    return json({ error: "Newsletter temporalmente no disponible" }, 503);
  }

  const input = await readInput(request);
  const email = String(input.email || "").trim().toLowerCase();
  const honeypot = String(input.website || "").trim();
  const source = String(input.source || "").slice(0, 200);

  // Bots que rellenan el campo oculto: respondemos éxito sin guardar nada.
  if (honeypot) return json({ ok: true, message: "¡Listo! Quedaste suscrito." });

  if (!EMAIL_RX.test(email)) {
    return json({ error: "Escribe un correo válido." }, 400);
  }

  const ip = request.headers.get("cf-connecting-ip") || "0.0.0.0";
  const rlKey = `rl:${ip}`;
  if (await env.NEWSLETTER.get(rlKey)) {
    return json({ error: "Demasiados intentos. Espera un minuto." }, 429, { "retry-after": String(RATE_LIMIT_TTL) });
  }
  await env.NEWSLETTER.put(rlKey, "1", { expirationTtl: RATE_LIMIT_TTL });

  const key = `sub:${email}`;
  const existing = await env.NEWSLETTER.get(key);
  if (existing) {
    return json({ ok: true, message: "Ya estabas suscrito. ¡Gracias!" });
  }

  const record = {
    email,
    ts: new Date().toISOString(),
    source,
    country: request.cf?.country || null,
    ua: (request.headers.get("user-agent") || "").slice(0, 200),
  };
  await env.NEWSLETTER.put(key, JSON.stringify(record), {
    metadata: { ts: record.ts, country: record.country },
  });

  return json({ ok: true, message: "¡Listo! Quedaste suscrito." });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/newsletter" || url.pathname === "/api/newsletter/") {
      return handleNewsletter(request, env);
    }
    if (url.pathname === "/api/health") {
      return json({ ok: true, ts: new Date().toISOString() });
    }
    // Resto (incl. /api/* desconocido): assets estáticos (404 propio si no existe).
    return env.ASSETS.fetch(request);
  },
};
