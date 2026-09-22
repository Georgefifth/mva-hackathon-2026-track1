# AGENTS.md — MVA Hackathon 2026, Track 1

本项目参加 SageBio "Rare Disease, Real Kid: MVA Hackathon 2026" 的 **Track 1（变异预测）**。
数据是一个真实患有 Mosaic Variegated Aneuploidy（MVA）的孩子的全基因组，受保密协议约束。

> 这份文件是 Devin 在本项目里的行为准则。每次开工前先读它。

---

## 0. 一句话红线

**原始基因组数据永远不进对话。** 我（Devin）是云后端驱动的 agent，
任何让我 `read` / 粘贴 / 处理的内容都会发到后端模型 provider。
VCF 行、FASTQ、全基因组基因型表 = 受保护数据，禁止进入对话。
我只碰**衍生发现**和**代码**。

---

## 1. 比赛背景速查

- **Track 1 目标**：从孩子的基因组（VCF/FASTQ）+ 临床表型（HPO）预测致病变异。
- **答案结构**：临床确认的致病变异，evaluation.py 表明是 **compound-heterozygous（2 个变异）**
  或单变异。评分对 compound-het 给半分（命中其中一个）。
- **proband_id**：`PROBAND01`（提交 CSV 里唯一接受的 ID）。
- **提交**：CSV，最多 10 行候选，按 EPCR（自估致病概率）排序。
- **评分**：
  - Rank points：top-1=100, top-3=50, top-5=25, top-10=10；compound-het 命中一个 = 半分。
  - F-max：在所有 EPCR 阈值上取最佳 F-measure（个体变异层面，不是行层面）。
- **提交次数**：6 次，取最高分。还附 GitHub 链接 + methods 报告（PDF/MD）。
- **时间线**：提交期 2026-08-24 ~ 2026-10-24。
- **提交 CSV 字段**：`proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes`
  - 坐标必须 **GRCh38**。
  - `finding_type`：`primary` 或 `secondary`（不影响自动评分，但 secondary 不会扣分）。
  - `epcr` ∈ (0, 1]。

---

## 2. 数据资产（在用户本地，我不直接碰）

数据集 `SageBio/mva-hackathon-2026-data`，~85GB，11 个文件：

| 文件 | 大小 | 性质 |
|---|---|---|
| `WGS_EX2312012_HGWCNDSX7.vcf.gz` | 315 MB | **受保护** — 变异调用结果 |
| `WGS_EX2312012_HGWCNDSX7.vcf.gz.tbi` | 2.3 MB | 索引 |
| `WGS_..._S16_L00{1-4}_R{1,2}_001.fastq.gz` ×8 | ~10.5GB 每个 | **受保护** — 原始测序 reads |
| `Challenge_Clinical_Phenotype_1.docx` | 17 KB | 临床表型描述（含 HPO terms） |

**存储建议**：本地至少 100–150 GB（含中间文件）。
**下载方式**：用户用 `hf download`（gated dataset，需先在 HF 页面同意条款）。

---

## 3. 隐私合规边界（最重要）

### 3.1 官方 Processor vs Recipient 测试（来自讨论 #2，Sage 隐私官 cfsuver）

- **Processor（工具）= 允许**：服务只为返回结果而处理数据，不取得权利，不能自用。
- **Recipient（接收方）= 禁止**：服务有权使用/留存/学习数据。发给它 = 泄漏。

用第三方 LLM API 允许，前提：
1. provider 不在输入/输出上训练，不取得权利；
2. 留存有限且限于特定目的（短期日志 OK，不能用于其他目的）。

**坑**：credit/grant 计划可能附带覆盖账户默认设置的条款 → 奖品的 Claude credits 要单独读条款。

### 3.2 我（Devin）的边界

| 类别 | 能否进对话 | 说明 |
|---|---|---|
| VCF 文件 / VCF 行 / 变异坐标+基因型 | **否** | 受保护，发到后端 = release |
| FASTQ / reads | **否** | 同上 |
| 全基因组基因型表、注释后的变异表 | **否** | "能重建基因组有意义部分"的中间产物 |
| 含变异块的 prompt/log | **否** | 删除义务范围内 |
| **HPO terms 列表** | 是 | 衍生发现，官方明确 KEEP |
| **候选基因排名、机制分析** | 是 | 衍生发现 |
| **代码 / 脚本 / pipeline** | 是 | 不含原始数据 |
| **报告 / 方法描述** | 是 | 不含受保护数据 |
| **文献检索、通路分析、药物候选** | 是 | 公共知识 |

