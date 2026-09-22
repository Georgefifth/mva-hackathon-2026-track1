# Track 1 Methods Report — MVA Hackathon 2026

**Team name:** Georgefifth
**Model:** `bub1b-compound-het-v1` (model 1 of 1)
**Submission file:** `georgefifth_bub1b-compound-het-v1.csv`

*Answers follow the official methods description template.*

---

## Method abstract (≤500 words)

We implemented a phenotype-directed, gene-panel-first variant prioritization pipeline for the single MVA proband. Because the phenotype (rhabdomyosarcoma + IUGR + parental recurrent miscarriages) strongly suggested autosomal-recessive MVA, we curated an 11-gene panel of published MVA/chromosome-instability genes (BUB1B, CEP57, TRIP13, CENATAC, MAD1L1, MAD2L1BP, CEP192, BUB1, BUB3, SMC5, SLF2) and extracted all variants within their GRCh38 gene bodies from the provided WGS VCF using pysam. Quality filtering used GQ≥20, DP≥10, alt-allele depth ≥3, and PASS-only filters. Every variant was annotated through the Ensembl VEP REST API (consequence, transcript, SIFT/PolyPhen, ClinVar co-location, gnomAD presence).

A key methodological observation: naive indel-length heuristics falsely flagged several intronic BUB1B indels as "frameshifts" — VEP annotation was essential to distinguish coding from non-coding calls. After annotation, BUB1B contained exactly one heterozygous stop-gain (p.Leu737*, ClinVar pathogenic, rs759242053) and one heterozygous missense (p.Asn1002Lys, SIFT 0.01 / PolyPhen 0.997, absent from population databases — ACMG PM2), constituting a textbook compound-heterozygous configuration matching the classic MVA pattern of one null allele + one hypomorphic allele. All other BUB1B calls and all other panel genes lacked biallelic coding impact. We further verified mechanistic plausibility: the PTC is NMD-eligible (exon 17/23, >10 kb upstream of the last exon junction), and the missense lies in the pseudokinase C-lobe adjacent to known unstable MVA variant L1012P.

**Strengths:** phenotype-driven search space reduction; annotation-verified consequence calls rather than heuristic indel classification; explicit compound-het detection; mechanism-level confirmation (NMD eligibility, domain mapping, dose-threshold literature). **Limitations:** no trio data — trans configuration inferred, not proven; the missense allele lacks a ClinVar entry and rests on in-silico + mechanistic evidence; panel-first design would miss a causal variant in a non-panel gene.

## Detailed answers

**1. Model/approach in detail.** Three-stage pipeline, all scripts in the linked repository (`pipeline/`). Stage 1 (`01_explore_vcf.py`): characterize the VCF — GRCh38 build, single sample, GATK-style INFO/FORMAT fields, no pre-existing functional annotation. Stage 2 (`02_mva_gene_search.py`): extract all records within gene-body regions of the 11-gene MVA panel; quality-filter; classify by genotype (het/hom-alt) and sequence ontology proxy. Stage 3 (`03_annotate_vep.py`): annotate every surviving variant with Ensembl VEP REST and rank consequences by severity (stop_gained/frameshift/splice > missense > synonymous > intronic). Candidate selection was then manual curation on the annotated table.

**2. Automated output vs. manual curation.** The submission file is the result of automated extraction, filtering, and annotation, followed by manual review of the small candidate list (≈40 annotated variants in low-count genes). The final EPCR ranking and the compound-het pairing were manually curated.

**3. Manual review.** We (a) confirmed both BUB1B variants sit on the MANE Select transcript ENST00000287598; (b) checked ClinVar co-location (Allele 1 = rs759242053, pathogenic; Allele 2 = novel); (c) verified the PTC's NMD eligibility from the Ensembl exon structure; (d) mapped the missense to the BUBR1 pseudokinase domain (UniProt O60566) adjacent to destabilizing MVA variant L1012P; (e) inspected allele balance (AD 21/25 and 15/13) — both consistent with true heterozygosity, not artifact.

**4. Data sources.** Only publicly available data were used beyond the provided case VCF: Ensembl VEP REST API (consequence annotation, SIFT/PolyPhen, gnomAD co-location), ClinVar significance via VEP co-located variants, UniProt domain annotations, and published MVA/BUBR1 literature (see References). No proprietary data.

**5. Compound-het capability.** The pipeline explicitly outputs compound-heterozygous candidates: it groups quality-passing heterozygous variants by gene and flags genes with ≥2 heterozygous coding-impact calls. The submitted row 1 is a two-variant compound-het pair; rows 2–3 submit each constituent variant singly for partial-credit coverage.

**6. Secondary/incidental findings.** None submitted; all non-BUB1B panel variants annotated as non-coding or biallelic-insufficient, and no high-impact incidental findings were flagged for return.

**7. Runtime and cost.** Full pipeline runs in minutes on a laptop (single-core, <1 GB RAM beyond the 300 MB VCF). Marginal cost ≈ $0; all resources used are public and free.

**8. LLM/AI use (required declaration).** Devin (Cognition AI), individual plan, default data-handling terms; Ensembl VEP REST API (EMBL-EBI). No protected genomic data was disclosed to the LLM — only derived findings (gene names, HPO terms, consequence annotations) and code. Variant-level processing ran locally; external API calls sent only variant coordinates. Details in the privacy section below.

---

## Rationale for the top-ranked pair

- **Phenotype match:** rhabdomyosarcoma occurs in ~75% of BUB1B-MVA patients but has not been reported in CEP57-MVA — the single most informative phenotype discriminator among panel genes.
- **Genetic configuration:** the proband's parents' recurrent miscarriages are consistent with both parents being BUB1B carriers (aneuploid embryo loss), i.e., compound-het inheritance.
- **Allele 1 (chr15:40209701 T>G, p.Leu737*):** ClinVar pathogenic nonsense; NMD-eligible → null allele.
- **Allele 2 (chr15:40220612 T>G, p.Asn1002Lys):** novel missense in the pseudokinase C-lobe; adjacent to known unstable variant L1012P; predicted deleterious by SIFT and PolyPhen → hypomorphic allele.
- **Mechanistic coherence:** null + unstable-missense compound-het is the classic BUB1B-MVA genotype pattern (biallelic, one severe + one partial-loss allele).

## Privacy & data-handling statement

Per the hackathon's Processor/Recipient framework: (i) the VCF, genotypes, and all genome-wide variant tables were processed only locally; (ii) Ensembl VEP acted as a Processor — it received bare variant coordinates and returned annotations, retaining no rights in the data; (iii) the LLM (Devin/Cognition) received only derived findings and code, never raw or reconstructive genomic data; (iv) protected data will be deleted within 30 days of the Hackathon's close per the data-use agreement, with deletion attestation preserved.

## References

1. Suijkerbuijk SJE et al. *Cancer Res* 2010;70:4891 — BUBR1 truncation/NMD biology in MVA
2. Hanks S et al. *Nat Genet* 2004;36:1159 — biallelic BUB1B → MVA + cancer
3. Matsuura S et al. *Am J Med Genet A* 2007;143A:358 — BUBR1 dose threshold
4. Malumbres M et al. *Nat Rev Genet* 2024 — MVA gene landscape (11-gene panel source)
5. Roy B et al. *PNAS* 2016;113:12508 — readthrough biochemistry (mechanistic context)
6. Ensembl VEP, UniProt O60566, ClinVar rs759242053 — public annotation resources
