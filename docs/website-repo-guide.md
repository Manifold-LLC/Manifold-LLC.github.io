# How to build and run a small company's website repository

This guide is for whoever maintains the company website next, whether they are starting it or taking it over. It assumes a small professional-services firm: a handful of pages, a contact form, one or two PDFs, a custom domain, GitHub Pages as the host, and no backend. The audience for the site is government program offices, prime contractors, and the people who search for the company before a meeting.

It combines published standards with the company's own rules. Company rules are tagged `[site]`, and most are traced to a specific failure on an earlier version of this site. Where the two disagree, the company rule wins. Sources are listed at the end, and where a rule rests on a source, the source is named in the text.

## Terms used throughout

- **Owner**: the human who directs the site. If nobody else has been named, it is the person you are working for in the session. Decisions about claims, spending, launches, domain changes and anything that names a customer belong to the Owner.
- **Page**: one HTML document served at one URL. The site has one content page, a 404 page and a print page for the capability statement.
- **Claim**: any sentence on the site that a reader could check: a clearance, a past engagement, a certification, a number, a partner's name.
- **Fact**: a company data point that must match an outside record exactly: legal name, UEI, CAGE code, NAICS codes, size status, address, phone, email.
- **Of record**: a page, PDF or claim is *of record* once it is reachable at the production domain. Drafts on a branch, preview builds and local renders are not of record. The stricter rules below apply only to things of record.
- **Generated asset**: any file that a script produced from other files in the repo: an SVG drawing, a PDF, a social-share image, a favicon.
- **Facts register**: the one file (`records/facts.md`) that lists every Fact, its source, and the date it was last checked.

---

## 0. Starting a session

Do this before anything else, every session:

1. Read `records/HANDOFF.md`.
2. Read `CHANGELOG.md` from the top. The newest entry is first, and some entries exist only to retract a claim.
3. Read `records/facts.md`. Anything marked "unconfirmed" or "on request" is a gap, not a fact.
4. Run these:
   ```
   git status && git log --oneline -20
   git remote -v && git ls-remote --heads origin
   curl -sI https://<domain>/ | head -20
   ```
5. Check that what is live matches what the default branch holds. On GitHub Pages the default branch usually *is* the site, so `curl -s https://<domain>/ | md5sum` should match `md5sum index.html`. If it does not, stop and work out why before you change anything.
6. Before saying that something was never done or does not exist, grep the changelog and list the artifact directories. `[site]`
   - Your context may have been summarized, and old work drops out of it. Absence from memory is not evidence.
   - In one session an agent could not reach the live site through the network policy and began to describe it from memory. The repository on disk was byte-identical to the live page the whole time.

**Taking over an existing repo:** do not migrate it to the layout in this guide. Add `records/`, a changelog and the checks in section 8 in place, and restructure only when the Owner asks.

**Starting a new repo:** build only what the current phase needs (section 1).

## 1. What to build, and when

Scaffolding for a ten-page site on day one buries a two-page site. Add things in this order:

| phase | add |
|---|---|
| Day one | `index.html`, `assets/css/site.css`, `assets/js/site.js` (may be empty), `assets/fonts/` with licenses, `404.html`, `CNAME`, `_config.yml`, `robots.txt`, `sitemap.xml`, `records/facts.md`, `records/HANDOFF.md`, `CHANGELOG.md`, `README.md` |
| First launch | favicon set, Open Graph image, `.well-known/security.txt`, schema.org JSON-LD, the HTML validation and link check in CI, a working contact path |
| First inbound lead | the form service wired and tested from the live domain, the privacy sentence next to the form, the capability statement PDF |
| Second page | a shared header and footer strategy (copy by hand or a build step), Playwright screenshots at three widths for layout changes |
| Growth | a static-site generator only when the page count makes hand-copied headers error-prone (usually past five pages) |

The full tree, once all phases are done:

```
site/
├── index.html                  # the one content page
├── 404.html
├── capability-statement.html   # print-styled source of the PDF
├── manifold-capability-statement.pdf   # generated, committed, linked from the page
├── CNAME                       # custom domain; GitHub Pages reads it. Never delete.
├── _config.yml                 # Jekyll: include .well-known, exclude records/, docs/, scripts/, *.md
├── robots.txt  sitemap.xml  favicon.svg  favicon.ico  apple-touch-icon.png
├── .well-known/security.txt    # RFC 9116; Contact and Expires are required
├── assets/
│   ├── css/site.css            # one stylesheet; tokens at the top
│   ├── css/capability-statement.css   # print layout for the one-pager
│   ├── js/site.js              # footer year, form handler; no framework
│   ├── fonts/*.woff2 + LICENSE # self-hosted, latin subset, variable where available
│   └── img/                    # generated SVGs, og.png; no stock photography
├── scripts/                    # generators: surface.py, og.html, icon.html, render.js
├── records/                    # facts.md, HANDOFF.md, decisions.md (see section 7)
├── docs/                       # this guide
├── .github/workflows/checks.yml  .github/dependabot.yml
├── CHANGELOG.md  README.md  CREDITS.md
└── .htmlvalidate.json
```

