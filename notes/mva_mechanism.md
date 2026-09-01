# MVA 机制研究笔记

> 来源：MedlinePlus, Orphanet, OMIM, Malumbres 2024 (Nat Rev Genet), Sugi Atlas, CAGI6 RGP 论文
> 日期：2026-09-01
> 用途：指导 Track 1 变异优先排序。不含任何患者数据。

---

## 1. MVA 是什么

Mosaic Variegated Aneuploidy (MVA) 综合征：一种染色体不稳定性疾病，
特征是**多个组织的镶嵌非整倍体**（mosaic aneuploidies）——部分细胞染色体数异常
（三体/单体），且不同细胞的异常染色体不同（variegated）。非整倍体细胞比例通常 >25%。

- **流行病学**：全球 <1/1,000,000，已报告约 41 例/家系（Orphanet 验证）。
- **发病机制**：有丝分裂中染色体错误分离 → 镶嵌非整倍体。根源是**纺锤体组装检查点 (SAC)**
  或**着丝粒-微管附着**相关基因的双等位基因功能丧失突变。
- **遗传模式**：**常染色体隐性 (AR)**，患者为 biallelic（纯合或复合杂合）。
  父母为携带者。复发风险 25%。少数基因有显性单等位报道（BUB1, BUB3）。

---

## 2. 已知 MVA 致病基因（按证据强度排序）

这是 pipeline 的**第一优先基因列表**。evaluation.py 表明答案是 compound-heterozygous
（2 个变异），所以重点是找这些基因里的**双杂合变异对**。

| 基因 | 染色体 | MVA亚型 | GenCC 证据 | 遗传 | 蛋白功能 | 癌症风险 | 特征性表型 |
|---|---|---|---|---|---|---|---|
| **BUB1B** | 15q15.1 | MVA1 | Definitive | AR | SAC 激酶 (BUBR1) | ~75% | 眼异常、心脏缺陷、Wilms/rhabdomyosarcoma/ALL |
| **CEP57** | 11q21 | MVA2 | Definitive | AR | 中心体蛋白，微管附着 | 无报告 | 眼异常、心脏缺陷 |
| **TRIP13** | 5p15.33 | MVA3 | Strong | AR | SAC 检查点 | Wilms tumor | café-au-lait 斑、小头、癫痫 |
| **CENATAC** | 11q23.3 | MVA4 | ? | AR | 次要剪接体 (U12) | — | compound het 已报道 |
| **MAD1L1** | 7p22.3 | MVA7 | — | AR | SAC 检查点 | 肿瘤倾向 | 炎症、café-au-lait 斑 |
| **MAD2L1BP** | — | — | — | AR | p31comet, SAC 沉默 | 颗粒细胞瘤 | 癫痫性脑病、小头 |
| **CEP192** | — | — | — | AR | 中心体 | — | — |
| **BUB1** | — | — | Supportive | AD/AR | SAC 激酶 | 结直肠癌倾向 | — |
| **BUB3** | — | — | Supportive | AD | SAC 检查点 | — | — |

### 关键判断
- **BUB1B 和 CEP57 是最成熟的两个**（Definitive），文献最多，应最优先检查。
- **TRIP13** 第三（Strong），有 Wilms tumor 关联。
- 约**一半 MVA 患者有已知基因突变**，另一半可能在新基因里 → 不能只看已知基因。
- 突变类型以**loss-of-function**为主（nonsense, frameshift, splice-site, 大缺失）。

---

## 3. MVA 临床表型 → HPO 映射

### 非常频繁 (80-99%)
| HPO ID | Term |
|---|---|
| HP:0000286 | Epicanthus (内眦赘皮) |
| HP:0000347 | Micrognathia (小颌畸形) |
| HP:0000501 | Glaucoma (青光眼) |
| HP:0000518 | Cataract (白内障) |
| HP:0000568 | Microphthalmia (小眼畸形) |
| HP:0001305 | Dandy-Walker malformation |
| HP:0001541 | Ascites (腹水) |
| HP:0001561 | Polyhydramnios (羊水过多) |
| HP:0002119 | Ventriculomegaly (脑室扩大) |
| HP:0003560 | Muscular dystrophy (肌营养不良) |
| HP:0004322 | Short stature (矮小) |
| HP:0007957 | Corneal opacity (角膜混浊) |
| HP:0010880 | Increased nuchal translucency (颈项透明层增厚) |

