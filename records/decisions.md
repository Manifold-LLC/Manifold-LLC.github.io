# Decisions

Append-only. Each entry: date from the clock, who decided, one paragraph. Entries marked "pending Owner confirmation" were made by the maintainer and stand until the Owner confirms or strikes them.

## 2026-11-08 | Replace the template with a hand-built page
Owner request: make the site better and less generic. The HTML5 UP template, its stock photographs and its copy were replaced with a single hand-written page, self-hosted fonts and a drawing generated from code. No photography of people is used because none depicts staff.

## 2026-11-08 | No cookies, no analytics, no third-party scripts on page load
Maintainer decision, pending Owner confirmation. The footer states it. The contact form, once keyed, delivers through Web3Forms; the form's fine print says so. Revisit only if the Owner asks for traffic data, and then choose a cookieless service.

## 2026-11-08 | Unconfirmed company data is left off the site
Maintainer decision, pending Owner confirmation. UEI, CAGE and NAICS codes were not available to the maintainer and are not shown. They are public SAM.gov data, so "on request" would read as "not registered"; the rows will be added when the Owner supplies them.

## 2026-11-08 | Past work is attributed to the principals, not the firm
Maintainer decision, pending Owner confirmation. Some referenced work predates the firm. The site says so, uses "our principals" rather than "we" for that work, and names Google and NVIDIA once as vendor engineering teams worked alongside rather than as partners.

## 2026-11-08 | Standardize on manifold-llc.com; email to move
Owner decision. The site stays at manifold-llc.com and email will move to info@manifold-llc.com once the mailbox exists. Until then every address on the site and PDF stays info@teammanifold.com. When the mailbox is live, change `records/facts.md` first, then every listed location, then re-render the PDF.

## 2026-11-08 | Commit author email stays as is
Owner decision. The maintainer's commit address is a personal address, and the Owner chose not to rewrite the branch history.

## 2026-11-08 | Independence sentence confirmed
Owner confirmed: the firm does not compete for work it helped specify and takes no referral or reseller fees. The sentence is on the page under How we work and in the capability statement.

## 2026-11-08 | Bios drawn from résumés, with sponsor and program detail left out
Maintainer decision under the Owner's instruction to put names, roles and two-line bios on the page. The résumés name a sponsor agency, program codenames, a contract vehicle and funding figures. None of that appears on the site; employers, titles, degrees and the kind of work do. The Owner should confirm that naming current employers is allowed.

## 2026-11-08 | Adopt the existing brand symbol as the site mark
Maintainer decision. The Owner's Drive holds a designed symbol (a calligraphic M drawn as a wave). It replaces the wire-grid mark in the header, footer, favicon, touch icon, share image and PDF. The wire-grid drawing stays as the hero figure.

## 2026-11-08 | Company data published from primary records
Maintainer decision under the Owner's instruction to add the SAM codes. UEI and CAGE come from the SAM.gov activation email, the formation date from the Virginia SCC acknowledgement, the county from the registered address, NAICS from the July 2026 capability statement, and the facility-clearance posture ("performed on customer premises") from the same document. The registered street address is a principal's home and is not published.

## 2026-11-08 | Development is in scope; advise or build, never both for one organization
Owner decision: the site need not be limited to consulting. The headline now reads "advice and engineering", a fifth capability covers applied research and development, and the conflict-of-interest item states the rule. Two research projects supplied by the Owner are described under Selected work within the limits their write-ups allow.

## 2026-11-08 | Research described without numbers; the paper under review mentioned only generically
Owner decision: publish no numbers from the three research projects; describe the dark-vessel and SAR work freely otherwise; mention the trajectory model without specifics. Applied to the page, the PDF, the facts register and the skills inventory. The trajectory model has one generic case note with no name, venue, numbers or architecture detail.

## 2026-11-08 | Capability statement becomes two pages
Maintainer decision. With five competencies, five experience entries and two bios, one page would have needed type under 8 points. Page one stands alone (competencies, differentiators, company data, contact); page two carries experience and principals. CI now checks for exactly two pages.

## 2026-11-08 | No phone number on the site
Owner decision. Email is the only published contact channel. The number removed from the page, the PDF, the structured data and the CI check.

