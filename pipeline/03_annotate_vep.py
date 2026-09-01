#!/usr/bin/env python3
"""用 Ensembl VEP REST API POST 批量注释变异。
Ensembl VEP = 变异注释工具（Processor），合规。"""

import json
import urllib.request
import csv
import time

TSV = "/home/yap/Hack/Disease/analysis/mva_candidates.tsv"
OUT = "/home/yap/Hack/Disease/analysis/mva_annotated.tsv"

TARGET_GENES = {"BUB1B", "CEP57", "TRIP13", "CENATAC", "MAD2L1BP", "BUB1"}

def make_hgvs(chrom, pos, ref, alt):
    """生成 HGVS g. notation"""
    if len(ref) == 1 and len(alt) == 1:
        return f"{chrom}:g.{pos}{ref}>{alt}"
    elif len(alt) < len(ref):
        # deletion
        if len(alt) == 1 and len(ref) > 1:
            return f"{chrom}:g.{pos}_{pos+len(ref)-len(alt)}del"
        elif len(alt) == 0:
            return f"{chrom}:g.{pos}_{pos+len(ref)-1}del"
        else:
            return f"{chrom}:g.{pos}delins{alt}"
    elif len(alt) > len(ref):
        # insertion
        if len(ref) == 1:
            return f"{chrom}:g.{pos}ins{alt[1:]}"
        else:
            return f"{chrom}:g.{pos}delins{alt}"
    else:
        return f"{chrom}:g.{pos}delins{alt}"

