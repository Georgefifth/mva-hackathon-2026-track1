# Track 2 Report — Drug Repurposing for BUB1B Compound-Heterozygous MVA

**Participant:** Georgefifth
**Hackathon:** Rare Disease, Real Kid: MVA Hackathon 2026
**Track:** 2 — Drug Repurposing
**Date:** 2026-09-23

---

## 1. Variant Mechanism Characterization

### 1.1 Identified Variants (from Track 1 analysis)

Compound-heterozygous BUB1B variants on MANE Select transcript ENST00000287598:

| | Allele 1 | Allele 2 |
|---|---|---|
| Coordinate (GRCh38) | chr15:40209701 T>G | chr15:40220612 T>G |
| Protein | p.Leu737* | p.Asn1002Lys |
| Type | Nonsense (UGA PTC) | Missense |
| ClinVar | Pathogenic (rs759242053) | Not reported |
| Population databases | rs759242053 (ultra-rare) | **Absent from dbSNP/gnomAD — novel** (ACMG PM2) |
| In silico | — | SIFT 0.01 (deleterious), PolyPhen 0.997 (probably_damaging) |

### 1.2 Allele-Specific Loss Mechanisms — Verified by Analysis

We analyzed each allele's loss mechanism computationally (script: `pipeline/04_readthrough_analysis.py`).

**Allele 1 (p.Leu737*) — loss via nonsense-mediated decay:**

The T>G substitution converts codon TTA (Leu) to TGA — a **UGA premature termination codon**. Exon-structure analysis of ENST00000287598 (23 exons) confirms the PTC lies in **exon 17 of 23**, ~10.9 kb upstream of the last exon-exon junction — far exceeding the ~50-55 nt NMD threshold. **The transcript is NMD-eligible and will be degraded.**

This matches published MVA biology: Suijkerbuijk et al. (Cancer Res 2010) showed BUBR1 truncation alleles (including 731X — 6 residues from ours) produce **no detectable protein in patient cells** due to NMD, yet the same truncations express stably at ≥ wild-type levels when NMD is bypassed by plasmid expression.

**Allele 2 (p.Asn1002Lys) — loss via protein instability:**

N1002K sits in the C-terminal **protein kinase domain (residues 766-1050; UniProt O60566)** — position 1002 lies in the kinase C-lobe. It is directly adjacent to **L1012P**, a known MVA missense shown to destabilize BUBR1. Four MVA-associated missense mutations in this domain (R727C, R814H, L844F, L1012P) all cause protein instability rather than catalytic loss — BUBR1's kinase domain is a **pseudokinase** that functions as a scaffold, and C-lobe substitutions appear to compromise structural integrity. N1002K is absent from all population databases (novel; ACMG PM2), supporting pathogenicity via the same instability mechanism.

### 1.3 Downstream Consequence

BUBR1 is a core spindle assembly checkpoint (SAC) protein:

- **N-terminal ~450 aa** (retained in any readthrough or stabilized product): contains KEN-box/D-box motifs for **APC/C-CDC20 inhibition** and the **KNL1 kinetochore-binding region (152-185)**. The mitotic checkpoint complex (MCC: MAD2-BUB3-BUBR1-CDC20) assembles **in the cytosol** — kinetochore localization is not strictly required for APC/C inhibition.
- **C-terminal kinase domain (766-1050)**: pseudokinase scaffold supporting kinetochore-microtubule attachment and MCC stability.

Biallelic loss → SAC failure → premature anaphase → mosaic variegated aneuploidy → the proband's phenotype (IUGR, short stature, rhabdomyosarcoma).

### 1.4 The Critical Pharmacological Insight: Threshold Effect

Matsuura et al. (AJMG 2007): heterozygous carriers with ~50% BUBR1 are asymptomatic; **>50% reduction causes disease**. The phenotype is dose-responsive, not all-or-nothing. **Restoring even 20-30% of BUBR1 function may cross the therapeutic threshold** — a decisive factor because readthrough drugs rarely restore >50%.

---

## 2. Readthrough-Amenability Analysis of Allele 1

We built a reproducible analyzer (`pipeline/04_readthrough_analysis.py`) that scores any nonsense variant for drug-induced readthrough suitability. Applied to our variant:

| Factor | Result | Favorable? |
|---|---|---|
| NMD eligibility | Exon 17/23; >10 kb from last junction | ✅ Confirmed |
| Stop codon class | **UGA** — the most readthrough-responsive codon | ✅ |
| +4 nucleotide context | **A** (UGA-A) — favorable context (score 2/3) | ✅ |
| Readthrough insertion | Trp / Arg / Cys at position 737 (Roy et al., PNAS 2016) | Neutral — substitution in linker region between BUB1 N-terminal domain (ends 226) and kinase domain (starts 766); not in a catalytic or binding motif |
| Truncated-product backup | Even without full-length readthrough, expressed **737X retains N-terminal 450 aa** → APC/C inhibition + KNL1 binding intact | ✅ |

**Composite score: 7/7 — strong readthrough candidate.**

A key consequence: this variant has **two independent rescue routes**. (a) Readthrough yields near-full-length protein (737-substituted). (b) NMD inhibition alone yields stable 737X, which retains the checkpoint-inhibitory N-terminus. Route (b) does not even require successful translational readthrough — it only requires the mutant mRNA to survive.

---

## 3. Drug Repurposing Candidates

### 3.1 Primary: Ataluren (Translarna, PTC124)

| Attribute | Detail |
|---|---|
| Mechanism | Competitive inhibitor of release-factor-complex termination → ribosomal readthrough of PTC |
| Regulatory | **EMA conditional approval** for nonsense-mutation DMD (2014; extended to ambulatory children 2-5 yr); STRIDE real-world registry ongoing; not FDA-approved |
| Pediatric safety | Established — chronic dosing in children ≥2 yr; consistently low toxicity |
| Match to variant | UGA PTC = best-responsive codon class; favorable +4 context; produces full-length protein with single substitution (L737W/R/C) |

**Honest limitations:** readthrough efficiency typically 10-25% and context-dependent; CF Phase III failed (efficacy is disease- and PTC-specific); no MVA precedent. However, the BUBR1 dose-threshold (>50% loss → disease) means even the low end of typical readthrough efficiency may suffice.

### 3.2 Secondary: Amlexanox — Independent Mechanism via NMD Inhibition

| Attribute | Detail |
|---|---|
| Mechanism | **Dual**: (a) NMD inhibition → more mutant mRNA available; (b) direct PTC readthrough via ribosomal A-site mimicry |
| Regulatory | Approved in Japan 1987 (asthma/aphthous ulcers); withdrawn 2019 for **commercial, not safety** reasons; Fortuity Pharma pursuing rare-disease re-approval |
| Safety | Decades of chronic-use safety data; crosses blood-brain barrier |
| Evidence | RDEB patient cells: 8/12 PTC alleles responded, some >50% of normal protein (J Invest Dermatol 2017); N=1 WOREE syndrome trial: clinical improvement, regression on withdrawal |

**Why it may matter more than ataluren here:** amlexanox's NMD inhibition alone could let the stable, partially-functional **737X truncated protein** accumulate — a route that does not depend on translational readthrough efficiency at all.

**Limitations:** currently no commercial supply; genotype-dependent efficacy; pleiotropic NMD effects uncharacterized.

### 3.3 Combination Rationale (Hypothesis)

Ataluren and amlexanox attack **different bottlenecks** in the PTC→protein pathway: amlexanox increases substrate (PTC-mRNA survival), ataluren increases yield-per-transcript (termination suppression). Ko et al. (NAR 2025) formally demonstrated that termination-inhibiting and misincorporation-promoting readthrough agents act orthogonally and can be combined. Proposed for preclinical testing in patient-derived cells.

### 3.4 Allele 2 (Missense) — Proteostasis Direction (Exploratory)

N1002K most likely destabilizes BUBR1 (adjacent to unstable L1012P). Protein-stability restoration is a validated repurposing strategy with real precedents: **ambroxol** (approved mucolytic) acts as a pharmacological chaperone for unstable GBA variants in Gaucher disease; **sodium 4-phenylbutyrate** (approved for urea-cycle disorders) is a generic chemical chaperone. No BUBR1-specific chaperone exists — we flag this as an **exploratory adjunct**, testable by measuring BUBR1 abundance in patient cells after chaperone exposure. If the missense protein is already degraded, restoring Allele 1 via readthrough remains the dominant strategy — again, the threshold model means one rescued allele may be enough.

### 3.5 Approaches Rejected on Mechanism or Safety Grounds

| Approach | Reason |
|---|---|
| Aminoglycosides (gentamicin/G418) | Ototoxicity/nephrotoxicity exclude chronic pediatric use; experimental control only |
| eRF1/eRF3a degraders (CC-90009, SRI-41315) | Engineered as anticancer agents promoting global readthrough — unacceptable in a cancer-prone child |
| HSP90 inhibitors / autophagy modulators | Global proteostasis disruption; pro-apoptotic in dividing cells; wrong direction for checkpoint rescue |
| Proteasome inhibitors (bortezomib) | Would stabilize missense protein but is cytotoxic chemotherapy — contraindicated for chronic use |
| Gene therapy / ACE-tRNA | Not an existing approved medication — outside Track 2 scope |