Layout rules:
- **One content page until there is a reason for two.** Government buyers and primes read a company site the way they read a capability statement: who, what, past performance, how to buy, contact. All of that fits on one scrolling page with anchors. A second content page earns its place only when it has a different reader (careers, a writing archive). The 404 page and the print page for the capability statement do not count.
- **Separate content, style and behavior.** Copy lives in HTML, style in the stylesheets, behavior in one script. Nothing is inline except the SVG sprite and the JSON-LD block, which also lets a meta Content-Security-Policy with `style-src 'self'` hold.
- **Copy rather than abstract.** A two-page site does not need a templating system. Copy the header and footer by hand and let the link checker catch drift. Add a generator only when the copying starts producing bugs.
- **Delete what you do not use. `[site]`**
  - An earlier version of this site shipped the template's `elements.html` and `generic.html`, full of lorem ipsum and "Untitled Inc", reachable at the production domain from May 2026 until this rebuild shipped. The template's `README.txt` and `LICENSE.txt` sat in the web root too.
  - After any template or theme is brought in, list every file it added and remove each one the site does not reference. A crawl of the live domain (section 8) should return exactly the pages you intend.

## 2. Environment and tooling

- **No build step by default.** A static site that is plain HTML can be served from the repository root, and GitHub Pages will do that from the default branch. Add a build step (and a `deploy.yml` workflow) only when something must be generated on every push.
- **Node for checks, Python for generators.** Node tooling (html-validate in CI; pa11y, Lighthouse and Playwright by hand) runs with `npx`, pinned by version in the command. Python with the standard library plus Pillow is enough for SVG and image generation.
- **Pin versions in the command line or lockfile**, never "latest". `npx html-validate@11`, `npx pa11y-ci@5`, `npx lighthouse@12`. If a `package.json` is added, commit its lockfile.
- **Playwright for rendering.** Screenshots at 390, 768 and 1440 px widths, the PDF render, and the OG image all come from Playwright's bundled Chromium. Do not install a second browser.
- **Secrets**: a static site should have none. The form service's public key is designed to be public (Web3Forms says so in its docs). Anything that must stay secret does not belong in a static site at all.
- **CI**: one GitHub Actions workflow on `pull_request` and pushes to `main`, actions pinned to full commit SHAs with the tag in a comment, a concurrency group with `cancel-in-progress: true`, and Dependabot watching `github-actions` weekly so the SHA pins get updated. Section 8 lists what it checks.

## 3. Configuration

A website's configuration is its design tokens and its metadata. Both live in exactly one place each.

- **Design tokens live at the top of `site.css`** as custom properties: colors, type families, the content width, the gutter, the section spacing. Nothing further down the file uses a raw hex value or a raw pixel width that a token already covers.
- **Metadata lives in the `<head>` of each page** and nowhere else: `<title>` under 70 characters, `<meta name="description">`, `<link rel="canonical">`, Open Graph tags with an absolute image URL, `theme-color`, the icon links, and one JSON-LD block of type `ProfessionalService` or `Organization`.
- **Facts are not configuration.** The phone number, email, legal name and address appear in several places (hero, company table, contact aside, footer, PDF, JSON-LD). They are copied by hand from `records/facts.md`, and a grep in CI confirms every copy matches (section 8).
- **New tokens default to the old look.** When you change a token, render the three screenshot widths before and after and look at them. A spacing token changed for one section moves every section.
- **One domain for everything.** The site domain, the email domain and the domain on the capability statement should be the same. This site serves from one domain while its email uses another, and that second domain sits on a hosting provider's "coming soon" page. Record the chosen domain and the fate of the others in `records/decisions.md`.

## 4. Content and assets

