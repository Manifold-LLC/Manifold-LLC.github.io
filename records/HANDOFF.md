# Handoff

Live state of the site. Update whenever any of this changes.

## Publishing
- Host: GitHub Pages, published from the `main` branch root of `Manifold-LLC/Manifold-LLC.github.io`. No build step. `_config.yml` keeps `records/`, `docs/`, `scripts/` and the Markdown files off the published site and includes `.well-known`.
- Domain: `manifold-llc.com` via the `CNAME` file. `manifold-llc.github.io` redirects to it. HTTPS is served by GitHub with a Let's Encrypt certificate.
- Registrar and DNS provider: a Cloudflare account exists on the company mailbox (marketing mail from September 2026); the registrar for manifold-llc.com and teammanifold.com is not recorded. Add both here, with where the credentials and recovery codes are kept.
- Email: Google Workspace on teammanifold.com, billed monthly to the company mailbox.
- Registrations: SAM.gov active since 2026-08-21, annual renewal due 2027-08-10. Loudoun County business license and business personal property filings due by 2027-03-01 each year.
- Brand: the logo mark is the "Manifold_Symbol_Master.svg" from the Drive folder "MANIFOLD Symbols SVG", cropped to its bounding box and inlined as an SVG symbol. `assets/img/mark.svg` is a standalone copy.
- Access: pushing needs Write on the repository or Owner on the `Manifold-LLC` organization. Check with `gh api repos/Manifold-LLC/Manifold-LLC.github.io --jq .permissions` before starting work.
- Form service: Web3Forms, not yet configured. The form falls back to `mailto:` until the access key in `index.html` is replaced.
- Checks: `.github/workflows/checks.yml` runs html-validate, a link check, the banned-pattern grep, a facts grep, the security.txt expiry check and the PDF page count on every pull request.

## Check and fix
```
curl -sI https://manifold-llc.com/ | head -12          # 200, server: GitHub.com
curl -s https://manifold-llc.com/ | md5sum; md5sum index.html   # should match once main is deployed
curl -sI https://manifold-llc.com/.well-known/security.txt      # 200 after the first deploy with _config.yml
dig manifold-llc.com +noall +answer -t A               # four 185.199.x.153 addresses
npx html-validate@11 index.html capability-statement.html 404.html
```

## Open question
- Which phone number to publish: (703) 436-1308 (site) or the number on the July 2026 capability statement in Drive.
- Whether to name the sponsor agency on the site, as the July 2026 capability statement does.
- Whether naming the principals' current employers is permitted under their outside-activity rules.
- NAICS codes are from the July 2026 capability statement; confirm against the SAM record.
- FastSAR: is the code public, and is the paper submitted, under review or accepted? The site says "written for" the journal and does not claim the code is available.
- Dark-vessel work: may any of the paper's figures be used on the site? The brief says to ask first.
- When the anonymous review of the trajectory model ends, it can be named under Selected work.

## Traps
- `CNAME` must stay in the repository root or the custom domain drops.
- The capability statement PDF is generated from `capability-statement.html`. Do not edit the PDF. It is two pages; `scripts/render.js` and CI both fail on any other count.
- Facts appear in several files. Change `records/facts.md` first, then grep for the old value.
- `404.html` uses absolute asset paths and looks unstyled when opened from disk. That is expected.

## Last updated
2026-11-08
