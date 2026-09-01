# Track 1 Methods Report — BUB1B Compound-Heterozygous Variant Prediction

**Participant:** Georgefifth
**Hackathon:** Rare Disease, Real Kid: MVA Hackathon 2026
**Track:** 1 — Variant Prediction
**Date:** 2026-09-01

---

## 1. Approach Overview

This submission identifies a compound-heterozygous variant pair in **BUB1B** as the likely causal variants for the proband's Mosaic Variegated Aneuploidy (MVA) phenotype. The approach combines phenotype-driven gene prioritization with systematic variant filtering and functional annotation.

## 2. Phenotype Analysis

The proband's clinical presentation was extracted from the provided clinical phenotype document and mapped to Human Phenotype Ontology (HPO) terms:

| Clinical Feature | HPO ID |
|---|---|
| Rhabdomyosarcoma | HP:0002859 |
| Nephrocalcinosis | HP:0000121 |
| Short stature | HP:0004322 |
| Failure to thrive | HP:0001508 |
| Skeletal muscle atrophy | HP:0003202 |
| Premature birth (32 weeks) | HP:0001622 |
| Small for gestational age (~1kg) | HP:0001518 |
| Parental recurrent miscarriages | HP:0200067 |

The constellation of cancer predisposition (rhabdomyosarcoma), growth restriction (IUGR, short stature, failure to thrive), adverse perinatal history, and parental reproductive loss is consistent with MVA syndrome. The absence of microcephaly and ocular abnormalities, while atypical for classic MVA1, does not exclude the diagnosis given the broad phenotypic spectrum.

## 3. Gene Prioritization

A curated list of 11 MVA-associated genes was compiled from literature (MedlinePlus, Orphanet, OMIM, Malumbres 2024 Nat Rev Genet):

| Gene | MVA Subtype | GenCC Evidence | Priority |
|---|---|---|---|
| BUB1B | MVA1 | Definitive | 1 (highest) |
| CEP57 | MVA2 | Definitive | 2 |
| TRIP13 | MVA3 | Strong | 3 |
| CENATAC | MVA4 | — | 4 |
| MAD1L1 | MVA7 | — | 5 |
| MAD2L1BP | — | — | 6 |
| CEP192 | — | — | 7 |
| BUB1 | — | Supportive | 8 |
| BUB3 | — | Supportive | 9 |
| SMC5 | MVA5 | — | 10 |
| SLF2 | MVA6 | — | 11 |

BUB1B was prioritized as the top candidate because:
- Rhabdomyosarcoma is a classic BUB1B-associated malignancy (~75% cancer rate in MVA1)
- IUGR and growth restriction are core MVA1 features (80-99% frequency)
- Parental recurrent miscarriages are consistent with autosomal recessive carrier parents
- CEP57 was deprioritized because CEP57-mutant patients have no reported cancers, contradicting the proband's rhabdomyosarcoma

## 4. Variant Analysis Pipeline

### 4.1 Data
- Input: GATK-called WGS VCF (GRCh38, single sample: WGS_EX2312012)
- The VCF was provided by the hackathon organizers; no re-alignment or variant calling was performed

### 4.2 Filtering
Variants within ±2kb of each candidate gene's genomic boundaries were extracted using pysam. Quality filters applied:
- PASS filter or no filter flag
- Genotype Quality (GQ) ≥ 20
- Read Depth (DP) ≥ 10
- Alternate allele depth (AD) ≥ 3

### 4.3 Compound-Heterozygous Detection
For each gene, heterozygous variants passing quality filters were identified. Genes with ≥2 heterozygous variants were flagged as potential compound-het candidates. Physical phasing information (PGT/PID fields in the VCF) was examined where available.

### 4.4 Functional Annotation
Variants were annotated using the Ensembl VEP REST API (GRCh38). Consequence terms were ranked by severity (frameshift > stop_gained > splice > missense > synonymous > intronic). ClinVar co-located variants and population frequencies (gnomAD) were retrieved where available.

## 5. Results

### 5.1 BUB1B Compound-Heterozygous Pair

Two heterozygous coding variants in BUB1B were identified on the MANE Select transcript (ENST00000287598, NM_001211.6):

