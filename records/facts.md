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
| Independence | "Independent AI/ML advice" in the headline; "No conflicts of interest" under How we work | Owner confirmed 2026-11-08: the firm does not compete for work it helped specify and takes no referral or reseller fees. | 2026-11-08 |
