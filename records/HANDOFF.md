# Handoff

Live state of the site. Update whenever any of this changes.

## Publishing
- Host: GitHub Pages, published from the `main` branch root of `Manifold-LLC/Manifold-LLC.github.io`. No build step. `_config.yml` keeps `records/`, `docs/`, `scripts/` and the Markdown files off the published site and includes `.well-known`.
- Domain: `manifold-llc.com` via the `CNAME` file. `manifold-llc.github.io` redirects to it. HTTPS is served by GitHub with a Let's Encrypt certificate.
- In front of GitHub: since 2026-11-11 the site is served through Cloudflare's proxy. The four A records and the `www` CNAME are set to Proxied, encryption mode is Full, and a Cloudflare Worker named `manifold-visits` runs on `manifold-llc.com/*` and `www.manifold-llc.com/*`. It passes every request through unchanged and keeps request statistics in a D1 database of the same name; its source, with comments, lives in the Cloudflare dashboard and not in this repository. Bot Fight Mode and Email Address Obfuscation are off because both rewrite the pages, and Browser Cache TTL is set to respect the site's own headers. To take Cloudflare out of the path, set those five records back to DNS only; the site reverts to direct GitHub within about five minutes and nothing else needs changing.
- teammanifold.com: bought through Google Workspace in April 2026 and registered with Squarespace Domains (Google's Workspace notice of 2026-04-12 says so). Sign in at account.squarespace.com with Google as Info@teammanifold.com; the domain also appears under Domains in the Workspace Admin Console. DNS is on Google Cloud DNS nameservers (ns-cloud-c1 to c4.googledomains.com) with Squarespace's parking A records and the Google mail records. Record here where recovery codes are kept.
- Email: Google Workspace, primary domain teammanifold.com, with manifold-llc.com as a user alias domain (verified 2026-11-08). Mail to info@manifold-llc.com and info@teammanifold.com lands in the same inbox. DNS for manifold-llc.com carries the Gmail MX, SPF and DKIM records; DMARC published 2026-11-09 at `_dmarc` with `p=none` and reports to info@manifold-llc.com; tighten to `p=quarantine` once a few weeks of reports look clean.
- Registrar and DNS: Cloudflare, account login info@teammanifold.com (domain registered there 2026-05-19). A DNS-edit API token created on 2026-11-08 was invalid; a replacement made on 2026-11-09 works and is saved on the maintainer's cloud environment. Delete the invalid one under My Profile, API Tokens.
- Registrations: SAM.gov active since 2026-08-21, annual renewal due 2027-08-10. Loudoun County business license and business personal property filings due by 2027-03-01 each year.
- Brand: the logo mark is the "Manifold_Symbol_Master.svg" from the Drive folder "MANIFOLD Symbols SVG", cropped to its bounding box and inlined as an SVG symbol. `assets/img/mark.svg` is a standalone copy.
- Access: pushing needs Write on the repository or Owner on the `Manifold-LLC` organization. Check with `gh api repos/Manifold-LLC/Manifold-LLC.github.io --jq .permissions` before starting work.
- Form service: Web3Forms, free plan, account info@manifold-llc.com, form "manifold-llc.com contact". The public access key is in `index.html`; submissions are emailed to the account address. Dashboard: app.web3forms.com.
- Checks: `.github/workflows/checks.yml` runs html-validate, a link check, the banned-pattern grep, a facts grep, the security.txt expiry check and the PDF page count on every pull request.

## Check and fix
```
curl -sI https://manifold-llc.com/ | head -12          # 200, server: cloudflare, a cf-ray header, no set-cookie
curl -s https://manifold-llc.com/ | md5sum; md5sum index.html   # should match once main is deployed
curl -sI https://manifold-llc.com/.well-known/security.txt      # 200 after the first deploy with _config.yml
dig manifold-llc.com +noall +answer -t A               # four 185.199.x.153 addresses
npx html-validate@11 index.html capability-statement.html 404.html
```

## To do outside this repository
- teammanifold.com forwards to https://manifold-llc.com with a 301 since 2026-11-09, set in Squarespace Domains (Website, Domain Forwarding, subdomains @ and www). The bare domain redirected within minutes; check that www.teammanifold.com also resolves and redirects once Squarespace's 24 to 48 hour window has passed. MX, SPF and DKIM for teammanifold.com were untouched.
- DMARC for manifold-llc.com was published on 2026-11-09 through the Cloudflare API (`p=none`, reports to info@manifold-llc.com). Consider the same for teammanifold.com, whose DNS is not on Cloudflare.
- The Web3Forms access key is public by design, so anyone can post to it; domain restriction on Web3Forms is a paid feature. If spam appears, move to the paid plan or switch to a service with a server-side secret.

## Open question
- NAICS codes are from the July 2026 capability statement; confirm against the SAM record.
- When the review of the trajectory model ends, its case note can be made specific. Owner's standing rule: no numbers from any of the three research projects on the site or in this repository.

## Traps
- `CNAME` must stay in the repository root or the custom domain drops.
- The capability statement PDF is generated from `capability-statement.html` and the one-page overview (the slick sheet) from `slick-sheet.html`, both by `scripts/render.js`, which also sets the PDF Author with `scripts/pdf-metadata.py` (needs `pypdf`). Do not edit the PDFs. The capability statement is two pages and the overview is one; the render script and CI fail on any other count. The overview's QR code (`assets/img/qr-site.svg`, made with `segno`) and acquisition-cycle diagram (inline SVG in `slick-sheet.html`, so its labels use the page fonts) were generated by short Python snippets, not drawn by hand. The share image `assets/img/og.png` comes from `scripts/og.html`; change its copy when the headline changes.
- Facts appear in several files. Change `records/facts.md` first, then grep for the old value.
- GitHub Pages tells browsers to cache files for ten minutes, so a changed stylesheet or script can run against a stale copy of the other. Every CSS and JS link carries a content hash (`?v=...`). After editing anything in `assets/css` or `assets/js`, run `python3 scripts/stamp.py` and commit the page changes with it; CI fails if the stamps are stale.
- `404.html` uses absolute asset paths and looks unstyled when opened from disk. That is expected.
- Cloudflare caches images, PDFs, CSS and JS for the ten minutes GitHub's headers ask for, so a freshly deployed PDF can be the old one for that long. To see it at once, clear the cache in the Cloudflare dashboard (Caching, Configuration, Purge Everything). Pages themselves are never cached.
- GitHub renews the custom domain's certificate by checking that the domain points at GitHub, which it no longer appears to do. If that renewal lapses, Cloudflare's Full mode still connects, so visitors see no difference. A certificate or 52x error page from Cloudflare is the sign to switch the records to DNS only while it is sorted out.
- Links inside the print pages must be absolute (`https://manifold-llc.com/...`). A relative link is baked into the PDF as the address of the local render server.

## Last updated
2026-11-11