| | Allele 1 | Allele 2 |
|---|---|---|
| Coordinate (GRCh38) | chr15:40209701 | chr15:40220612 |
| Change | T>G | T>G |
| VEP Consequence | stop_gained | missense_variant |
| Protein effect | p.Leu737* | p.Asn1002Lys |
| Impact | HIGH | MODERATE |
| ClinVar | pathogenic (rs759242053, RCV003324778) | not reported |
| SIFT | — | 0.01 (deleterious) |
| PolyPhen | — | 0.997 (probably_damaging) |
| Genotype | 0/1 (heterozygous) | 0/1 (heterozygous) |
| GQ / DP | 99 / 46 | 99 / 28 |
| AD (ref, alt) | 21, 25 | 15, 13 |

**Allele 1** (p.Leu737*) is a nonsense mutation truncating BUBR1 at position 737 of 1050 amino acids, removing the C-terminal APC/C interaction domain. This variant is classified as pathogenic in ClinVar and has been reported in MVA1 patients.

**Allele 2** (p.Asn1002Lys) is a missense mutation near the C-terminus. Both SIFT (0.01) and PolyPhen (0.997) predict it as deleterious/probably damaging.

### 5.2 Exclusion of Other BUB1B Variants
All other 12 BUB1B variants (including 3 homozygous and 1 heterozygous indel initially classified as frameshift by length-based heuristics) were confirmed by VEP annotation to be intronic or downstream gene variants with no coding impact.

### 5.3 Other MVA Genes
- **CEP57**: 2 homozygous intronic indels, 2 heterozygous intronic SNVs — no coding LoF
- **TRIP13**: 1 heterozygous intronic SNV — no coding LoF
- **CENATAC**: 11 homozygous intronic/upstream indels, 1 heterozygous missense (p.? in non-MANE transcript) — no clear biallelic coding LoF
- **MAD2L1BP**: 4 heterozygous intronic/upstream SNVs — no coding LoF
- **BUB1**: 5 homozygous intronic indels, 3 heterozygous intronic SNVs — no coding LoF
- **MAD1L1, BUB3, CEP192, SMC5, SLF2**: High variant counts suggestive of low-complexity regions or segmental duplications; frameshift calls likely artifacts. Not pursued as primary candidates.

## 6. Submission

Three rows submitted:
1. **Compound-het pair** (both variants), EPCR=0.95 — primary candidate
2. **stop_gained alone**, EPCR=0.85 — backup for partial match scoring
3. **missense alone**, EPCR=0.60 — backup for partial match scoring

## 7. LLM and AI Tool Usage Declaration

| Tool | Provider | Plan/Tier | Data Handling |
|---|---|---|---|
| Devin | Cognition AI | Individual plan | Default: may use data for model training unless opted out. Zero Data Retention available with opt-out on paid plans. **No protected genomic data (VCF content, variant coordinates, genotypes) was entered into Devin.** Only derived findings (gene names, HPO terms, consequence annotations, literature) were processed. Raw data analysis was performed locally via scripts written by Devin but executed by the user. |
| Ensembl VEP REST API | EMBL-EBI | Public | Processes variant coordinates to return annotations; does not retain or train on input data. Only variant coordinates (chr:pos:ref:alt) were sent, no sample identifiers or genotype data. |

**Data handling note:** Per the hackathon's Processor vs Recipient framework (Discussion #2, Sage Privacy Officer), Ensembl VEP functions as a Processor (returns annotations, does not retain or train on input). Devin was used in a restricted mode where no protected genomic data entered the conversation — only gene names, HPO terms, literature findings, and code. The user verified that this approach complies with the conservative interpretation of the data use rules.

## 8. Limitations

- No trio data available (single-subject dataset); compound-het phase (cis vs trans) could not be definitively confirmed from PGT/PID alone for these two variants
- The missense allele (p.Asn1002Lys) lacks ClinVar classification; pathogenicity is inferred from in silico predictions only
- Nephrocalcinosis is not a standard MVA HPO term and may represent a secondary complication or an atypical feature
- High-variant-count genes (MAD1L1, BUB3, CEP192, SMC5, SLF2) were not exhaustively annotated due to likely artifact contamination in low-complexity regions

## 9. Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
