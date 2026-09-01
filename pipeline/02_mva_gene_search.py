#!/usr/bin/env python3
"""在 11 个 MVA 候选基因区域提取变异，筛选质量，找 compound-het。
stdout = 汇总统计（安全）；详细写到本地 TSV。
"""
import pysam
import os
from collections import Counter

VCF = "/home/yap/Hack/Disease/data/WGS_EX2312012_HGWCNDSX7.vcf.gz"
DETAIL_TSV = "/home/yap/Hack/Disease/analysis/mva_candidates.tsv"

GENES = {
    "BUB1B":     ("15", 40160000, 40222000),
    "CEP57":     ("11", 95789000, 95838000),
    "TRIP13":    ("5",  892000,   920000),
    "CENATAC":   ("11", 118998000, 119016000),
    "MAD1L1":    ("7",  1815000,  2234000),
    "MAD2L1BP":  ("6",  43629000, 43641000),
    "CEP192":    ("18", 12991000, 13126000),
    "BUB1":      ("2",  110635000, 110679000),
    "BUB3":      ("10", 123154000, 123314000),
    "SMC5":      ("9",  70258000, 70355000),
    "SLF2":      ("10", 100912000, 100966000),
}

MIN_GQ, MIN_DP, MIN_AD_ALT = 20, 10, 3

def get_gt(rec):
    for s in rec.samples:
        dat = rec.samples[s]
        gt = dat.get("GT", None)
        if gt:
            return "/".join(str(x) for x in gt), dat
    return None, None

def classify(rec):
    ref, alts = rec.ref, rec.alts
    if not alts: return "no_alt"
    alt = alts[0]
    if len(ref) == 1 and len(alt) == 1: return "SNV"
    if len(alt) > len(ref):
        return "INS_inframe" if (len(alt)-len(ref)) % 3 == 0 else "INS_frameshift"
    if len(alt) < len(ref):
        return "DEL_inframe" if (len(ref)-len(alt)) % 3 == 0 else "DEL_frameshift"
    return "MNP/complex"

def main():
    vcf = pysam.VariantFile(VCF)
    gene_stats = {}
    all_rows = []

    for gene, (chrom, start, end) in GENES.items():
        s = {"total":0,"pass_qc":0,"het":0,"hom_alt":0,"by_type":Counter(),
             "lof_het":[],"lof_hom":[],"all_het":[]}
        try:
            for rec in vcf.fetch(chrom, start, end):
                s["total"] += 1
                filt = list(rec.filter.keys()) if rec.filter else []
                if filt and filt != ["PASS"]: continue
                gt_str, dat = get_gt(rec)
                if gt_str is None: continue
                gq = dat.get("GQ",0) or 0
                dp = dat.get("DP",0) or 0
                ad = dat.get("AD",None)
                if gq < MIN_GQ or dp < MIN_DP: continue
                alt_ad = ad[1] if ad and len(ad) >= 2 else 0
                if alt_ad < MIN_AD_ALT: continue
                s["pass_qc"] += 1
                vtype = classify(rec)
                s["by_type"][vtype] += 1
                is_het = gt_str in ("0/1","1/0","0|1","1|0")
                is_hom = gt_str in ("1/1","1|1")
                pgt = dat.get("PGT",None)
                pid = dat.get("PID",None)
                row = {"gene":gene,"chrom":chrom,"pos":rec.pos,
                       "ref":rec.ref,"alt":rec.alts[0] if rec.alts else ".",
                       "qual":rec.qual if rec.qual else 0,"gt":gt_str,
                       "gq":gq,"dp":dp,
                       "ad_ref":ad[0] if ad and len(ad)>=1 else 0,
                       "ad_alt":alt_ad,"type":vtype,
                       "pgt":str(pgt) if pgt else "","pid":str(pid) if pid else ""}
                all_rows.append(row)
                if is_het:
                    s["het"] += 1; s["all_het"].append(row)
                    if "frameshift" in vtype: s["lof_het"].append(row)
                elif is_hom:
                    s["hom_alt"] += 1
                    if "frameshift" in vtype: s["lof_hom"].append(row)
        except ValueError as e:
            print(f"  [警告] {gene}: {e}"); s["total"] = -1
        gene_stats[gene] = s

    vcf.close()

    cols = ["gene","chrom","pos","ref","alt","qual","gt","gq","dp","ad_ref","ad_alt","type","pgt","pid"]
    with open(DETAIL_TSV, "w") as f:
        f.write("\t".join(cols)+"\n")
        for r in all_rows:
            f.write("\t".join(str(r[c]) for c in cols)+"\n")

    print("="*70)
    print("MVA 候选基因变异汇总（不含坐标，安全）")
    print("="*70)
    print(f"\n详细: {DETAIL_TSV}")
    print(f"阈值: GQ>={MIN_GQ}, DP>={MIN_DP}, AD_ALT>={MIN_AD_ALT}\n")
    print(f"{'基因':<12}{'总':>6}{'QC':>6}{'杂合':>6}{'纯合':>6}{'FS杂':>6}{'FS纯':>6}")
    print("-"*70)
    for g in GENES:
        s = gene_stats[g]
        if s["total"] == -1: print(f"{g:<12}{'ERR':>6}"); continue
        print(f"{g:<12}{s['total']:>6}{s['pass_qc']:>6}{s['het']:>6}{s['hom_alt']:>6}{len(s['lof_het']):>6}{len(s['lof_hom']):>6}")

    print("\n" + "="*70)
    print("frameshift 杂合（compound-het 候选）")
    print("="*70)
    for g in GENES:
        s = gene_stats[g]
        if s["lof_het"]:
            print(f"\n  {g}: {len(s['lof_het'])} 个")
            for v in s["lof_het"]:
                print(f"    {v['type']}: GQ={v['gq']} DP={v['dp']} AD={v['ad_ref']},{v['ad_alt']} PGT={v['pgt']} PID={v['pid']}")

    print("\n" + "="*70)
    print(">=2 杂合的基因（潜在 compound-het）")
    print("="*70)
    for g in GENES:
        s = gene_stats[g]
        if s["het"] >= 2:
            types = Counter(v["type"] for v in s["all_het"])
            print(f"  {g}: {s['het']} 杂合 ({', '.join(f'{t}:{c}' for t,c in types.most_common())})")

    print("\n" + "="*70)
    print("纯合 alt（homozygous recessive）")
    print("="*70)
    for g in GENES:
        s = gene_stats[g]
        if s["hom_alt"] > 0:
            print(f"  {g}: {s['hom_alt']} 纯合")

if __name__ == "__main__":
    main()