### 频繁 (30-79%)
| HPO ID | Term |
|---|---|
| HP:0000252 | Microcephaly (小头畸形) |
| HP:0000325 | Triangular face (三角脸) |
| HP:0000478 | Abnormality of the eye |
| HP:0000504 | Abnormality of vision |
| HP:0001249 | Intellectual disability (智力障碍) |
| HP:0001263 | Global developmental delay (全面发育迟缓) |

### 偶发 (5-29%) — 含癌症
| HPO ID | Term |
|---|---|
| HP:0002667 | Nephroblastoma (Wilms tumor) |
| HP:0002859 | Rhabdomyosarcoma |
| HP:0006721 | Acute lymphoblastic leukemia |
| HP:0007565 | Multiple café-au-lait spots |
| HP:0001250 | Seizure |
| HP:0001252 | Hypotonia |
| HP:0001511 | Intrauterine growth retardation |
| HP:0001631 | Atrial septal defect |
| HP:0001680 | Coarctation of aorta |

---

## 4. 亚型-表型关联（用于从患者 HPO 反推候选基因）

| 如果患者有... | 优先考虑... | 理由 |
|---|---|---|
| Wilms tumor + café-au-lait | **TRIP13** | MVA3 特征性关联 |
| 高癌症风险（rhabdomyosarcoma/ALL/Wilms）| **BUB1B** | ~75% 癌症率 |
| 眼异常 + 心脏缺陷，无癌症 | **CEP57** | MVA2 无癌症报告 |
| 癫痫性脑病 + 颗粒细胞瘤 | **MAD2L1BP** | 特征性 |
| 炎症 + café-au-lait | **MAD1L1** | MVA7 特征 |
| Dandy-Walker + 严重发育迟缓 | BUB1B / CEP57 | 经典 MVA 表现 |

---

## 5. Track 1 策略推导

### 5.1 从 evaluation.py 得知的关键信息
- 答案是 **compound-heterozygous（2 个变异）** → 常隐，同基因双杂合。
- 评分：top-1 full match = 100 分；partial match（命中一个）= 半分。
- F-max 奖励 precision → **少而准**，不要堆噪声。

### 5.2 Pipeline 策略
1. **已知基因优先**：先在 9 个 MVA 基因里找 biallelic 变异。
2. **LoF 优先**：nonsense, frameshift, canonical splice-site, start-loss。
3. **compound-het 检测**：同基因 ≥2 个杂合变异，且 phased trans（如果有父母数据）。
   - 本数据集是 single-subject（无父母），所以只能靠"同基因双杂合"启发式。
4. **HPO 驱动排序**：用患者的 HPO terms 匹配亚型特征 → 调整基因优先级。
5. **新基因候选**：若已知基因无 biallelic LoF，扩展到 SAC/有丝分裂/着丝粒相关基因。
6. **ACMG 评级**：用 VEP/ANNOVAR 注释，参考 ClinVar。

### 5.3 提交策略
- **Row 1**：最可能的 compound-het pair（基因 + 2 个变异坐标），EPCR 最高。
- **Row 2-5**：其他候选 compound-het pair 或单变异。
- **Row 6-10**：secondary findings（如果有临床意义的附带发现）。
- EPCR 分配：top candidate 0.9+，其余递减，保持排序清晰。
- **不要凑满 10 行**——F-max 奖励 precision，少而准优于多而杂。

---

## 6. 扩展候选基因池（若已知基因无果）

SAC / 有丝分裂 / 着丝粒相关基因（机制相邻）：
- BUB1, BUB3（已有 Supportive 证据）
- MAD2 (MAD2L1)
- CDC20
- NDC80 复合体成员
- KNL1
- ZW10, ZWILCH, ROD (RZZ 复合体)
- SKA 复合体
- 中心体：PCNT, CEP63, CEP152, CEP215 (CDK5RAP2)
- 凝缩蛋白：SMC2, SMC4, NCAPD2, NCAPG, NCAPH
- 分离酶/Securin：ESPL1, PTTG1
- Cohesin：STAG1, STAG2, RAD21, SMC1A, SMC3
- 微管相关：TUBG1, TUBG2, TUBB, TUBA1A

---

## 7. 待补充

- [ ] 患者的实际 HPO terms（从 Challenge_Clinical_Phenotype_1.docx 摘录）
- [ ] 患者是否有癌症史（影响 BUB1B vs CEP57 判断）
- [ ] VCF 的变异调用质量/覆盖度（需在服务器上检查）
- [ ] 是否有父母数据（本数据集似乎是 single-subject，无 trio）
