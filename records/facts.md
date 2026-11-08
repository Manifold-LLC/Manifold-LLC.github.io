# Facts register

Every company data point that appears on the site, its source, and when it was last checked. A fact changes here first, then in every place listed, in one commit. "Unconfirmed" is a legal value; a guess is not. Unconfirmed facts are not shown on the site.

| Fact | Value on site | Source | Checked | Appears in |
|---|---|---|---|---|
| Legal name | Manifold LLC, Virginia LLC formed March 2026 | Virginia SCC Articles of Organization acknowledgement, 2026-03-29 (company mailbox); SAM.gov record | 2026-11-08 | index.html (company table, footer, JSON-LD), capability-statement.html, 404.html |
| Location | Loudoun County, Virginia | SAM.gov registered address and Loudoun County business license (company mailbox). The street address is a principal's home and is not published. | 2026-11-08 | index.html (hero facts, company table, contact aside, footer), capability-statement.html, 404.html |
| Email | info@teammanifold.com | Earlier site copy; git author on all prior commits | 2026-11-08 | index.html (hero facts, company table, contact aside, footer, form fallback, JSON-LD), capability-statement.html, 404.html, .well-known/security.txt, assets/js/site.js |
| Phone | (703) 436-1308 | Earlier site copy. The July 2026 capability statement in Drive lists a different number; Owner to choose one. | 2026-11-08 | index.html (company table, contact aside, footer, JSON-LD), capability-statement.html |
| Size status | Small business | SAM.gov registration; July 2026 capability statement | 2026-11-08 | index.html, capability-statement.html |
| Socioeconomic status | not shown | unconfirmed; none claimed on the earlier site | 2026-11-08 | not shown |
| Clearances | TS/SCI with CI polygraph, both principals | Singerman CV; July 2026 capability statement in Drive ("Both Principals TS/SCI w/ CI Poly") | 2026-11-08 | index.html (hero facts, approach, company table), capability-statement.html |
| Facility clearance | None; classified work performed on customer premises | July 2026 capability statement ("Classified Work: Performed on customer premises"); no DCSA or FCL correspondence in the company mailbox | 2026-11-08 | index.html (approach, company table), capability-statement.html |
| UEI | C6P2G6PQLEB8 | SAM.gov activation email, 2026-08-21 (company mailbox) | 2026-11-08 | index.html (company table, JSON-LD), capability-statement.html |
| CAGE | 23X60 | SAM.gov activation email, 2026-08-21 | 2026-11-08 | index.html (company table, JSON-LD), capability-statement.html |
| NAICS | 541715, 541512, 541611, 541690 | July 2026 capability statement in Drive; Owner to confirm these match the SAM record | 2026-11-08 | index.html (company table), capability-statement.html |
| SAM renewal | 2027-08-10 | SAM.gov activation email | 2026-11-08 | records/HANDOFF.md |
| Founding date | March 2026 | Virginia SCC acknowledgement, 2026-03-29 | 2026-11-08 | index.html (company table, JSON-LD foundingDate), capability-statement.html |
| Principal names and bios | Paul G. Singerman, Ph.D. and John "Luke" Och, with short bios | Résumés supplied by the Owner on 2026-11-08 (Singerman CV, Och résumé Oct 2025) and the July 2026 capability statement. Bios use employer, title, degrees and the shape of the work; no sponsor names, program names, contract vehicles or dollar figures. The July 2026 capability statement names the sponsor agency throughout; the site does not, pending the Owner's decision. Owner to confirm that naming current employers is permitted under each employer's outside-activity rules. | 2026-11-08 | index.html (Principals block, JSON-LD founder), capability-statement.html (company data, point of contact) |
| Site domain | manifold-llc.com | `CNAME`; live site | 2026-11-08 | canonical and Open Graph URLs, sitemap, security.txt |

## Claims register

Claims that are not company data but that a reader could check. Each is worded on the site as the principals' experience unless the source supports more.

| Claim | Wording on site | Source | Checked |
|---|---|---|---|
| Navy UARC generative AI system | Principals designed and delivered a RAG system on Amazon Bedrock in an IL4 AWS GovCloud environment, integrated with the laboratory's directory service (LDAP), TLS on every connection; delivered to production | Earlier site copy ("Bedrock RAG system at a Navy UARC with full IL4 / LDAP / SSL compliance", "production CUI GenAI"); wording corrected 2026-11-08. Owner confirmed 2026-11-08 the note is fine as written. | 2026-11-08 |
| Geospatial foundation models | Principals served as architects, working directly with vendor engineering teams at Google and NVIDIA | Earlier site copy ("architecting geospatial foundation models in active collaboration with Google and NVIDIA"); no partnership implied. Owner confirmed 2026-11-08 the note is fine as written. | 2026-11-08 |
| IC acquisition experience | About ten years inside Intelligence Community acquisition offices and research programs, one principal as a trusted agent at a Navy UARC, the other as a SETA contractor | Owner, 2026-11-08 | 2026-11-08 |
| Principal-delivered, no bench | Every engagement delivered by a founding principal | Earlier site copy | 2026-11-08 |
| Typical engagement length | A few weeks to a few months | Maintainer wording, pending Owner confirmation | 2026-11-08 |
| Independence | "Independent AI/ML advice and engineering" in the headline; "No conflicts of interest" under How we work: advise or build, never both for one organization; no competing for work the firm helped specify; no vendor fees | Owner, 2026-11-08: development is in scope as long as the firm does not advise and build for the same organization; the no-compete and no-fee points confirmed earlier the same day. | 2026-11-08 |
| Dark-vessel tracking research | Five-sensor tracker over about 350,000 square kilometers; 70 to 86 percent of stationary and 10 to 17 percent of moving dark vessels re-found per week; true next sighting in the top five about half the time; thirteen tracker changes without gain; first public baseline; unpublished draft, 2026 | Research brief supplied by the Owner on 2026-11-08, section 7 of which lists what may be stated publicly. No funder, sponsor, data program, vessel name or position is published. | 2026-11-08 |
| FastSAR | SAR image formation on CPUs, GPUs and TPUs; 1.06 to 22,000 times faster than open-source implementations at equal or better accuracy; a 108-megapixel image in about three seconds on the lowest-priced cloud GPU; written with a co-author at Penn State ARL for IEEE TGRS | Paper draft supplied by the Owner on 2026-11-08 (authors named on it). Publication status and whether the code is public are unconfirmed; the site says "written for" the journal and does not say the code is available. | 2026-11-08 |
| Vessel-trajectory foundation model | Not on the site | Paper under anonymous conference review, marked do not distribute. Nothing identifying appears in this repository until the review ends. | 2026-11-08 |
