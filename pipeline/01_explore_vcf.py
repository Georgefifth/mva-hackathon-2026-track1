#!/usr/bin/env python3
"""探查 VCF 结构 — 不输出任何变异坐标/基因型，只输出汇总统计。
安全可贴回对话。"""

import pysam
import sys
from collections import Counter

VCF = "/home/yap/mva-data/WGS_EX2312012_HGWCNDSX7.vcf.gz"

def main():
    vcf = pysam.VariantFile(VCF)

    # 样本
    samples = list(vcf.header.samples)
    print(f"样本数: {len(samples)}")
    for s in samples:
        print(f"  样本名: {s}")

    # header 里的关键信息
    print(f"\n--- Header 元信息 ---")
    for key in ["reference", "contig", "source", "GATKCommandLine", "commandline"]:
        for rec in vcf.header.records:
            if rec.key and key.lower() in rec.key.lower():
                print(f"  {rec.key}: {rec.value[:200] if rec.value else ''}")
                break

    # contig 数量
    contigs = list(vcf.header.contigs)
    print(f"\ncontig 数: {len(contigs)}")
    print(f"  前5个: {[c.name for c in contigs[:5]]}")

    # 变异统计
    total = 0
    by_chrom = Counter()
    by_type = Counter()
    pass_filter = 0
    qual_bins = Counter()

    # 只扫前 500k 变异做快速估计（全扫太慢）
    MAX = 500_000

    for rec in vcf:
        total += 1
        by_chrom[rec.chrom] += 1

        # variant type
        if rec.alts:
            alt = rec.alts[0]
            if len(rec.ref) == 1 and len(alt) == 1:
                by_type["SNV"] += 1
            elif len(alt) > len(rec.ref):
                by_type["INS"] += 1
            elif len(alt) < len(rec.ref):
                by_type["DEL"] += 1
            else:
                by_type["MNP/complex"] += 1
        else:
            by_type["no_alt"] += 1

        # filter
        if rec.filter.keys() == ["PASS"] or len(rec.filter) == 0:
            pass_filter += 1

        # quality
        q = rec.qual
        if q is None:
            qual_bins["missing"] += 1
        elif q < 20:
            qual_bins["<20"] += 1
        elif q < 50:
            qual_bins["20-50"] += 1
        elif q < 100:
            qual_bins["50-100"] += 1
        else:
            qual_bins["100+"] += 1

        if total >= MAX:
            print(f"\n(扫描前 {MAX} 条变异做快速估计)")
            break

    print(f"\n--- 变异统计 (前 {total} 条) ---")
    print(f"总数: {total}")
    print(f"PASS/无filter: {pass_filter} ({100*pass_filter/total:.1f}%)")
    print(f"\n按类型:")
    for t, c in by_type.most_common():
        print(f"  {t}: {c} ({100*c/total:.1f}%)")
    print(f"\n按质量:")
    for b in ["missing", "<20", "20-50", "50-100", "100+"]:
        if b in qual_bins:
            print(f"  {b}: {qual_bins[b]} ({100*qual_bins[b]/total:.1f}%)")
    print(f"\n按染色体 (前10):")
    for c, n in by_chrom.most_common(10):
        print(f"  {c}: {n}")

    # 检查 INFO 字段有哪些
    print(f"\n--- INFO 字段 ---")
    info_keys = list(vcf.header.info)
    print(f"  共 {len(info_keys)} 个 INFO 字段")
    for k in info_keys[:20]:
        rec = vcf.header.info[k]
        print(f"  {k}: {rec.description[:80]}")

    # 检查 FORMAT 字段
    print(f"\n--- FORMAT 字段 ---")
    fmt_keys = list(vcf.header.formats)
    print(f"  共 {len(fmt_keys)} 个 FORMAT 字段")
    for k in fmt_keys:
        rec = vcf.header.formats[k]
        print(f"  {k}: {rec.description[:80]}")

    vcf.close()

if __name__ == "__main__":
    main()
