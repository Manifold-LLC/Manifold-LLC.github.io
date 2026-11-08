# Handoff

Live state of the site. Update whenever any of this changes.

## Publishing
- Host: GitHub Pages, published from the `main` branch root of `Manifold-LLC/Manifold-LLC.github.io`. No build step. `_config.yml` keeps `records/`, `docs/`, `scripts/` and the Markdown files off the published site and includes `.well-known`.
- Domain: `manifold-llc.com` via the `CNAME` file. `manifold-llc.github.io` redirects to it. HTTPS is served by GitHub with a Let's Encrypt certificate.
- Registrar and DNS provider: a Cloudflare account exists on the company mailbox (marketing mail from September 2026); the registrar for manifold-llc.com and teammanifold.com is not recorded. Add both here, with where the credentials and recovery codes are kept.
- Email: Google Workspace, primary domain teammanifold.com, with manifold-llc.com as a user alias domain (verified 2026-11-08). Mail to info@manifold-llc.com and info@teammanifold.com lands in the same inbox. DNS for manifold-llc.com carries the Gmail MX, SPF and DKIM records; DMARC is not yet published (add a TXT at `_dmarc`: `v=DMARC1; p=none; rua=mailto:info@manifold-llc.com`).
- Registrar and DNS: Cloudflare, account login info@teammanifold.com (domain registered there 2026-05-19). A DNS-edit API token was created on 2026-11-08 but was rejected as invalid when used; delete or replace it under My Profile, API Tokens.
- Registrations: SAM.gov active since 2026-08-21, annual renewal due 2027-08-10. Loudoun County business license and business personal property filings due by 2027-03-01 each year.
- Brand: the logo mark is the "Manifold_Symbol_Master.svg" from the Drive folder "MANIFOLD Symbols SVG", cropped to its bounding box and inlined as an SVG symbol. `assets/img/mark.svg` is a standalone copy.
- Access: pushing needs Write on the repository or Owner on the `Manifold-LLC` organization. Check with `gh api repos/Manifold-LLC/Manifold-LLC.github.io --jq .permissions` before starting work.
- Form service: Web3Forms, free plan, account info@manifold-llc.com, form "manifold-llc.com contact". The public access key is in `index.html`; submissions are emailed to the account address. Dashboard: app.web3forms.com.
- Checks: `.github/workflows/checks.yml` runs html-validate, a link check, the banned-pattern grep, a facts grep, the security.txt expiry check and the PDF page count on every pull request.

## Check and fix
```
curl -sI https://manifold-llc.com/ | head -12          # 200, server: GitHub.com
curl -s https://manifold-llc.com/ | md5sum; md5sum index.html   # should match once main is deployed
curl -sI https://manifold-llc.com/.well-known/security.txt      # 200 after the first deploy with _config.yml
dig manifold-llc.com +noall +answer -t A               # four 185.199.x.153 addresses
npx html-validate@11 index.html capability-statement.html 404.html
```

## To do outside this repository
- teammanifold.com still serves a Squarespace "Coming Soon" page. Its DNS is on Google Cloud DNS nameservers (the former Google Domains, now Squarespace Domains), with A records pointing at Squarespace. Set a permanent redirect of teammanifold.com and www.teammanifold.com to https://manifold-llc.com/ in the Squarespace Domains panel (Domains, teammanifold.com, Forwarding), or move the domain's DNS to Cloudflare and use a redirect rule there. Keep the MX, SPF and DKIM records; mail for info@teammanifold.com still lands on them.
- DMARC for manifold-llc.com is not published. In Cloudflare DNS add a TXT record at `_dmarc` with value `v=DMARC1; p=none; rua=mailto:info@manifold-llc.com`. Consider the same for teammanifold.com.
- The Web3Forms access key is public by design, so anyone can post to it; domain restriction on Web3Forms is a paid feature. If spam appears, move to the paid plan or switch to a service with a server-side secret.

## Open question
- NAICS codes are from the July 2026 capability statement; confirm against the SAM record.
- When the review of the trajectory model ends, its case note can be made specific. Owner's standing rule: no numbers from any of the three research projects on the site or in this repository.

## Traps
- `CNAME` must stay in the repository root or the custom domain drops.
- The capability statement PDF is generated from `capability-statement.html` by `scripts/render.js`, which also sets the PDF Author with `scripts/pdf-metadata.py` (needs `pypdf`). Do not edit the PDF. It is two pages, page one standing alone; the render script and CI both fail on any other count. The share image `assets/img/og.png` comes from `scripts/og.html`; change its copy when the headline changes.
- Facts appear in several files. Change `records/facts.md` first, then grep for the old value.
- `404.html` uses absolute asset paths and looks unstyled when opened from disk. That is expected.

## Last updated
2026-11-08