**原则**：用户在本地跑 pipeline，产出衍生发现（基因名、HPO、排名），
把衍生发现带进对话让我分析。原始数据永不进对话。

### 3.3 30 天删除义务（用户负责，我提醒）

**删除**：VCF/BAM/CRAM 及副本/切片/索引、全基因组基因型表、含变异块的本地 prompt/log、
在原始基因组数据上训练的权重。
**保留**：候选变异列表（=提交物）、HPO、基因排名、代码、报告。

### 3.4 LLM 使用声明（必须做）

methods 报告里必须记录一行，例如：
> "Devin (Cognition), GLM-5.2 High, [plan/tier], [data-handling setting]"

→ 用户需先核实 Devin/Cognition 的数据条款是否满足 Processor 测试，再决定带多少内容进对话。

---

## 4. Track 1 工作流（合规骨架）

```
[用户本地]                          [对话里 — 我能帮的]
原始数据 (VCF/FASTQ)
    │
    ▼
本地 pipeline（我写脚本，用户跑）
    │  - QC / 过滤
    │  - 注释 (VEP/ANNOVAR/SnpEff)
    │  - 按 HPO 表型优先排序
    │  - recessive/compound-het 模型
    │  - 排名 → EPCR
    ▼
衍生发现（基因名、HPO、候选变异排名）──→  带进对话
                                        │
                                        ▼
                                  我做：文献检索、
                                  机制分析、排名优化、
                                  写报告、生成提交 CSV 模板
                                        │
                                        ▼
                                  用户填坐标 → 本地验证 → 提交
```

### 4.1 我能贡献的具体工作
1. **写 pipeline 脚本**：bcftools/htslib/VEP/Python，用户本地跑。
2. **HPO 驱动的基因优先排序**：把临床表型映射到 HPO → 关联基因 → 在候选里排序。
3. **MVA 文献/机制研究**：MVA 已知致病基因（BUB1B, CEP57, TRIO, ...）、
   mosaic variegated aneuploidy 的遗传机制（常隐，多数 biallelic）。
4. **compound-het 检测逻辑**：在 VCF 里找同基因双杂合变异的脚本。
5. **EPCR 排序策略**：怎么把多证据（ACMG 评级、HPO 匹配、基因相关性）合成排名。
6. **生成提交 CSV 模板**：用户填坐标，我帮校验格式。
7. **写 methods 报告**：含 LLM 使用声明。

### 4.2 用户负责
- 下载/存储数据、本地跑 pipeline、填变异坐标、提交、30 天删除确认。

---

## 5. 提交清单（Track 1）

- [ ] 预测 CSV（≤10 行，GRCh38，含 epcr/finding_type）
- [ ] GitHub repo（hackathon 期间可私有，结束时公开）
- [ ] methods 报告（PDF/MD，用官方模板，含 LLM 使用声明）
- [ ] 文件名含 username/team name，如 `yap_mva-rank-v1.csv`

---

## 6. 评分细节备忘（来自 evaluation.py）

- 行按 epcr 降序排序后赋 rank（不要求提交时预排序，但会警告）。
- full match = 一行的 variants frozenset 完全等于 true_variants。
- compound-het：若没 full match，找含其中一个 true variant 的行 → partial match → 半分。
- F-max：把每行展开成个体 variant，在每个 epcr 阈值上算 precision/recall，取最大 F。
  → **意味着 secondary findings 不会拉低 F-max**（它们只增加 FP，但 F-max 取的是最佳阈值）。
- 策略含义：**top-1 放最可能的 compound-het pair，其余放有依据的候选**；
  宁可少而准（F-max 奖励 precision），不要堆噪声。

---

## 7. 工作目录约定

```
/home/yap/Hack/Disease/
├── AGENTS.md            # 本文件
├── pipeline/            # 我写的脚本（用户本地跑）
├── analysis/            # 衍生发现、分析笔记（无原始数据）
├── submission/          # 提交 CSV、报告草稿
└── notes/               # 文献、机制研究
```

**禁止**：把 `data/`（原始数据目录）放进本工作目录让我读取。

---

## 8. 已确认事项（2026-09-01）

### 提交准备状态
- [x] 预测 CSV: `submission/georgefifth_bub1b-compound-het-v1.csv`（3 行）
- [x] Methods 报告: `submission/georgefifth_track1_report.md`
- [x] GitHub repo: https://github.com/Georgefifth/mva-hackathon-2026-track1（私有，结束后公开）
- [x] LLM 使用声明: 已写入 methods 报告第 7 节
- [x] 受保护数据已从 git 历史清除（VCF/docx/TSV）

