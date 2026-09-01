# BUB1B Compound-Het 分析结论

> 日期：2026-09-01
> 这是候选 findings（少量命名变异），合规。

## 致病变异对（compound-heterozygous）

| | Allele 1 | Allele 2 |
|---|---|---|
| 基因 | BUB1B | BUB1B |
| 染色体 | 15 | 15 |
| 坐标 (GRCh38) | 40209701 | 40220612 |
| ref | T | T |
| alt | G | G |
| 基因型 | 0/1 (het) | 0/1 (het) |
| GQ | 99 | 99 |
| DP | 46 | 28 |
| AD (ref,alt) | 21,25 | 15,13 |
| VEP 注释 | stop_gained | missense_variant |
| 蛋白变化 | p.Leu737* | p.Asn1002Lys |
| 转录本 | ENST00000287598 (MANE Select) | ENST00000287598 |
| ClinVar | **pathogenic** (rs759242053, RCV003324778) | 未报告 |
| SIFT | — | 0.01 (deleterious) |
| PolyPhen | — | 0.997 (probably_damaging) |
| Impact | HIGH | MODERATE |

## 排除的其他 BUB1B 变异

所有其他 BUB1B 变异（14 个）经 VEP 注释均为：
- intron_variant（内含子，不影响编码）
- downstream_gene_variant（基因下游，不影响）

包括之前以为是 LoF 的 frameshift 变异（40181093, 40198239, 40216568, 40216570）——
全部在内含子中，不是编码区 frameshift。

## 表型吻合度

| 患者特征 | BUB1B (MVA1) 预期 | 吻合 |
|---|---|---|
| Rhabdomyosarcoma | ~75% 癌症率，rhabdo 是经典 | ✅ 强 |
| IUGR / 矮小 | Very frequent (80-99%) | ✅ 强 |
| Failure to thrive | 发育迟缓 frequent | ✅ |
| 早产 / 低出生体重 | IUGR 相关 | ✅ |
| 父母反复流产 | AR 携带者 → 非整倍体胚胎流失 | ✅ 强 |
| 无 microcephaly | BUB1B 常见但非必需 | ⚠️ 缺失但不排除 |
| 无眼异常 | BUB1B 常见但非必需 | ⚠️ 缺失但不排除 |

## 遗传模式

- 常染色体隐性 (AR)
- compound-heterozygous: 两个不同杂合变异
- 父母各携带一个 → 符合父母反复流产史（携带者婚配）

## 提交策略

- **Row 1**: compound-het pair (两个变异), EPCR=0.95, primary
- **Row 2**: stop_gained 单独 (备用，partial match), EPCR=0.85, primary
- **Row 3**: missense 单独 (备用), EPCR=0.6, primary
