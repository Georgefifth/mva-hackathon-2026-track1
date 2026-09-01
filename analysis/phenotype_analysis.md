# 患者临床表型分析

> 来源：Challenge_Clinical_Phenotype_1.docx（本地提取）
> 日期：2026-09-01
> ⚠️ 不含基因组数据，仅表型文本 + HPO terms，合规。

---

## 1. 患者表型清单

| 临床特征 | HPO Term | HPO ID | 备注 |
|---|---|---|---|
| Rhabdomyosarcoma | Rhabdomyosarcoma | HP:0002859 | **主要肿瘤事件**，触发紧急检查 |
| Nephrocalcinosis | Nephrocalcinosis | HP:0000121 | 肾钙质沉着，出生即有 |
| Short stature | Short stature | HP:0004322 | 身高显著低于预期 |
| Failure to thrive | Failure to thrive | HP:0001508 | 反复记录，早期起病，体重增长差+肌肉发育差 |
| Skeletal muscle atrophy | Skeletal muscle atrophy | HP:0003202 | 肌肉量减少 |
| Premature birth | Premature birth | HP:0001622 | 32 周早产 |
| Small for gestational age | Small for gestational age | HP:0001518 | 出生约 1kg，严重低体重，IUGR |
| Recurrent spontaneous abortion（父母） | Recurrent spontaneous abortion | HP:0200067 | 父母多次流产史 |

## 2. proband_id
- 提交系统只接受 **PROBAND01**（来自 evaluation.py / submit_track1.py）。

---

## 3. 表型组合分析

### 3.1 核心特征集群
1. **癌症倾向**：Rhabdomyosarcoma（横纹肌肉瘤）—— MVA 经典儿童肿瘤之一
2. **生长受限**：IUGR + 早产 + 矮小 + failure to thrive
3. **肾异常**：Nephrocalcinosis（肾钙质沉着）
4. **不良生育史**：父母反复流产

### 3.2 与 MVA 经典表型的对比

| 患者有 | MVA 经典 | 匹配 |
|---|---|---|
| Rhabdomyosarcoma | ✅ MVA 经典肿瘤（BUB1B ~75% 癌症率） | **强匹配** |
| Short stature / IUGR | ✅ Very frequent (80-99%) | **强匹配** |
| Failure to thrive / 肌肉萎缩 | ✅ 发育迟缓 frequent | **匹配** |
| Premature birth / 低出生体重 | ✅ IUGR 相关 | **匹配** |
| Nephrocalcinosis | ❌ 不在 MVA 标准 HPO 里 | **不典型** |
| 父母反复流产 | ✅ 染色体不稳定 → 非整倍体胚胎流失 | **强匹配** |
| Microcephaly | ❌ 患者未报告 | 缺失 |
| 眼异常 (cataract/glaucoma) | ❌ 患者未报告 | 缺失 |
| Dandy-Walker | ❌ 患者未报告 | 缺失 |
| café-au-lait 斑 | ❌ 患者未报告 | 缺失 |

### 3.3 关键判断

**患者有 rhabdomyosarcoma + IUGR + 父母反复流产，但无小头、无眼异常、无 café-au-lait。**

这指向：
1. **BUB1B (MVA1)** — 最强候选。rhabdomyosarcoma 是 BUB1B 突变患者的经典肿瘤，
   IUGR/矮小是 MVA1 核心特征。BUB1B 有 ~75% 癌症率，最高。
   但患者缺 microcephaly 和眼异常（BUB1B 常见），不完全典型。

2. **CEP57 (MVA2)** — 次选。但 CEP57 患者无癌症报告，而患者有 rhabdomyosarcoma → **可能性降低**。

3. **TRIP13 (MVA3)** — 需考虑。TRIP13 关联 Wilms tumor（不是 rhabdomyosarcoma），
   且常伴 café-au-lait 斑（患者无）→ **可能性中低**。

4. **MAD2L1BP** — 关联颗粒细胞瘤，不是 rhabdomyosarcoma → 低。

5. **MAD1L1 (MVA7)** — 有肿瘤倾向+炎症，但患者无炎症表现 → 中低。

### 3.4 父母反复流产的信号

文档明确提示：反复流产在染色体不稳定疾病中反映**可遗传机制**。
AR 遗传 → 父母都是携带者 → 胚胎如果是 biallelic 突变可能早期流失（非整倍体胚胎多数自然流产）。
这强化了 **compound-heterozygous AR** 模型，与 evaluation.py 的答案结构一致。

### 3.5 Nephrocalcinosis — 非典型特征

肾钙质沉着不在 MVA 标准 HPO 里。可能：
- MVA 的偶发表现（MVA 表型谱很广，103 个 HPO）
- 或暗示某个特定基因的额外表型
- 或是继发于早产/IUGR 的并发症
- **不应排除 MVA 诊断**，但值得在 methods 里讨论

---

## 4. 基因优先级排序（基于表型）

| 排名 | 基因 | 理由 | 置信度 |
|---|---|---|---|
| 1 | **BUB1B** | Rhabdomyosarcoma + IUGR + AR + 父母流产 → 完美吻合 MVA1 | 高 |
| 2 | **TRIP13** | 有癌症倾向，但 Wilms 而非 rhabdo，无 café-au-lait | 中 |
| 3 | **MAD1L1** | 肿瘤倾向，但无炎症特征 | 中低 |
| 4 | **CEP57** | 无癌症报告 vs 患者有 rhabdo → 矛盾 | 低 |
| 5 | **CENATAC** | compound het 已报道，但表型信息少 | 低 |
| 6 | **MAD2L1BP** | 颗粒细胞瘤 ≠ rhabdo | 低 |
| 7 | **CEP192** | 中心体，表型信息少 | 低 |
| 8 | **BUB1** | Supportive，AD 为主 | 低 |
| 9 | **BUB3** | Supportive，AD | 低 |

### 扩展候选（若已知基因无 biallelic LoF）
- SAC/有丝分裂/着丝粒相关基因（见 mva_mechanism.md 第 6 节）

---

## 5. Pipeline 搜索策略

1. **第一轮**：在 BUB1B 里找 biallelic LoF（nonsense/frameshift/splice/start-loss）
   - 期望找到 compound-het pair（2 个杂合变异）
   - 如果找到 → 这就是 top-1 提交候选

2. **第二轮**：在 TRIP13, MAD1L1, CEP57, CENATAC 里找 biallelic LoF

3. **第三轮**：在全部 9 个已知基因里找 biallelic missense（可能 pathogenic）

4. **第四轮**：扩展到 SAC/有丝分裂基因池

5. **排序**：用 HPO 匹配度 + ACMG 评级 + LoF 优先级合成 EPCR

---

## 6. 提交 CSV 预期结构

```
proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes
PROBAND01,chr15,<pos1>,<ref>,<alt>,chr15,<pos2>,<ref>,<alt>,0.95,primary,BUB1B compound-het; rhabdo+IUGR+AR
PROBAND01,chr5,<pos>,<ref>,<alt>,chr5,<pos>,<ref>,<alt>,0.6,primary,TRIP13 compound-het candidate
...
```

（坐标待 pipeline 填入，不在此文档中出现）