### Devin/Cognition 条款核实结果（2026-09-01）
- Cognition 默认可能用数据训练模型；付费计划可 opt-out 并启用 Zero Data Retention
- **采取的合规措施**：原始基因组数据（VCF/FASTQ/基因型）从未进入 Devin 对话
- 只处理了衍生发现（基因名、HPO、注释结果、文献）和代码
- Ensembl VEP REST API 作为 Processor 使用（只发坐标，不发样本信息）
- methods 报告第 7 节如实记录了以上信息

---

## 9. Track 2 — 药物再利用（进行中）

### 9.1 目标与交付物

基于 Track 1 找到的致病变异机制，提出**已批准药物**的再利用候选。

| 交付物 | 状态 |
|---|---|
| 报告（PDF/MD，用官方 methods 模板） | 进行中 |
| GitHub repo 补充 Track 2 分析 | 复用现有 repo |
| 3 分钟 pitch 视频（YouTube/Vimeo） | **暂缓** — 用户自行决定 |

- 评分：专家评委 — 科学严谨 35% / 潜在影响 25% / 创新 25% / 可扩展 15%
- 提交次数：3 次，只评最新一次
- 评审周期：~2-3 个月

### 9.2 机制假设（来自 Track 1 结论）

- **变异**：BUB1B compound-het — `chr15:40209701 T>G` p.Leu737*（stop_gained, ClinVar pathogenic）+ `chr15:40220612 T>G` p.Asn1002Lys（missense, SIFT deleterious / PolyPhen probably_damaging）
- **机制链**：PTC（提前终止密码子）→ nonsense-mediated decay (NMD) → BUBR1 蛋白缺失 → 纺锤体组装检查点 (SAC) 缺陷 → 染色体错误分离 → 非整倍体
- missense allele 可能产生部分功能蛋白（未证实）

### 9.3 药物方向（待调研验证）

| 方向 | 机制 | 状态 |
|---|---|---|
| **主方向：无义突变 readthrough** | ataluren (Translarna/PTC124) 促进核糖体 readthrough PTC → 恢复部分 BUBR1 | 待验证 |
| 备选 | amlexanox（NMD 抑制+readthrough）、氨基糖苷类（G418/gentamicin，毒性大仅讨论） | 待验证 |
| **排除** | 促进增殖/抑制检查点的药物（MVA 患者癌症易感，反效果风险） | 已排除 |

**关键风险（必须在报告里如实写）**：
- readthrough 效率通常只有 10-25%
- 截断位点在 737/1050 aa —— 恢复的蛋白量能否挽救 SAC 功能是开放问题
- BUBR1 是大蛋白，readthrough 后蛋白是否折叠/定位正常未知
- missense allele (p.Asn1002Lys) 不是 PTC，readthrough 药物对它无效——最多只救一半基因剂量

### 9.4 工作流

1. **文献调研**：MVA/BUB1B/BUBR1 + NMD + readthrough 药物 + 非整倍体耐受机制（PubMed/Europe PMC API）
2. **药物数据库**：DGIdb、Open Targets、ChEMBL 查 BUB1B 相关药物（公开 API = Processor，合规）
3. **机制论证**：LoF 机制 → 药物如何干预 → 预期效果 → 局限性（评委最看重 Scientific Rigor）
4. **报告**：用 `static/templates/methods_description_form.xlsx` 的结构写 MD
5. **repo**：补 Track 2 分析脚本（drug-gene 查询、文献检索脚本）

### 9.5 Track 2 隐私边界（同 Track 1）

- **不需要再碰原始基因组数据** —— Track 2 只用变异结论（findings，可保留）+ 公共知识
- 药物数据库/文献 API 全是公开查询工具 = Processor
- 对话里可以讨论：变异机制、药物候选、文献结论
- 不讨论：基因组级数据、其他变异坐标表

- [x] HF 账号已获批数据集访问权限。
- [x] 本地资源：用户**有自己的服务器**，能跑 pipeline。
      ⚠️ **服务器上有其他项目——操作时必须小心，不得扰乱既有项目。**
      原则：只在指定工作目录下操作；不碰其他目录；不装会冲突的系统级依赖
      （用 conda/venv/docker 隔离）；改任何系统配置前先问。
- [ ] **Devin/Cognition 数据条款尚未核实** → 当前采取保守模式：
      只带公开知识 + 明确安全的衍生发现（基因名、HPO、排名）进对话；
      任何边界模糊的内容，用户本地处理。核实条款后再放宽。
- [x] 单独参赛。team name = 用户的 HF username。
