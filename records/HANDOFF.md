# Handoff

Live state of the site. Update whenever any of this changes.

## Publishing
- Host: GitHub Pages, published from the `main` branch root of `Manifold-LLC/Manifold-LLC.github.io`. No build step, no deploy workflow.
- Domain: `manifold-llc.com` via the `CNAME` file. `manifold-llc.github.io` redirects to it. HTTPS is served by GitHub with a Let's Encrypt certificate.
- Registrar and DNS provider: not recorded yet. Add them here.
- Access: the GitHub organization `Manifold-LLC` has an owner account separate from the maintainer's personal account. Anyone who will push needs Write on the repository or Owner on the organization. Check with `gh api repos/Manifold-LLC/Manifold-LLC.github.io --jq .permissions` before starting work.
- Form service: Web3Forms, not yet configured. The form falls back to `mailto:` until the access key in `index.html` is replaced.

## Check and fix
```
curl -sI https://manifold-llc.com/ | head -12          # 200, server: GitHub.com
curl -s https://manifold-llc.com/ | md5sum; md5sum index.html   # should match once main is deployed
dig manifold-llc.com +noall +answer -t A               # four 185.199.x.153 addresses
npx html-validate@11 "*.html"
```

## Open question
- UEI, CAGE, NAICS, socioeconomic status, principal bios and facility-clearance posture are unconfirmed. See `records/facts.md`.

## Traps
- `CNAME` must stay in the repository root or the custom domain drops.
- The capability statement PDF is generated from `capability-statement.html`. Do not edit the PDF. The page count must stay at one; check it after every render.
- Facts appear in several files. Change `records/facts.md` first, then grep for the old value.
- This container's network policy blocks most outbound hosts. The live site and a short allowlist are reachable; everything else returns 403 from the proxy.

## Last updated
2026-11-08
