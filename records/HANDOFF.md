# Handoff

Live state of the site. Update whenever any of this changes.

## Publishing
- Host: GitHub Pages, published from the `main` branch root of `Manifold-LLC/Manifold-LLC.github.io`. No build step. `_config.yml` keeps `records/`, `docs/`, `scripts/` and the Markdown files off the published site and includes `.well-known`.
- Domain: `manifold-llc.com` via the `CNAME` file. `manifold-llc.github.io` redirects to it. HTTPS is served by GitHub with a Let's Encrypt certificate.
- Registrar and DNS provider: not recorded yet. Add them here, with where the credentials and recovery codes are kept.
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
- UEI, CAGE, NAICS, socioeconomic status, principal bios, facility-clearance posture and the conflict-of-interest sentence are unconfirmed. See `records/facts.md`.

## Traps
- `CNAME` must stay in the repository root or the custom domain drops.
- The capability statement PDF is generated from `capability-statement.html`. Do not edit the PDF. The page count must stay at one; CI checks it.
- Facts appear in several files. Change `records/facts.md` first, then grep for the old value.
- `404.html` uses absolute asset paths and looks unstyled when opened from disk. That is expected.

## Last updated
2026-11-08
