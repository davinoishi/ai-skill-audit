// Tests for the local media-use patch. Run: node --test patch.test.mjs <dir-with-freeze.mjs-and-heygen.mjs>
// No real network is used: public IP literals skip DNS and globalThis.fetch is stubbed.
import { strict as assert } from "node:assert";
import { test } from "node:test";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const dir = resolve(process.env.PATCH_DIR || "./patched");
const { isDirectMediaUrl, isPrivateHostname, freezeUrl } = await import(pathToFileURL(join(dir, "freeze.mjs")));
const { loadEnvFromDir } = await import(pathToFileURL(join(dir, "heygen.mjs")));

test("original upstream cases still hold", () => {
  assert.equal(isDirectMediaUrl("https://cdn.example.com/clip.mp4"), true);
  assert.equal(isDirectMediaUrl("http://example.com/logo.svg"), true);
  assert.equal(isDirectMediaUrl("https://172.40.0.1/a.mp4"), true);
  assert.equal(isDirectMediaUrl("https://11.example.com/a.mp4"), true);
  assert.equal(isDirectMediaUrl("https://www.youtube.com/watch?v=abc"), false);
  assert.equal(isDirectMediaUrl("ftp://example.com/a.mp4"), false);
});

test("bypasses found in the review are now blocked", () => {
  for (const u of [
    "http://[::ffff:7f00:1]/a.mp4", // IPv4-mapped loopback (reproduced bypass)
    "http://[::ffff:c0a8:101]/a.mp4", // IPv4-mapped 192.168.1.1 (reproduced bypass)
    "http://[::]/a.mp4",
    "http://100.64.0.5/a.mp4", // CGNAT / noBGP overlay
    "http://100.127.255.1/a.mp4",
    "http://198.18.0.1/a.mp4",
    "http://[64:ff9b::7f00:1]/a.mp4", // NAT64 → 127.0.0.1
    "http://[2002:c0a8:0101::1]/a.mp4", // 6to4 → 192.168.1.1
    "http://2130706433/a.mp4", // decimal 127.0.0.1
    "http://0x7f.1/a.mp4",
    "http://router/a.mp4", // single-label name
    "http://nas.lan/a.mp4",
    "http://pi.home.arpa/a.mp4",
    "http://localhost./a.mp4",
  ]) {
    assert.equal(isDirectMediaUrl(u), false, `should block ${u}`);
  }
  assert.equal(isPrivateHostname("100.63.255.255"), false, "just below CGNAT is public");
  assert.equal(isPrivateHostname("100.128.0.1"), false, "just above CGNAT is public");
});

test("freezeUrl refuses a redirect to a private address", async () => {
  const realFetch = globalThis.fetch;
  for (const target of ["http://127.0.0.1/x.mp4", "http://[::ffff:7f00:1]/x.mp4", "http://100.64.1.2/x.mp4"]) {
    let calls = 0;
    globalThis.fetch = async (url, opts) => {
      calls++;
      assert.equal(opts?.redirect, "manual");
      return new Response(null, { status: 302, headers: { location: target } });
    };
    await assert.rejects(freezeUrl("https://93.184.215.14/a.mp4", join(tmpdir(), "x")), /blocked/);
    assert.equal(calls, 1, "private hop never fetched");
  }
  globalThis.fetch = realFetch;
});

test("freezeUrl refuses a private first URL without fetching", async () => {
  const realFetch = globalThis.fetch;
  globalThis.fetch = async () => assert.fail("fetch should not run");
  await assert.rejects(freezeUrl("http://192.168.1.1/a.mp4", join(tmpdir(), "x")), /blocked/);
  globalThis.fetch = realFetch;
});

test("freezeUrl still downloads a public URL and follows a public redirect", async () => {
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (url) =>
    String(url).includes("first")
      ? new Response(null, { status: 301, headers: { location: "https://93.184.215.15/second.mp4" } })
      : new Response(new Uint8Array([1, 2, 3]), { status: 200 });
  const dest = join(mkdtempSync(join(tmpdir(), "mu-")), "out.bin");
  assert.equal(await freezeUrl("https://93.184.215.14/first.mp4", dest), 3);
  globalThis.fetch = realFetch;
});

test("loadEnvFromDir imports only allow-listed keys and stops at a project boundary", () => {
  const root = mkdtempSync(join(tmpdir(), "mu-env-"));
  writeFileSync(join(root, ".env"), "UNRELATED_SECRET=leak\nHEYGEN_API_KEY=parent-key\n");
  const proj = join(root, "videos", "demo");
  mkdirSync(proj, { recursive: true });
  delete process.env.UNRELATED_SECRET;
  delete process.env.HEYGEN_API_KEY;

  // 1) project boundary: demo has hyperframes.json and no .env → parent .env NOT read
  writeFileSync(join(proj, "hyperframes.json"), "{}");
  loadEnvFromDir(proj);
  assert.equal(process.env.HEYGEN_API_KEY, undefined);

  // 2) no boundary marker → walks up, but only the allow-listed key is imported
  const loose = join(root, "loose", "dir");
  mkdirSync(loose, { recursive: true });
  loadEnvFromDir(loose);
  assert.equal(process.env.HEYGEN_API_KEY, "parent-key");
  assert.equal(process.env.UNRELATED_SECRET, undefined);
  delete process.env.HEYGEN_API_KEY;
});
