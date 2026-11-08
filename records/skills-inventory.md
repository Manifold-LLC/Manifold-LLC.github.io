# Skills and experience inventory

Drawn from three project write-ups the Owner supplied on 2026-11-08: a radar image-formation paper (FastSAR, two named authors), a research brief on re-finding dark vessels across satellite passes (unpublished draft, with its own list of what may be published), and a vessel-trajectory foundation-model paper under anonymous conference review. Nothing identifying from the third appears in this repository or on the site until its review ends; its skills are listed generically.

Use this when writing capability statements, proposals or bios. Items marked "site" already appear on the page.

## Machine learning and foundation models
- Pretraining domain foundation models from raw operational data at the tens-of-billions-of-tokens scale, with a trunk-and-heads design so one frozen model serves several analyst tasks (classification, destination, arrival time, activity detection). Generic on the site.
- Compute-optimal scaling studies (IsoFLOP sweeps, power-law fits for model size and token count), used to decide how large the next model should be. Site, generically.
- Custom architectures for geospatial sequences: position encodings at multiple scales, time-indexed rotary embeddings, density-over-a-canvas output heads, calibrated probabilistic forecasts rather than point estimates.
- Self-supervised and bootstrapped training for remote-sensing detectors, including training from AIS positions and a control (the "empty berth" test) that proves a detector finds ships rather than the places ships usually sit. Site.
- Per-detection attribute models: heading and speed from Sentinel-2 band delay and wake, heading and speed from Sentinel-1, length, learned identity embeddings. Site.
- Finding and documenting a training-data leak (chip size encoding speed and length) and retraining on fixed windows. Worth citing in any methodology discussion.

## Multi-sensor fusion and tracking
- Multi-target tracking over anonymous detections from five sensors with different revisit rates and clutter, global assignment per pass, stationary and moving hypotheses, and an explicit "not found" outcome. Site.
- Empirical motion models learned from a year of AIS (about four million displacement samples per horizon), cutting a 12-hour search area from about 62,600 to about 870 square kilometers. Site.
- Evaluation protocol design with withheld ground truth, recall-versus-search-area curves, candidate-list metrics, and thirteen clearly reported negative results. Site.

## Radar and remote sensing
- SAR image formation: exact and factorized backprojection, polar format, autofocus; readers for CPHD, SICD, Sentinel-1 and NISAR; stripmap and sliding-spotlight mosaics; image-quality grading for interferometric and radiometric use. Site.
- Commercial SAR data handling (Umbra, Capella) and public missions (Sentinel-1, Sentinel-2, Landsat 8/9, NISAR, VIIRS). Site.
- Early use of NISAR L-band data for ship detection. Site.

## High-performance and cloud computing
- Kernel engineering in C++ with OpenMP, CUDA, and JAX Pallas for TPUs; mixed and reduced precision (float64, float32, float16, bfloat16, split-precision matrix products) with measured accuracy cost. Site.
- Roofline-level performance analysis: each stage within 40 to 100 percent of its hardware limit. 
- Matched-hardware benchmarking and cost-per-result on on-demand cloud instances (NVIDIA L4, A100, H100; TPU v5e, v6e; CPU), including energy per result. Directly supports the site's cluster-sizing and cost-modeling claims. Site.
- Large-scale data engineering: about one million radar chips, 2.9 million optical chips, seven years of nightly VIIRS detections, nine years of AIS, over 200 GB of derived data. Site.

## Research practice and communication
- Papers written to journal and conference standard (IEEE TGRS, a top machine-learning conference), with reproducible protocols, open data choices, and released or planned-release code.
- Benchmarking that retrains published baselines on the same data and scores purpose-built models against frozen probes.
- Honest reporting: calling a 10 to 17 percent result a first baseline rather than a solution; publishing what did not work.

## Domain knowledge
- Maritime domain awareness: AIS and its gaps, dark vessels, illegal fishing, sanctions evasion, Danish and Norwegian AIS archives, Global Fishing Watch and Skylight as reference systems.
- Space-based remote sensing economics: fleet growth, revisit, resolution, and why more looks per day beats a smarter tracker.

## Open items before any of this goes further on the site
- Whether the FastSAR code is public yet, and the paper's status (submitted, under review, accepted).
- Whether the dark-vessel paper's figures (map of footprints, recall-versus-search-area, a six-day track) may be used. The brief says to ask first.
- When the anonymous review of the trajectory model ends, so it can be named and linked.
