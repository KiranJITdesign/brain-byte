import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import express from "express";
import nodemailer from "nodemailer";

const here = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(here, "../backend/.env") });

const app = express();
app.disable("x-powered-by");
app.use(express.json({ limit: "256kb" }));

const username = (process.env.SMTP_USERNAME || process.env.MAIL_USER || "").trim();
const gmailHost = username.toLowerCase().endsWith("@gmail.com");
const host = (process.env.MAIL_HOST || process.env.SMTP_HOST || (gmailHost ? "smtp.gmail.com" : "")).trim();
const port = Number(process.env.MAIL_PORT || process.env.SMTP_PORT || 465);
const sender = (process.env.SMTP_FROM || username).trim();
let password = (process.env.SMTP_PASSWORD || process.env.MAIL_PASS || "").trim();
if ((password.startsWith('"') && password.endsWith('"')) || (password.startsWith("'") && password.endsWith("'"))) {
  password = password.slice(1, -1);
}
password = password.replace(/\s+/g, "");
const serviceToken = (process.env.MAIL_SERVICE_TOKEN || "").trim();
const mailConfigured = Boolean(host && Number.isInteger(port) && port > 0 && port <= 65535 && sender && username && password);
const servicePort = Number(process.env.MAIL_SERVICE_PORT || 8025);

const transporter = mailConfigured
  ? nodemailer.createTransport({
      host,
      port,
      secure: (process.env.SMTP_USE_SSL || "false").toLowerCase() === "true" || port === 465,
      auth: { user: username, pass: password },
      connectionTimeout: 15000,
      greetingTimeout: 10000,
      socketTimeout: 20000,
    })
  : null;

function authorized(req) {
  if (!serviceToken) return false;
  const header = req.get("authorization") || "";
  const supplied = header.match(/^Bearer\s+(.+)$/i)?.[1] || "";
  const expectedBytes = Buffer.from(serviceToken);
  const suppliedBytes = Buffer.from(supplied);
  return expectedBytes.length === suppliedBytes.length && crypto.timingSafeEqual(expectedBytes, suppliedBytes);
}

app.get("/health", (_req, res) => {
  res.json({ ok: true, emailConfigured: mailConfigured, serviceTokenConfigured: Boolean(serviceToken) });
});

app.post("/send", async (req, res) => {
  if (!authorized(req)) {
    return res.status(serviceToken ? 401 : 503).json({ ok: false, error: "Mail service authorization is not configured." });
  }
  if (!transporter) {
    return res.status(503).json({ ok: false, error: "Email settings are incomplete in backend/.env." });
  }

  const { to, subject, text, html } = req.body || {};
  if ((!Array.isArray(to) && typeof to !== "string") || !String(to).trim() || !String(subject || "").trim() || (!text && !html)) {
    return res.status(400).json({ ok: false, error: "Provide recipient, subject, and a text or HTML body." });
  }

  try {
    const info = await transporter.sendMail({
      from: sender,
      to,
      subject,
      text: text || undefined,
      html: html || undefined,
    });
    return res.status(200).json({ ok: true, messageId: info.messageId });
  } catch (error) {
    const invalidGoogleLogin = error?.code === "EAUTH" && Number(error?.responseCode) === 535;
    const detail = invalidGoogleLogin
      ? `Gmail rejected the login for ${username}. Set MAIL_PASS to a current Google App Password created for that same account.`
      : error?.message || "Email delivery failed.";
    console.error(`Nodemailer delivery failed (${error?.code || "SMTP_ERROR"}): ${detail}`);
    return res.status(502).json({
      ok: false,
      error: detail,
      code: error?.code || null,
      responseCode: error?.responseCode || null,
    });
  }
});

app.listen(servicePort, "127.0.0.1", () => {
  console.log(`Mail service listening on http://127.0.0.1:${servicePort}`);
  console.log(`SMTP settings ${mailConfigured ? "are present" : "are incomplete"}; shared token ${serviceToken ? "is configured" : "is missing"}.`);
});