- **Copy is source code.** It lives in the HTML, it is reviewed in pull requests, and it follows section 14. There is no CMS and no separate copy deck to drift out of sync.
- **Claims need a source.** Every Claim on the site maps to a line in the claims register in `records/facts.md` that says where it came from (a contract number, a résumé, a SAM.gov record, the Owner's word on a dated line). A Claim with no line is removed, not softened.
- **Facts match SAM.gov word for word.** SBA tells contracting officers to use the Small Business Search for market research, and tells small businesses that the SAM profile "is like a résumé." A company name or NAICS list that differs between the site and SAM may keep you out of that search. Misrepresenting size or socioeconomic status is a federal offense under 15 U.S.C. 645(d). Until a Fact is confirmed, the site leaves it out. UEI and CAGE are public data, so "on request" reads as "not registered". `[site]`
  - An earlier draft of the company table was nearly populated with the four NAICS codes "typical for this kind of work." None had been checked against the registration. They were removed.
- **Technical claims get a technical review. `[site]`**
  - The earlier site described a delivered system as having "full IL4 / LDAP / SSL compliance." IL4 is a DoD cloud impact level; LDAP and SSL are protocols. A reader from a program office sees that sentence and discounts everything after it. The corrected sentence names an IL4-accredited GovCloud environment with LDAP integration and TLS on every connection.
  - Before any sentence that names a standard, protocol, impact level, accreditation or model goes of record, someone who has worked with that thing reads it.
- **No photographs of people who do not work here. `[site]`**
  - The earlier site's "Who we are" section carried a stock photo of two smiling men in blazers. A second image, of four executives at a conference table, had the lighting and hand geometry of a generated image. Neither depicted anyone at the company. Stock agencies accept generated images (Adobe Stock since December 2022, labeled by the contributor), and generated images may not be copyrightable at all.
  - People photos are of actual staff, taken for the site, with written consent recorded in `records/decisions.md`. Otherwise there are no people photos.
- **Prefer drawings generated from code over stock imagery.** A figure drawn by `scripts/surface.py` is authored by the company, carries no third-party license, scales without artifacts, is a few kilobytes, and can be regenerated. The hero of this site is one such drawing.
- **Image discipline.** Every raster image has `width` and `height` attributes (web.dev: this is how you avoid layout shift), is served at no more than twice its displayed size, and is AVIF or WebP with a JPEG fallback when photography is unavoidable. The one image above the fold carries `fetchpriority="high"` and is never lazy-loaded; everything below the fold carries `loading="lazy"`. `[site]`
  - The earlier site shipped nine JPEGs totalling about 8 MB, including a 6000 by 4000 pixel original displayed at 400 pixels wide. The rebuilt site, fonts included, is under 600 KB.
- **Fonts are self-hosted woff2, latin subset, variable where available**, with `font-display: swap` and at most two `<link rel="preload" as="font" crossorigin>` lines for the faces used above the fold. The license file sits beside the font files. Google Fonts served from Google's servers sends visitor IP addresses to Google; a Munich court (LG München I, 20 January 2022, Az. 3 O 17493/20) found that to breach GDPR without consent. Self-hosting is also faster. The Fontsource npm packages are the simplest source of properly subset files.
- **PDFs are generated, not hand-made.** The capability statement is an HTML page with print CSS, rendered to PDF by Playwright. The HTML is the source; the PDF is committed so the link works without a build. `[site]`
  - The first render of this site's one-page capability statement ran to two pages by a few pixels. "One page" is a requirement buyers state out loud. `scripts/render.js` fails unless the PDF's `/Count` is exactly 1, and CI checks the committed file the same way.

## 5. Provenance: every generated asset has a generator

Any file that a script produced is reproducible from the repository, or it is not committed.

- **`scripts/` holds the generators.** `surface.py` draws the SVGs; `og.html` and `icon.html` are the pages Playwright screenshots for the share image and the touch icon; the README gives the exact commands. A generated asset with no generator in `scripts/` is a bug.
- **Generated files are not edited by hand.** If the OG image needs a different headline, change `og.html` and re-render.
- **Record the toolchain** in the README: the Playwright version, the Chromium build, the Python and Pillow versions. PDF and screenshot output differ slightly between browser builds; a diff in CI that nobody can explain is usually this.
- **`CREDITS.md` names every third-party thing in the repo** with its license and source URL: each font family, any icon set, any photograph, the template if any part of it survives. When the last line of a template is removed, the credits line is removed in the same commit and the changelog says so (section 10).
- **Git history is the provenance for copy.** Commits that change a Claim say what changed and why in the body, so `git log -S "IL4"` answers "when did we start saying that, and on whose word."

## 6. Deploys, previews and rollbacks

- **Know your publishing source.** GitHub Pages publishes either from a branch (its root or its `/docs` folder) or from a GitHub Actions workflow using `actions/upload-pages-artifact` and `actions/deploy-pages`. GitHub recommends a workflow when you have a build step and the branch when you do not. Write which one applies in `records/HANDOFF.md`.
- **Branch publishing facts** (GitHub docs): Jekyll runs unless `.nojekyll` exists at the root. It skips files and folders that start with `_`, `.` or `#` (so `.well-known` needs an `include:` line in `_config.yml`), and it renders every Markdown file into a public HTML page unless `_config.yml` excludes it; a push from a workflow using `GITHUB_TOKEN` does not trigger a Pages build; sites may be no larger than 1 GB; soft limits are 100 GB of bandwidth a month and 10 builds an hour; a deployment that takes over 10 minutes times out.
- **What the host does and does not do.** Checked against this site's live headers: GitHub Pages sends `cache-control: max-age=600`, `server: GitHub.com`, and no `Strict-Transport-Security`, `Content-Security-Policy` or `X-Frame-Options`. It supports no custom headers, no server-side redirects beyond HTTP to HTTPS, between apex and www, and `/dir` to `/dir/`, and no `.htaccess`. Plan around that: a meta CSP in the HTML (section 9), meta-refresh stubs with a canonical link for moved URLs, and no feature that needs a header.
- **Previews.** A pull request that touches the stylesheet or the page structure gets three screenshots (390, 768, 1440 px), and the reviewer looks at them. Text-only changes are reviewed in the diff. `[site]`
  - The mobile view of this site's first render put a decorative figure above the headline. It looked fine at desktop width and was caught only because the phone-width screenshot was taken.
- **Deploys are commits to the default branch.** Nothing else. No FTP, no uploading through the GitHub web UI once CI exists, no editing on the server because there is no server.
- **Rollback is `git revert`.** Never force-push the publishing branch to roll back; revert the commit so the history shows what happened and the changelog can say so.
- **Tag launches.** An annotated tag such as `launch-2026-11` on the commit that went live. Semantic versioning does not apply to a website (there is no API to break); say so at the top of the changelog, as Keep a Changelog asks.
- **Who can deploy.** At least two humans hold write access to the repository and owner rights on the GitHub organization, and `records/HANDOFF.md` names them. `[site]`
  - This site's redesign sat unpushed for an afternoon because the organization that owns the repository had one owner account, and the person doing the work was logged in as a different account with read-only access. Access is checked at the start of a session, not at push time.

## 7. Records: changelog, handoff, facts and what goes public

These records let a maintainer with no memory of past work continue it correctly.

- **`CHANGELOG.md`** follows Keep a Changelog 1.1.0: newest first, an `Unreleased` section at the top, dated entries in ISO 8601, grouped under Added, Changed, Removed, Fixed and Security. Two local additions:
  - A **Claims** group for any entry that adds, changes or withdraws a Claim, with the source named.
  - A line stating the changelog does not follow Semantic Versioning and that launches are tagged by date.
- **`records/facts.md`** is the facts register: a table with Fact, value, source, checked-on date, and the list of places it appears, followed by the claims register. "Unconfirmed" is a legal value, and an unconfirmed Fact is not shown on the site. A Fact changes here first, then everywhere it appears, in one commit.
- **`records/HANDOFF.md`** holds live state under five headings: Publishing (source, domain, DNS provider, registrar, who has access), Check and fix (the commands), Open question, Traps, Last updated (from `date -u`). Update it whenever any of these change.
- **`records/decisions.md`** is append-only. Each entry has a date from the clock, who decided (the Owner, or you under the Owner's standing instructions), and one paragraph. Domain choices, the decision to carry no analytics, consent for a staff photo, the decision to withdraw a Claim: all go here.
- **Timestamps come from the clock**, in the same command that writes the entry:
  ```
  printf '\n## %s | %s\n' "$(date -u +%Y-%m-%d)" "<title>" >> records/decisions.md
  ```
- **What goes public.** This repository is public, and the site would be public even if the repository were private (GitHub docs). The decision taken: `records/` and `docs/` stay in the repository but `_config.yml` keeps them off the published site. So:
  - Everything in the repository is written as if a competitor and a contracting officer will read it. That is fine for a changelog and a facts register, which contain nothing a capability statement does not.
  - Review notes, draft Claims under discussion, customer names that cannot yet be published, anything about a prospective engagement, notes about the tooling used to build the site, and named people's account details never enter the repository. They live wherever the Owner keeps business records.

## 8. Quality gates

### Correctness of claims
- **Every Claim traces to a line in the records** (section 4). CI cannot check this; a human does, on every pull request that touches copy, using the diff and the facts register side by side.
- **Facts are consistent across the site.** The CI workflow fails if the email or phone number is missing from any page that should carry it. It does not read the register; when a Fact changes, grep for the old value by hand before committing.
- **Every interactive element works or does not exist. `[site]`**
  - The earlier site's contact form posted to `#`. A visitor who filled it in lost the message and received no error. Before a form goes of record, a test submission is sent from the live domain and received at the destination mailbox. Until the service is configured, the form falls back to a `mailto:` with the fields pre-filled and says so.

### Validity and links
- **html-validate** with `html-validate:recommended`, run on every HTML file in CI. It caught, on this site: a title over 70 characters, inline styles, an `autocomplete` attribute on a checkbox, and two `aside` landmarks without distinct names. Fix the markup rather than disabling rules. The one rule turned off, `tel-non-breaking`, is replaced by a `.nowrap` span because the non-breaking hyphen glyph is not in the font subsets.
- **lychee** on every HTML file in offline mode with `--root-dir` set to the workspace, so root-relative links resolve and the build fails on a broken internal link. After deploy, run it once by hand against the live domain, which also proves no template leftovers are reachable (section 1).

### Performance
- **Targets are the Core Web Vitals thresholds at the 75th percentile** (web.dev): LCP within 2.5 s, INP at or under 200 ms, CLS at or under 0.1. A static page with self-hosted fonts and one SVG passes these with room to spare; the budget exists so it stays that way.
- **The company's budget**, stated as a company number and not a standard: total transfer under 500 KB for the front page, JavaScript under 20 KB, zero third-party requests on page load. web.dev's own worked example uses 300 KB total and 125 KB of JavaScript; the HTTP Archive median mobile page is about 2 MB. Check it by hand with `npx lighthouse@12` at launch and after any design change; the November 2026 build measured 206 KB and scored 98 to 100 in every category. Lighthouse CI exists if the page count grows enough to need it.
- **Dependency budget. `[site]`** The earlier site loaded jQuery, a scroll plugin, a breakpoint library and all of Font Awesome (about 3 MB of assets) to open a menu and show two icons. A library is added only when the hand-written version would exceed the library in size or in bugs. The rebuilt site's script is about a hundred lines.

### Accessibility
- **Target WCAG 2.2 AA.** Section 508 binds federal agencies, not a contractor's own marketing site, but agencies look at a vendor's public site as evidence, and the 2017 refresh of Section 508 incorporates WCAG 2.0 AA, which 2.2 AA contains. Meeting it costs almost nothing on a static page.
- **The criteria that bite on a marketing site**, from the WCAG 2.2 text: contrast 4.5:1 for text and 3:1 for large text and UI components (1.4.3, 1.4.11); reflow at 320 CSS pixels without horizontal scrolling (1.4.10); text spacing overrides must not break layout (1.4.12); a skip link (2.4.1); visible focus (2.4.7) and focus not hidden behind a sticky header (2.4.11); pointer targets at least 24 by 24 CSS pixels unless inline in text (2.5.8); form fields with real `<label>` elements and errors described in text (3.3.1, 3.3.2); and `prefers-reduced-motion` honored for anything that moves.
- **Automated checks**: pa11y-ci with both the `axe` and `htmlcs` runners against every HTML file, and Lighthouse's accessibility category, run by hand at launch and after design changes. Deque's own figure is that axe finds about 57 percent of WCAG issues automatically, so a keyboard walk-through of every page (tab from top to bottom, submit the form, open any menu) is part of each launch checklist. On this site, pa11y found 113 contrast errors from one grey token before launch.

### Search and sharing
- Every page has a unique `<title>` and `description`, a canonical URL, and Open Graph tags with an absolute `og:image` of 1200 by 630 pixels. `robots.txt` names the sitemap. The JSON-LD validates in the Rich Results Test.
- After launch: verify the domain in Google Search Console with the DNS TXT record, submit the sitemap, import the property into Bing Webmaster Tools, and run the Facebook Sharing Debugger and LinkedIn Post Inspector once so their caches hold the new image.

### Cross-device review
- **Three screenshots for layout changes** (390, 768, 1440 px, full page), produced with Playwright. The reviewer reads them. Also check `document.documentElement.scrollWidth` against `clientWidth` at 320 and 375 px; this site overflowed at both until the email addresses were allowed to wrap. Playwright's `toHaveScreenshot` can turn the screenshots into a regression test once the design has settled.

### Writing review
- Every pull request that touches copy runs the pattern check in section 14 and gets a read-aloud by a human. The check is mechanical; the read is not.

The committed workflow, `.github/workflows/checks.yml`, runs on every pull request and on pushes to `main`: html-validate on the three pages, lychee in offline mode, the banned-punctuation and banned-word grep, the facts grep, a check that `security.txt` expires more than 60 days out, and a check that the committed PDF is one page. Actions are pinned to commit SHAs (resolved with `git ls-remote --tags` in November 2026) and Dependabot keeps them current.

## 9. Operating a live site safely

- **DNS for the apex domain** (GitHub docs): four A records, `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; optionally the four AAAA records; a `www` CNAME to `<org>.github.io` without the repository name. GitHub redirects between apex and www on its own. Never use a wildcard record; GitHub says it puts you "at an immediate risk of domain takeovers, even if you verify the domain." If CAA records exist, one must allow `letsencrypt.org`.
- **Order of operations when adding a domain**: verify the domain in the GitHub organization settings first, add it to the repository's Pages settings second, change DNS third. GitHub warns that doing DNS first "could result in someone else being able to host a site on one of your subdomains."
- **HTTPS**: once the DNS check passes, GitHub requests a Let's Encrypt certificate; then tick "Enforce HTTPS." The full domain name must be under 64 characters for the certificate to issue. Check `curl -sI https://<domain>/` after any DNS change.
- **Domain hygiene**: auto-renew on, a current payment card, registrar lock on (`clientTransferProhibited` in the RDAP record), WHOIS privacy on, and the renewal date in `records/HANDOFF.md`. A lapsed domain on a Pages site is a takeover waiting to happen.
- **Email authentication for the company's sending domain**: SPF, DKIM for each sending service, and DMARC starting at `p=none` with aggregate reports, moving to `p=quarantine` and then `p=reject` once reports are clean. A domain that never sends mail publishes `v=spf1 -all` and `p=reject`. The inbox the contact form delivers to is on this domain.
- **The form service is a data processor.** Name it next to the form, say what is sent (name, email, organization, message, and the visitor's IP address by way of the service), and link its privacy policy. Use the meta CSP's `form-action` to allow only that endpoint. Keep the plain email address visible as the fallback.
- **Security headers you can and cannot set.** Without server headers, a `<meta http-equiv="Content-Security-Policy">` can still restrict `default-src`, `script-src`, `img-src`, `connect-src` and `form-action` to `'self'` plus the form endpoint. It cannot set `frame-ancestors`, `report-uri` or `sandbox` (MDN and OWASP: these are ignored in meta), cannot set HSTS, and `X-Frame-Options` has no effect in meta. If clickjacking protection or HSTS ever matters, put a CDN that sets headers in front of Pages. Any third-party script that cannot be avoided carries a Subresource Integrity hash and `crossorigin="anonymous"`.
- **`security.txt`** at `/.well-known/security.txt` per RFC 9116, with `Contact:` and `Expires:` (required; the RFC recommends under a year), `Canonical:` and `Preferred-Languages:`. A CI step warns when `Expires` is within 60 days.
- **No cookies, no analytics, no consent banner** is the default, and it is written in the footer so visitors and reviewers can see it. If analytics are ever added, choose a cookieless service (Plausible, GoatCounter, Fathom), add it to the CSP, add it to the privacy sentence, and record the decision. GitHub logs visitor IP addresses for its own security purposes regardless; the privacy sentence can say so.
- **Uptime**: one external monitor on the production URL at a five-minute interval (UptimeRobot's or Better Stack's free tier suffices), alerting to a mailbox that someone reads.
- **Incident response for a defaced or hijacked site**, in order: from a trusted device, change the GitHub password and revoke all tokens, OAuth grants and SSH keys for every account with write access; read the account security log and the repository's deployment history to find the entry point; restore with a new commit that brings the tree back to the last launch tag (`git revert`, or `git checkout launch-2026-11 -- .` and commit), and force-push only if the history itself is compromised, with the Owner's approval; then re-enable branch protection; rotate the registrar password and two-factor, confirm registrar lock and every DNS record against the list above, and confirm the domain is still verified in GitHub; rotate the form service key and re-scrape the Open Graph caches; write the incident under `Security` in the changelog.
- **Kill nothing you have not looked at.** A Pages site has no processes to kill, but it has DNS records, deploy keys and collaborators. Before removing any of them, list it and state the reason in the command description.

## 10. Other people's work: templates, fonts, images, services

- **Templates.** HTML5 UP templates are CC BY 3.0: free for commercial use provided the design is credited. The credit obligation attaches to the design, markup and CSS. If a rebuild shares no template code or design, the credit may go, and the changelog entry for that commit says the last template file was removed on that date. Until then, the credit stays. `[site]`
  - The earlier site credited the template in the footer, correctly. The rebuilt site shares nothing with it, and the credit was removed in the same commit that removed the last template file.
- **Fonts.** SIL Open Font License 1.1: fonts may be bundled and redistributed with the site, must not be sold alone, and a modified or subset font must not use the Reserved Font Name. Keep each family's license file in `assets/fonts/`. Fontsource packages ship the license; copy it.
- **Icons.** Font Awesome Free is CC BY 4.0 for icons, OFL for the font files and MIT for the code, with attribution required and embedded in the files. If you need two icons, draw two SVGs instead and own them.
- **Photographs.** The Unsplash License allows free commercial use without attribution but forbids compiling photos into a competing service and selling unmodified copies. Keep a local copy and a line in `CREDITS.md` with the photographer and URL anyway; licenses change (Unsplash moved from CC0 in 2017, added restrictions in 2018, and launched a paid tier in 2022). See section 4 for why photographs of people are avoided entirely.
- **Agency seals and names.** Federal seals and insignia are protected by statute: 18 U.S.C. 701 for agency insignia, 18 U.S.C. 713 for the Great Seal and the presidential and congressional seals, 50 U.S.C. 3513 for the CIA, 50 U.S.C. 3613 for the NSA, and 10 U.S.C. 425 for the NGA, NRO and DIA. The DoD Joint Ethics Regulation bars stated or implied endorsement by DoD or its employees. Do not display agency seals, quote officials, or phrase past work in a way that implies the agency recommends you. "A Navy University Affiliated Research Center" is fine; a Navy seal is not.
- **Clearances.** Under 32 CFR 117.9, a contractor "will not use its favorable entity eligibility determination for advertising or promotional purposes." DCSA guidance allows a job posting to state the clearance a position requires. Saying that principals hold a personnel clearance level is common practice; advertising a facility clearance as a selling point is not, and naming classified programs or customers is never acceptable. Everything on the site is unclassified by default, and the site says so where it invites contact.
- **Form and other services.** Pin the service by name and plan in `records/HANDOFF.md`, record its free-tier limits (Web3Forms: 250 submissions a month; Formspree: 50), and note what it retains. A service that goes away takes the form with it; the `mailto:` fallback in the script exists for that day.
- **Vendored code.** If any third-party JavaScript or CSS is copied into the repo, it goes under `assets/vendor/<name>/` with an `UPSTREAM` file giving the URL, version, date and license, and `CREDITS.md` lists it.

## 11. Commits and authorship

- **No names of staff in code, comments, configs, docs or commit messages.** Author and copyright fields (the footer copyright line, the capability statement's point of contact, bios on the page) are filled only with text the Owner supplies. Use neutral phrasing in commits: "Owner decision", "correction (date):".
- **No tooling attribution in commits or pull requests.** Remove `Co-authored-by` trailers and session links that tools add by default unless the Owner has asked in writing for them.
- **Commit as the account that holds write access.** Set `user.name` and `user.email` to the person the Owner names, using that person's GitHub noreply address rather than an employer's or a university's domain, which can identify a customer by association. GitHub links a commit to a profile only through an email verified on that account.
- **Verified badges.** GitHub shows "Verified" only on signed commits; unsigned commits show no badge and nothing else. Whether to sign is the Owner's call.
- **Commit messages** use the imperative mood, say what changed and why, and cover one logical change each. A small set of prefixes (`content:`, `design:`, `fix:`, `chore:`, `docs:`) keeps `git log` readable; the full Conventional Commits machinery for version bumps is overhead on a site with no versions.
- **Do not rewrite pushed history.** Other clones, the Pages deployment record and links in the changelog depend on it. If something sensitive was pushed, tell the Owner and let them decide.
- **Before pushing, grep for private content:**
  ```
  git grep -nE '/home/[a-z]+/|REVIEW|VERDICT|TODO: ask|DRAFT' -- . ':!CHANGELOG.md' ':!docs/'
  git ls-files records/
  ```
  Logs and screenshots copied from a development machine carry home paths. Scrub them before committing, not after a push.

## 12. README and documentation

- **The README has a fixed structure:**
  1. Overview (two lines: what the site is, where it is served)
  2. Files (a table of every top-level path and what it is)
  3. Editing copy (where it lives, the house style in two sentences, the list of places a Fact appears)
  4. Contact form (which service, how to turn it on, what the fallback does)
  5. Re-rendering generated assets (exact commands for the PDF, OG image, icons and drawings)
  6. Facts still to fill in (the "On request" list, so the gap is visible to the next person)
  7. DNS and HTTPS (the records and the settings, in one paragraph)
  8. License and credits (pointer to `LICENSE` and `CREDITS.md`)
- **The README is for the next maintainer, not for visitors.** Marketing copy goes on the site. Process rules go in `docs/` (this guide). Business context goes in `records/`.
- **Keep the README true.** It is checked in every pull request that changes a path it names. A README that lists a file that no longer exists is worse than none.
- **Update the changelog as soon as a change is of record.** A change left out of the changelog gets forgotten or described wrongly later.

## 13. Launch

A launch is the first time a page, a PDF or a Claim goes of record at the production domain, and any later change that touches a Fact or a Claim.

- **The launch gate.** Nothing goes of record until the Owner says so. The gate:
  - the CI checks pass, and Lighthouse and pa11y have been run by hand;
  - the three screenshots and the PDF have been looked at by a human;
  - every Claim in the diff traces to a line in the records, and every Fact matches `records/facts.md`;
  - a test submission through the live form has arrived;
  - a crawl of the production domain after deploy returns only the pages intended (section 1).
- **Post-launch, same day**: `dig <domain> +noall +answer -t A` shows the four GitHub addresses; `curl -sI` shows a 200 with a valid certificate, `/.well-known/security.txt` returns 200, `/records/HANDOFF.html` returns 404, and `/does-not-exist` returns a real 404; Search Console and Bing have the sitemap; the share debuggers show the new OG image; the uptime monitor is green; the launch is tagged and the changelog has a dated entry.
- **Old URLs stay alive.** If any URL that was ever of record goes away, a stub with `<meta http-equiv="refresh">` and a `<link rel="canonical">` to the new location takes its place, because the host offers no server-side redirects.
- **Name collisions.** Before launch, search the company name with the industry's keywords and record in `records/decisions.md` which other firms share it. A consultancy in the same region with a near-identical name and overlapping services exists for this company; the site's metadata and first sentence are written so a searcher can tell them apart.

## 14. Writing

The banned list applies to everything written in the repo, the site, the PDF, commits and the changelog. The sentence and paragraph limits apply to site copy and the PDF; repository documents follow them where they can. Quotations used as evidence are exempt. `[site]`

The earlier version of this site read, in its own words: "Manifold blends cutting-edge understanding with a decade of IC acquisition execution — helping sponsors make faster, better decisions on AI/ML investments and deploy them to mission at scale." and "No benches, no hand-offs. Every engagement is delivered personally by a founding Principal. We're the same people who briefed your senior leadership, shaped your acquisitions, and published the research — not a logo with a staffing model." Most of the patterns below appear in those two passages. The one paragraph on that site that read as written by a person was the specific one, about a Bedrock system at a Navy UARC. That is the register to extend.

- **Banned punctuation:** no em dashes, en dashes or long hyphens. Use commas, periods or parentheses. Wikipedia's editors list spaced em dashes among the historical signs of machine writing; whether or not that stays true, a sentence that needs one usually needs splitting.
- **Banned constructions:**
  - "Not X, but Y" and "not just X, but also Y", unless X is a claim someone actually made earlier in the text. Also the fragment form: "No X. No Y. Just Z."
  - "Whether you're A, B, or C" and other audience tricolons.
  - Trailing explanations of why something matters: "..., helping sponsors make better decisions", "..., ensuring compliance".
  - Headlines built as balanced antitheses: "Research-grade depth, production delivery."
  - Sets of three balanced clauses. Break a list of three into two or four, or into a sentence.
- **Banned words**, from the 18F content guide, plainlanguage.gov and the Wikipedia list, plus this company's own: cutting-edge, full-spectrum, seamless, leverage, robust, holistic, comprehensive, mission-critical, at scale, best-in-class, tailored, innovative, empower, unlock, streamline, transform, utilize, facilitate, impactful, thought leader, delve, landscape (abstract), testament, pivotal, crucial, underscore (verb), showcase, boasts, "serves as", "stands as", moreover, furthermore, "it is important to note", "in conclusion".
- **Write what only this company can write.** Lead with nouns a buyer can verify: the agency type, the program phase, the named system, the standard, the impact level, the model family, the cloud region, the number of years. "Built a retrieval-augmented generation system on Amazon Bedrock for a Navy UARC, in an IL4 GovCloud environment, with LDAP and TLS" beats "production CUI GenAI." If a sentence could appear on any consultancy's site, replace it with a fact or delete it.
- **Numbers over adjectives.** Years, counts, dollar ranges, dates. Where the exact figure is sensitive, give a range or a rounded figure and say it is rounded ("about ten years").
- **Plain verbs and "is" and "has".** Wrote, built, sized, evaluated, briefed, trained, shipped. Allow "is" and "has". Cut "deliver" as the verb for everything.
- **First person plural.** "We" is the company; "you" is the reader. plainlanguage.gov: "More than any other single technique, using 'you' pulls users into the information."
- **Admit scope limits.** "Manifold has no bench." "Some of this work predates the firm." "Classified discussion happens only under a sponsoring contract." Buyers need these to decide quickly, and no template contains them. One or two per page; a page made entirely of what the firm is not reads as defensive.
- **Take a position once.** One sentence of opinion on the page, such as "Sometimes the answer is not to build it."
- **Mechanics.** Sentence case for headings, no trailing colons on headings, acronyms spelled out on first use unless the audience uses them daily (IC, DoD, RFP, SOW, TS/SCI, GPU and the like need no expansion here), "U.S." not "US", "federal" lowercase, sentences under about 25 words (GOV.UK's limit), paragraphs under about 100 words on the web (plainlanguage.gov, citing Nielsen Norman Group: readers take in about 18 percent of a page).
- **Rhythm.** Vary sentence length. A one-line sentence after a long one is fine. Three of the same length in a row is not.
- **Endings.** No closing paragraph that restates the page. The page ends when the content does.
- **The check.** CI greps the three HTML files for the banned list and for em and en dashes, in literal and entity form, and fails on a hit. Then someone reads the changed copy aloud.

## 15. Checklists

**Before opening a pull request that changes copy**
- [ ] Every new or changed Claim has a line in `records/facts.md` or `records/claims.md` with a source.
- [ ] Every Fact appears identically in all its places (hero, table, aside, footer, PDF, JSON-LD).
- [ ] The banned-pattern grep passes and the copy has been read aloud.
- [ ] Technical terms were reviewed by someone who has used the thing named.
- [ ] Three screenshots are attached and have been looked at.

**Before the pull request merges**
- [ ] The CI checks pass.
- [ ] No new third-party request; total transfer still under budget.
- [ ] Any generated asset was re-rendered from its generator, not edited.
- [ ] `CHANGELOG.md` has an entry under `Unreleased`.
- [ ] No names of staff, no AI attribution, no home paths in the diff or the commit message.

**Before a launch**
- [ ] The Owner has approved.
- [ ] A test form submission arrived at the destination mailbox from the live domain.
- [ ] The PDF is one page, dated, and matches the site's Facts.
- [ ] `security.txt` expiry is more than 60 days out.
- [ ] DNS, certificate, 404 page, `security.txt` and the www-to-apex redirect checked with `dig` and `curl`.
- [ ] Crawl of the live domain returns only intended URLs.
- [ ] Launch tagged; changelog entry dated; Search Console sitemap submitted; share caches refreshed.

**Every year, at SAM renewal**
- [ ] Re-check every Fact against SAM.gov and update the checked-on date.
- [ ] Renew `security.txt` `Expires`.
- [ ] Confirm domain auto-renew, registrar lock and DMARC reports.
- [ ] Run the live crawl, Lighthouse and pa11y against production.
- [ ] Read the page as a stranger and delete anything that has gone stale.

---

## Sources

Hosting and deployment:
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- Custom workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- Jekyll processing: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll
- Custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- Domain verification: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- 404 pages: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site
- Troubleshooting domains (CAA, CNAME overwrite): https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages
- Actions hardening (pin to SHA): https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- Actions concurrency: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/control-the-concurrency-of-workflows-and-jobs
- Dependabot for actions: https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot
- Protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- Commit signature verification: https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
- Co-authored-by trailers: https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors
- Revoking credentials: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/revoking-your-credentials

Performance:
- Core Web Vitals: https://web.dev/articles/vitals
- LCP, INP, CLS: https://web.dev/articles/lcp , https://web.dev/articles/inp , https://web.dev/articles/cls
- Performance budgets: https://web.dev/articles/performance-budgets-101 , https://web.dev/articles/use-lighthouse-for-performance-budgets
- Lighthouse: https://github.com/GoogleChrome/lighthouse
- Font best practices: https://web.dev/articles/font-best-practices , https://web.dev/articles/optimize-webfont-loading
- Image formats and responsive images: https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Image_types , https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
- Fetch priority and lazy loading: https://web.dev/articles/fetch-priority , https://web.dev/articles/browser-level-image-lazy-loading
- Fontsource: https://github.com/fontsource/fontsource

Accessibility:
- WCAG 2.2: https://www.w3.org/TR/WCAG22/ and quick reference https://www.w3.org/WAI/WCAG22/quickref/
- prefers-reduced-motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- axe-core: https://github.com/dequelabs/axe-core
- pa11y-ci: https://github.com/pa11y/pa11y-ci
- Section 508 laws and policies: https://www.section508.gov/manage/laws-and-policies/
- W3C policy summary for the United States: https://www.w3.org/WAI/Policy/policy/united-states

Testing:
- html-validate: https://html-validate.org/
- Nu HTML Checker: https://github.com/validator/validator
- lychee: https://lychee.cli.rs/ and https://github.com/lycheeverse/lychee-action
- Playwright snapshots: https://playwright.dev/docs/test-snapshots

Security and privacy:
- CSP (meta limitations): https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP , https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
- X-Frame-Options: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
- Subresource Integrity: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
- Third-party JavaScript: https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Javascript_Management_Cheat_Sheet.html
- RFC 9116 security.txt: https://www.rfc-editor.org/rfc/rfc9116.txt and https://securitytxt.org/
- Google Fonts and GDPR (Munich, 2022): https://en.wikipedia.org/wiki/Google_Fonts
- DMARC: https://en.wikipedia.org/wiki/DMARC
- Let's Encrypt CAA: https://letsencrypt.org/docs/caa/

Content and claims:
- 18F Content Guide: https://guides.18f.gov/content-guide/ (source: https://github.com/18F/guides)
- Federal plain language guidelines: https://www.plainlanguage.gov/guidelines/
- GOV.UK clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- SBA contracting guide: https://www.sba.gov/federal-contracting/contracting-guide/basic-requirements , https://www.sba.gov/federal-contracting/contracting-guide/how-win-contracts
- SBA for contracting officials (Small Business Search): https://www.sba.gov/partners/contracting-officials/small-business-procurement
- Small business misrepresentation: 15 U.S.C. 645(d) https://uscode.house.gov/ and 13 CFR 121.108 https://www.law.cornell.edu/cfr/text/13/121.108
- FAR 9.104-1 responsibility standards: https://www.acquisition.gov/far/9.104-1
- FTC advertising substantiation policy: https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation
- Joint Ethics Regulation (DoD 5500.07-R): https://dodsoco.ogc.osd.mil/
- Federal seals and insignia: 18 U.S.C. 701 https://www.law.cornell.edu/uscode/text/18/701 ; 50 U.S.C. 3513 ; 50 U.S.C. 3613 ; 10 U.S.C. 425
- NISPOM, 32 CFR 117.9 (advertising of facility clearance): https://www.ecfr.gov/current/title-32/part-117/section-117.9
- Capability statement format: https://www.same.org/wp-content/uploads/2026/06/2026-SAME-Missouri-River-JETS-APEX-Accelerator-Presented-by-Veronica-Doga.pdf , https://nhsbdc.org/sites/default/files/media/2024-11/capabilities-statement-2024.pdf

Licensing:
- HTML5 UP license: https://html5up.net/license
- SIL Open Font License 1.1: https://openfontlicense.org/open-font-license-official-text/
- Google Fonts licensing: https://github.com/google/fonts
- Font Awesome Free license: https://github.com/FortAwesome/Font-Awesome/blob/6.x/LICENSE.txt
- Unsplash License history: https://en.wikipedia.org/wiki/Unsplash
- Adobe Stock generative AI policy: https://helpx.adobe.com/stock/contributor/help/generative-ai-content.html

Process:
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- Conventional Commits 1.0.0: https://www.conventionalcommits.org/en/v1.0.0/
- Google Search Central, sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/ ; LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/
