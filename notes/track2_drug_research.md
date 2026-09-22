# Track 2 文献调研笔记 — BUB1B 药物再利用

> 2026-09-23。全部是公开文献/数据库信息，不含患者基因组数据。

## 1. 我们的变异

| | Allele 1 | Allele 2 |
|---|---|---|
| 变异 | chr15:40209701 T>G | chr15:40220612 T>G |
| 蛋白 | p.Leu737* (stop_gained) | p.Asn1002Lys (missense) |
| 终止密码子 | **UGA**（TTA→TGA，+4 位 = A） | — |
| 机制 | PTC → NMD → BUBR1 缺失 | pseudokinase domain 不稳定（推测） |
| 证据 | ClinVar pathogenic | SIFT 0.01 / PolyPhen 0.997 |

## 2. 关键机制证据

### 2.1 NMD 是主要失效机制（不是蛋白不稳定）

Cancer Research 2010 (Suijkerbuijk et al., PMID 20530523)：
- MVA 患者细胞中检测不到 BUBR1 截断蛋白（386X, 731X, 753X）
- 原因：**mRNA 被 NMD 降解**，不是蛋白不稳定
- 质粒表达绕过 NMD → **731X 表达量 ≥ 野生型，蛋白"极其稳定"**
- BUBR1 731X 保留 N 端 450aa 的 APC/C 抑制功能

**我们的 737X 与文献 731X 几乎同位置 → 预期同样稳定。**

### 2.2 剂量敏感性（阈值效应）

AJMG 2007 (Matsuura et al.)：
- >50% BUBR1 表达下降即可导致 PCS/MVA 表型
- 杂合携带者（父母）有轻微有丝分裂缺陷但无症状 → **部分恢复可能跨过阈值**

### 2.3 Pseudokinase domain 错义突变 → 蛋白不稳定

MVA 患者中 R727C、R814H、L844F、**L1012P** 均导致蛋白不稳定。
我们的 N1002K 紧邻 L1012P → 高度可能也是不稳定机制。

## 3. 药物候选

### 3.1 主候选：Ataluren (Translarna, PTC124)

| 属性 | 内容 |
|---|---|
| 机制 | 竞争性抑制 release factor 复合物 → 核糖体 readthrough PTC |
| 批准 | EMA 条件批准（nmDMD，2014）；FDA 未批准 |
| 安全性 | 临床试验一致低毒性；儿童使用数据存在（DMD 2-5 岁） |
| 对 UGA 的效果 | 插入 Trp/Arg/Cys — UGA 是响应最好的终止子类型 |
| 局限 | 疗效不一致（CF III 期失败）；readthrough 效率依 PTC 上下文 |
| 关键文献 | Roy et al. PNAS 2016; Welch et al. Nature 2007; NAR 2025 gkaf216 |

**对我们变异的适用性**：
- UGA-A 上下文 → readthrough 偏好较好
- 恢复全长蛋白（737 位替换为 W/R/C）或至少增加 PTC-mRNA 翻译
- 即使部分恢复，因阈值效应可能临床获益

### 3.2 次候选：Amlexanox

| 属性 | 内容 |
|---|---|
| 机制 | **双重作用**：NMD 抑制 + PTC readthrough（核糖体 A 位点模拟 aminoacyl-tRNA） |
| 批准历史 | 日本 1987 批准（哮喘/口腔溃疡）；2019 商业原因退市（非安全性） |
| 证据 | RDEB 患者细胞：8/12 PTC 响应，部分恢复 >50% 正常水平；WOREE 综合征 N=1 试验改善 |
| 优势 | 穿过血脑屏障；数十年低副作用记录 |
| 局限 | 目前无厂商供应（Fortuity Pharma 在推进复产）；疗效依基因型 |

**协同潜力**：NMD 抑制增加 PTC-mRNA 可用量 + ataluren 促进 readthrough = 理论上协同。
NAR 2025 (gkaf216) 提出 ataluren + G418 联合的正交机制组合思路。

### 3.3 其他（按可行性排序）

| 药物/方向 | 机制 | 可行性 |
|---|---|---|
| ELX-02 | 氨基糖苷衍生物，readthrough，毒性低于 G418 | 临床 II 期（CF），未批准 |
| eRF1/eRF3a 抑制剂（CC-90009, SRI-41315） | 降解终止因子 | 抗癌药开发中，对 MVA 患者风险高 |
| ACE-tRNA | 反密码子编辑 tRNA 抑制 PTC | 前沿实验，非药物 |
| 化学伴侣（4-PBA, TUDCA） | 稳定不稳定蛋白 | 对 Allele 2 推测性强 |
| **排除**：促增殖/检查点抑制剂 | — | MVA 癌症易感，禁忌 |

## 4. 风险与局限（报告必须写）

1. readthrough 效率 10-25% 典型值，变异个体差异大
2. 737X 截断蛋白缺 pseudokinase domain + kinetochore binding → 仅部分功能
3. 患者已有癌症（rhabdomyosarcoma）——药物目标是减少新发非整倍体负担，不是治癌
4. amlexanox 目前无上市供应渠道
5. 儿童 MVA 无先例用药数据，需 compassionate use / N=1 框架

## 5. 推荐报告结构

主候选 ataluren（机制最清楚、有儿童数据）+ 次候选 amlexanox（NMD 抑制协同）。
强调剂量阈值效应：不需要完全恢复，部分恢复即可跨过致病阈值。