def batch_vep(variants, batch_size=10):
    """批量查询 VEP"""
    all_results = []
    for i in range(0, len(variants), batch_size):
        batch = variants[i:i+batch_size]
        url = "https://rest.ensembl.org/vep/human"
        payload = json.dumps({"variants": batch}).encode()
        req = urllib.request.Request(url, data=payload, headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                all_results.extend(data)
                print(f"  批次 {i//batch_size+1}: {len(data)} 结果")
        except Exception as e:
            print(f"  批次 {i//batch_size+1}: ERROR - {e}")
            # 逐个重试
            for v in batch:
                try:
                    single_url = f"https://rest.ensembl.org/vep/human/hgvs/{urllib.parse.quote(v)}?content-type=application/json"
                    req2 = urllib.request.Request(single_url, headers={"Accept": "application/json"})
                    with urllib.request.urlopen(req2, timeout=15) as resp2:
                        d = json.loads(resp2.read())
                        all_results.extend(d)
                except Exception as e2:
                    all_results.append({"input": v, "error": str(e2)})
        time.sleep(0.5)
    return all_results

def main():
    import urllib.parse

    # 读取 TSV
    rows = []
    with open(TSV) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            if r["gene"] in TARGET_GENES:
                rows.append(r)

    print(f"待注释: {len(rows)} 个变异\n")

    # 生成 HGVS
    hgvs_list = []
    for r in rows:
        h = make_hgvs(r["chrom"], int(r["pos"]), r["ref"], r["alt"])
        hgvs_list.append(h)

    # 批量查询
    results = batch_vep(hgvs_list)

    # 建立映射
    result_map = {}
    for r in results:
        inp = r.get("input", "")
        result_map[inp] = r

    # 解析注释
    severity_order = [
        "frameshift_variant", "stop_gained", "stop_lost", "start_lost",
        "splice_acceptor_variant", "splice_donor_variant",
        "missense_variant", "inframe_insertion", "inframe_deletion",
        "synonymous_variant", "intron_variant", "upstream_gene_variant",
        "downstream_gene_variant", "intergenic_variant"
    ]
    lof_types = {"frameshift_variant", "stop_gained", "stop_lost", "start_lost",
                 "splice_acceptor_variant", "splice_donor_variant"}

    annotated = []
    for i, r in enumerate(rows):
        h = hgvs_list[i]
        vep_data = result_map.get(h, {})

        if "error" in vep_data:
            csq, gene, hgvs_c, hgvs_p, impact = "ERROR", "", "", "", ""
        else:
            consequences = vep_data.get("transcript_consequences", [])
            best = None
            best_rank = 999
            for tc in consequences:
                for c in tc.get("consequence_terms", []):
                    if c in severity_order:
                        rank = severity_order.index(c)
                        if rank < best_rank:
                            best_rank = rank
                            best = tc
            if best:
                csq = ",".join(best.get("consequence_terms", []))
                gene = best.get("gene_symbol", "")
                hgvs_c = best.get("hgvsc", "")
                hgvs_p = best.get("hgvsp", "")
                impact = best.get("impact", "")
            else:
                csq = "no_transcript"
                gene = ""
                hgvs_c = ""
                hgvs_p = ""
                impact = ""

        entry = {**r, "consequence": csq, "ens_gene": gene,
                 "hgvsc": hgvs_c, "hgvsp": hgvs_p, "impact": impact}
        annotated.append(entry)

        lof_mark = "🚨" if csq in lof_types else "  "
        print(f"  {lof_mark} {r['gene']:<10} {r['gt']:<5} {r['type']:<20} → {csq:<25} {gene} {hgvs_p}")

    # 写结果
    cols = list(rows[0].keys()) + ["consequence", "ens_gene", "hgvsc", "hgvsp", "impact"]
    with open(OUT, "w") as f:
        f.write("\t".join(cols) + "\n")
        for r in annotated:
            f.write("\t".join(str(r.get(c, "")) for c in cols) + "\n")

    # 汇总
    print(f"\n{'='*70}")
    print(f"注释完成: {OUT}")
    print(f"{'='*70}")

    print("\n🚨 LoF 变异:")
    for gene in sorted(TARGET_GENES):
        lof = [r for r in annotated if r["gene"] == gene and r["consequence"] in lof_types]
        if lof:
            print(f"\n  {gene}: {len(lof)} 个 LoF")
            for v in lof:
                print(f"    {v['gt']:<5} {v['consequence']:<25} {v['hgvsc']} {v['hgvsp']}")

    print(f"\n{'='*70}")
    print("🎯 杂合 LoF（compound-het 候选）:")
    print(f"{'='*70}")
    for gene in sorted(TARGET_GENES):
        het_lof = [r for r in annotated if r["gene"] == gene
                   and r["gt"] in ("0/1", "1/0", "0|1", "1|0")
                   and r["consequence"] in lof_types]
        if het_lof:
            print(f"\n  {gene}: {len(het_lof)} 个杂合 LoF")
            for v in het_lof:
                print(f"    {v['consequence']:<25} {v['hgvsc']} {v['hgvsp']}")

    print(f"\n{'='*70}")
    print("📌 纯合 LoF（homozygous recessive）:")
    print(f"{'='*70}")
    for gene in sorted(TARGET_GENES):
        hom_lof = [r for r in annotated if r["gene"] == gene
                   and r["gt"] in ("1/1", "1|1")
                   and r["consequence"] in lof_types]
        if hom_lof:
            print(f"\n  {gene}: {len(hom_lof)} 个纯合 LoF")
            for v in hom_lof:
                print(f"    {v['consequence']:<25} {v['hgvsc']} {v['hgvsp']}")

    # missense 也列出来（可能是 pathogenic missense）
    print(f"\n{'='*70}")
    print("⚠️ 杂合 missense（可能是第二个 compound-het allele）:")
    print(f"{'='*70}")
    for gene in sorted(TARGET_GENES):
        het_miss = [r for r in annotated if r["gene"] == gene
                    and r["gt"] in ("0/1", "1/0", "0|1", "1|0")
                    and r["consequence"] == "missense_variant"]
        if het_miss:
            print(f"\n  {gene}: {len(het_miss)} 个杂合 missense")
            for v in het_miss:
                print(f"    {v['hgvsc']} {v['hgvsp']}")

if __name__ == "__main__":
    main()