## 2026-11-08 | Sponsor agency stays unnamed; employers generic for now; FastSAR linked
Owner decisions. The public site keeps "an Intelligence Community agency" rather than naming the sponsor. Current employers are described generically until the Owner confirms outside-activity rules. FastSAR is linked to its GitHub repository, PyPI package and arXiv preprint, and described as submitted to IEEE TGRS. Counts in the bios stay.

## 2026-11-08 | Dollar figures only when loosely rounded
Owner rule. No exact dollar figures anywhere public; rounded magnitudes such as "over two hundred million" are allowed. Applied to Paul's bio: program funding "over ten million dollars a year" and a follow-on contract ceiling "above two hundred million dollars". Research results stay number-free.

## 2026-11-08 | Employers named; email moved to info@manifold-llc.com
Owner decisions. Naming Penn State ARL and SAIC in the bios is fine, so the names are restored. The mailbox info@manifold-llc.com exists, so every published address moved to it (page, PDF, 404, security.txt, form fallback, JSON-LD, CI check). The feature branch is to be deleted once its last changes are merged.

## 2026-11-08 | Published address precedes the mailbox
Owner decision. info@manifold-llc.com stays on the site while the Owner adds manifold-llc.com as a Workspace domain alias. The maintainer had switched the address on a misread of "exists"; the Owner chose to keep it rather than revert.

## 2026-11-08 | Contact form delivery through Web3Forms
Owner set up the account under info@manifold-llc.com on the free plan and supplied the public access key. The key is in the page by design; the service's own docs say so.

## 2026-11-08 | Commits are authored by the Owner's named person with no tooling trailers
Owner instruction.

## 2026-11-08 | Founder-centric wording removed so the site survives hiring
Owner decision: the firm intends to grow, so the page and PDF no longer say that the two founding principals do all the work. Operational claims now read "senior practitioners", "everyone at the firm", "the practitioner who scopes an engagement does the work". The founders are still named in the Principals block, the JSON-LD and the PDF, and past work is still attributed to them ("led by the people who founded Manifold"). The clearance line now says "everyone at the firm"; change it the day someone uncleared joins.

## 2026-11-08 | Review fixes applied
Owner instruction to fix the adversarial review findings. The town in Luke's bio became "Northern Virginia" so the unnamed sponsor cannot be inferred. "No conflicts of interest" gained the sentence that the firm does not pursue work at an organization where a member serves as a trusted agent or evaluator; the Owner should strike it if it is not a commitment the firm will keep. The approach section now says the founders also hold positions at Penn State ARL and SAIC. The capabilities intro now says the delivery half of Secure generative AI is building. The share image was regenerated with the current headline. The capability statement now carries Past performance on page one, Research and Principals on page two, a Contract vehicles row, live links, and Author metadata set by `scripts/pdf-metadata.py`. A case-note index was added at the top of Selected work. The FastSAR magnitudes ("orders of magnitude", "in seconds", "a fraction of a cent") were kept as loosely rounded under the Owner's dollar rule.

## 2026-11-09 | A one-page overview alongside the capability statement
Owner asked whether the capability statement was also the slick sheet and chose to have one built. The overview is a separate one-page PDF for capture teams and conference tables; the capability statement stays the plain federal document. On the Owner's instruction the overview is centred on the advisory and SETA role (strategy, acquisition support, compute and cost, assessment, secure generative AI, training) with an acquisition-cycle diagram, and the research projects are left to the site and the capability statement. The foundation-model credential is stated generally, as the Owner asked: inventor and lead of several advanced foundation models developed for the U.S. government. Graphics are generated (the manifold drawing, the diagram, a QR code). Same wording rules as the site: no research numbers, no sponsor name.

## 2026-11-09 | Opening rewritten in the Intelligence Community's own terms
Owner decision, prompted by a colleague's note that the opening read generically. The headline now leads with Intelligence Community program offices and "people who have sat on the government's side of the table"; the lead names trusted agents, SETA engineers, source-selection and BAA panels, the front office and the high side. The same opening is on the share image, the overview and the capability statement, shortened where space required. Insider terms that would imply a facility clearance (ICD 503, SCIF, SAP) are deliberately absent. The hero headline size was reduced to fit the longer line.