---

## 4. The Cancer Context — Addressed Honestly

The proband already has rhabdomyosarcoma. Our proposal must account for this:

1. **What the drug would do:** restoring SAC function reduces the *rate of new aneuploidy events* in healthy tissues. It does not treat the existing tumor.
2. **Why it may still matter:** MVA patients face **recurrent, early-onset cancer risk** throughout childhood (rhabdomyosarcoma, Wilms tumor, leukemia). Slowing new aneuploidy accumulation could reduce second-malignancy risk — the dominant long-term threat.
3. **A subtle oncology interaction:** taxane-class chemotherapy depends on sustained SAC-mediated mitotic arrest for efficacy. A weakened SAC may confer partial taxane resistance; restored BUBR1 could normalize chemosensitivity — relevant if the proband receives mitotic-poison chemotherapy. (Hypothesis-level; flagged, not asserted.)
4. **Risk acknowledgment:** any intervention modulating a checkpoint in a child with active malignancy requires tumor-board-level review. Our proposal is a hypothesis for validation, not a treatment recommendation.

---

## 5. Proposed Validation Pathway (Scalability Demonstration)

1. **Patient-derived fibroblasts/lymphoblasts** → ataluren ± amlexanox → measure: BUBR1 protein (WB), SAC integrity (nocodazole arrest assay), aneuploidy fraction (karyotype/SNP-array). All endpoints are measurable in standard cell culture.
2. **Our analyzer generalizes:** `04_readthrough_analysis.py` scores any nonsense variant (any gene, any disease) for NMD eligibility, codon class, context, and truncated-product salvageability — the same pipeline applies to ~12% of all disease mutations (PTC fraction), i.e., the approach scales beyond this single case.

---

## 6. Summary Table

| Rank | Candidate | Mechanism | Allele | Evidence tier |
|---|---|---|---|---|
| 1 | **Ataluren** | PTC readthrough (RFC inhibition) | 1 | EMA-approved; pediatric data; UGA-optimal variant |
| 2 | **Amlexanox** | NMD inhibition + readthrough | 1 | Approved history; enables stable 737X expression without readthrough |
| 3 | Ataluren + amlexanox | Orthogonal combination | 1 | Mechanistic rationale (NAR 2025) |
| 4 | Chemical chaperone (e.g., 4-PBA/ambroxol-class) | Protein stabilization | 2 | Exploratory; precedent in other diseases |

---

## 7. LLM and AI Tool Usage Declaration

| Tool | Provider | Plan/Tier | Data Handling |
|---|---|---|---|
| Devin | Cognition AI | Individual plan | Default terms; **no protected genomic data entered into Devin** — only derived findings (variant annotations, gene/protein facts, literature) and code were processed. |
| Ensembl REST API (VEP, sequence, lookup) | EMBL-EBI | Public | Annotation/sequence lookup; only variant coordinates sent |
| UniProt REST API | UniProt consortium | Public | Protein domain annotation |

All genomic analysis ran locally; external APIs received only public-database identifiers or variant coordinates (Processor-equivalent usage per hackathon Discussion #2 framework).

## 8. Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON, with prize sponsorship from AWS and Anthropic. We thank the child and family who generously contributed their data and story.

---

## References

1. Suijkerbuijk SJE et al. *Cancer Res* 2010;70:4891 — BUBR1 truncations stable when NMD bypassed; N-term 450aa = APC/C inhibition
2. Roy B et al. *PNAS* 2016;113:12508 — ataluren near-cognate tRNA insertion specificity (UGA→W/R/C)
3. Ko W et al. *Nucleic Acids Res* 2025;gkaf216 — orthogonal readthrough mechanisms support combination design
4. Matsuura S et al. *Am J Med Genet A* 2007;143A:358 — BUBR1 dose-threshold (>50% loss → disease)
5. Hanks S et al. *Nat Genet* 2004;36:1159 — biallelic BUB1B → aneuploidy + cancer predisposition
6. Atanasova VS et al. *J Invest Dermatol* 2017;137:2214 — amlexanox readthrough in RDEB patient cells
7. Wijaya YI et al. thesis (Groningen) — BUBR1 pseudokinase-domain missense instability (R727C/R814H/L844F/L1012P)
8. Malumbres M et al. *Nat Rev Genet* 2024 — MVA gene/ pathway landscape review
