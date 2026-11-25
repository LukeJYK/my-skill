---
title: Skill comparison
created: 2026-11-21
updated: 2026-11-24
tags: [skills, inventory]
---

# Skill comparison

对比对象：
- **参考表**：上游 vault 的 `build.py`，22 个领域，`CATEGORIES` 里共 417 个技能
- **已安装**：`skills/`，共 657 个
- **我的分类**：[`.skill-vault/build-vault.py`](../.skill-vault/build-vault.py)，14 个领域：去掉了参考表的 8 个生物领域和 analytics-engineering（只装了 1 个，`observability-and-instrumentation` 并入 software-dev），新增 Scientific Expert Profiles

上一版（2026-11-21，对比 `LukeJYK/skillset` 的 264 个）在 git 历史里。

## 总览

| 类别 | 数量 |
|---|---|
| 参考表 | 417 |
| 已安装（在参考表中） | 145 |
| 已安装但不在参考表中：自己加的 | 8 |
| 已安装但不在参考表中：K-Dense 专家 profile | 504 |
| 未安装 | 272 |
| └ 仍在 `CATEGORIES` 里（待装清单） | 100 |
| └ 已从 `CATEGORIES` 移除：analytics-engineering | 16 |
| └ 已从 `CATEGORIES` 移除：生物相关 | 156 |

仍在 `CATEGORIES` 里的未装技能不影响生成结果：map 只列出已安装的技能。留着它们，以后装上会自动归到对应领域。

## 按领域

| 领域 | 参考表 | 已装 | 未装 | 备注 |
|---|---:|---:|---:|---|
| Genomics, Variants & Population Genetics | 34 | 0 | 34 | 已从 `CATEGORIES` 移除 |
| Single-Cell, RNA-seq & Functional Genomics | 23 | 0 | 23 | 已从 `CATEGORIES` 移除 |
| Proteomics & Metabolomics | 7 | 0 | 7 | 已从 `CATEGORIES` 移除 |
| Drug Discovery, Cheminformatics & Structural Biology | 21 | 0 | 21 | 已从 `CATEGORIES` 移除 |
| Sequence Analysis, NGS & Phylogenetics | 22 | 0 | 22 | 已从 `CATEGORIES` 移除 |
| Bio Databases, Lab & Cloud Platforms | 22 | 0 | 22 | 已从 `CATEGORIES` 移除 |
| Clinical, Medical & Pharmacogenomics | 13 | 0 | 13 | 已从 `CATEGORIES` 移除 |
| Imaging, Microscopy & Biosignals | 13 | 0 | 13 | 已从 `CATEGORIES` 移除 |
| Machine Learning & AI | 13 | 11 | 2 |  |
| Data Science, Stats & Scientific Computing | 31 | 18 | 13 | 另有本地新增 `statistical-power`, `uncertainty-and-units` |
| Quantum, Physics & Materials | 7 | 4 | 3 | 另有本地新增 `pybamm` |
| Scientific Writing, Figures & Publishing | 20 | 19 | 1 | 另有本地新增 `rebuttal-guidance` |
| Academic Paper & Nature Pipelines | 14 | 14 | 0 |  |
| Literature Search & Knowledge Discovery | 14 | 6 | 8 |  |
| Documents, Office & Media | 11 | 6 | 5 |  |
| Cloud, Infra & MLOps | 15 | 11 | 4 | 另有本地新增 `docker-expert`, `kubernetes-specialist` |
| Software Development & Engineering | 35 | 29 | 6 | 另有本地新增 `constraint-driven-development`, `pi-agent`；另从 analytics-engineering 移入 `observability-and-instrumentation` |
| Vault, Skills & Workflow Meta | 13 | 5 | 8 | 去掉了 `bio-orchestrator` |
| Reasoning, Ideation & Decision | 10 | 9 | 1 |  |
| Web Automation, Frontend & Design | 26 | 7 | 19 |  |
| Analytics Engineering & LLM Operations | 17 | 1 | 16 | 已从 `CATEGORIES` 移除；`observability-and-instrumentation` 并入 software-dev |
| Security & Auditing | 36 | 5 | 31 |  |
| [Scientific Expert Profiles](maps/scientific-expert-profiles.md) | — | 504 | — | 不在参考表；按 SKILL.md metadata 自动归类 |

## 安装建议

不全装：每个已装技能的名字和描述每次会话都会加载；功能重叠会让 Claude 选错技能；主流库用技能帮助不大。

- **已装**：`defuddle`（2026-11-24，来自 `obsidianmd/obsidian-skills`）。它要用 `defuddle` 命令行，先运行 `npm install -g defuddle`。
- **推荐**：`obsidian-markdown`、`obsidian-bases`，和 defuddle 来自同一个仓库：
  ```bash
  npx skills add kepano/obsidian-skills -s obsidian-markdown -g -a universal -y
  npx skills add kepano/obsidian-skills -s obsidian-bases -g -a universal -y
  ```
- **视需要**：`pymatgen`（材料方向）；DuckDB 的 `query`、`read-file`；`xarray`。
- **已移除**：dbt 和 LLM 可观测性那 16 个连同 analytics-engineering 领域一起删了，以后要装得先加回 `CATEGORIES`。
- **不装**：`paper-2-web`。K-Dense 在 2026-04-02 删了它，skills.sh 上只剩第三方副本。要用的话，从 K-Dense 删除前的提交 `c61a6a2` 拿官方最后一版放进 `skills/paper-2-web/`，当本地技能。
- 其余等真遇到对应任务再装，安装命令见 [README](../README.md)。
- **K-Dense 专家 profile**：504 个已导入（见下文）。它们的名字和描述每次会话都会加载，约 4.8 万 token；不想要了，删掉 `skills/` 里带 `scientific-agents-profile: true` 的文件夹，再跑 `build-vault.py --prune`。

## ❌ 未安装：仍在 CATEGORIES 里

共 100 个，是待装清单：装上后会自动归到对应领域。“上游仓库”是 2026-11-24 在 GitHub 上查到的；“未查到”只是不在我查过的几个仓库里，不代表不存在。

### Machine Learning & AI（2）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `pufferlib-v2` | 未查到 | 跳过：已有 pufferlib |
| `pufferlib-v3` | 未查到 | 跳过：已有 pufferlib |

### Data Science, Stats & Scientific Computing（13）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `matlab` | `K-Dense-AI/scientific-agent-skills` | 跳过：小众工具 |
| `scikit-survival` | `K-Dense-AI/scientific-agent-skills` | 跳过：小众工具 |
| `usfiscaldata` | `K-Dense-AI/scientific-agent-skills` | 跳过：小众工具 |
| `xarray` | 未查到 | 视需要：处理多维数组数据时再装 |
| `pandera-validation` | 未查到 | 跳过：用不到 |
| `xarray-pandera-duckdb` | 未查到 | 跳过：和 xarray/DuckDB 重复 |
| `attach-db` | 未查到 | 跳过：DuckDB 有 query/read-file 就够 |
| `duckdb-docs` | 未查到 | 跳过：DuckDB 有 query/read-file 就够 |
| `install-duckdb` | 未查到 | 跳过：DuckDB 有 query/read-file 就够 |
| `query` | 未查到 | 视需要：用 DuckDB 时装这个 |
| `read-file` | 未查到 | 视需要：用 DuckDB 时装这个 |
| `paraview` | 未查到 | 跳过：小众工具 |
| `ttk-viz` | 未查到 | 跳过：小众工具 |

### Quantum, Physics & Materials（3）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `astropy` | `K-Dense-AI/scientific-agent-skills` | 跳过：不做天文 |
| `fluidsim` | `K-Dense-AI/scientific-agent-skills` | 跳过：小众 |
| `pymatgen` | `K-Dense-AI/scientific-agent-skills` | 视需要：做材料方向再装（你有 pybamm） |

### Scientific Writing, Figures & Publishing（1）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `paper-2-web` | ⚠️ 上游已删除（K-Dense，2026-04-02） | 不装：上游删了；第三方副本不用，要做主页直接让 Claude 做 |

### Literature Search & Knowledge Discovery（8）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `pubmed-summariser` | 未查到 | 跳过：偏生物医学；检索技能已够 |
| `lit-synthesizer` | 未查到 | 跳过：已有 6 个检索技能，重复 |
| `bgpt-mcp` | 未查到 | 跳过：已有 6 个检索技能，重复 |
| `bgpt-paper-search` | `K-Dense-AI/scientific-agent-skills` | 跳过：已有 6 个检索技能，重复 |
| `paperzilla` | `K-Dense-AI/scientific-agent-skills` | 跳过：已有 6 个检索技能，重复 |
| `open-notebook` | `K-Dense-AI/scientific-agent-skills` | 跳过：已有 6 个检索技能，重复 |
| `data-extractor` | 未查到 | 跳过：已有 6 个检索技能，重复 |
| `claw-semantic-sim` | 未查到 | 跳过：已有 6 个检索技能，重复 |

### Documents, Office & Media（5）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `liteparse` | `K-Dense-AI/scientific-agent-skills` | 跳过：偏商业/办公 |
| `infographics` | `K-Dense-AI/scientific-agent-skills` | 跳过：偏商业/办公 |
| `market-research-reports` | `K-Dense-AI/scientific-agent-skills` | 跳过：偏商业/办公 |
| `doc-coauthoring` | `anthropics/skills` | 跳过：偏商业/办公 |
| `internal-comms` | `anthropics/skills` | 跳过：偏商业/办公 |

### Cloud, Infra & MLOps（4）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `nextflow` | `K-Dense-AI/scientific-agent-skills` | 跳过：偏生物信息 |
| `snakemake-workflow-engine` | 未查到 | 跳过：偏生物信息 |
| `e2b-sandbox` | 未查到 | 跳过：已有 modal |
| `conda-bioconda` | 未查到 | 跳过：偏生物信息 |

### Software Development & Engineering（6）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `pytest` | 未查到 | 跳过：主流库，Claude 本来就熟 |
| `docker` | 未查到 | 跳过：主流工具，Claude 本来就熟 |
| `fastapi` | 未查到 | 跳过：主流库，Claude 本来就熟 |
| `github-actions-ci` | 未查到 | 跳过：和 ci-cd-and-automation 重复 |
| `check-pr` | 未查到 | 跳过：绑定 Greptile |
| `greploop` | 未查到 | 跳过：绑定 Greptile |

### Vault, Skills & Workflow Meta（7）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `obsidian-markdown` | `obsidianmd/obsidian-skills` | ⭐ 推荐：你在维护这个 Obsidian vault |
| `obsidian-bases` | `obsidianmd/obsidian-skills` | ⭐ 推荐：`vault/skills.base` 就是 Bases |
| `obsidian-cli` | `obsidianmd/obsidian-skills` | 视需要：用 Obsidian 命令行时再装 |
| `json-canvas` | `obsidianmd/obsidian-skills` | 视需要：画 `.canvas` 时再装 |
| `skill-builder` | 未查到 | 跳过：已有 writing-skills |
| `clawpathy-autoresearch` | 未查到 | 跳过：用不到 |
| `repro-enforcer` | 未查到 | 跳过：用不到 |

### Reasoning, Ideation & Decision（1）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `dhdna-profiler` | `K-Dense-AI/scientific-agent-skills` | 跳过：用不到 |

### Web Automation, Frontend & Design（19）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `agentcore` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `core` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `dogfood` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `electron` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `slack` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `vercel-sandbox` | `vercel-labs/agent-browser` | 跳过：做前端产品才需要；已有 frontend-design |
| `playwright-cli` | 未查到 | 跳过：和 webapp-testing / playwright-best-practices / agent-browser 重复 |
| `web-design-guidelines` | `vercel-labs/agent-skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `vercel-composition-patterns` | `vercel-labs/agent-skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `vercel-react-best-practices` | `vercel-labs/agent-skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `vercel-react-view-transitions` | `vercel-labs/agent-skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `figma-use` | 未查到 | 跳过：做前端产品才需要；已有 frontend-design |
| `figma-generate-design` | 未查到 | 跳过：做前端产品才需要；已有 frontend-design |
| `figma-generate-library` | 未查到 | 跳过：做前端产品才需要；已有 frontend-design |
| `figma-implement-design` | 未查到 | 跳过：做前端产品才需要；已有 frontend-design |
| `web-artifacts-builder` | `anthropics/skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `brand-guidelines` | `anthropics/skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `theme-factory` | `anthropics/skills` | 跳过：做前端产品才需要；已有 frontend-design |
| `algorithmic-art` | `anthropics/skills` | 跳过：做前端产品才需要；已有 frontend-design |

### Security & Auditing（31）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `llm-agent-security-redteam` | 未查到 | 跳过：专业审计方向；已有 security-and-hardening |
| `audit-context-building` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `audit-prep-assistant` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `code-maturity-assessor` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `secure-workflow-guide` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `differential-review` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `codeql` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `sarif-parsing` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `semgrep` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `semgrep-rule-creator` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `c-review` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `constant-time-analysis` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `constant-time-testing` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `harness-writing` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `coverage-analysis` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `fuzzing-dictionary` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `fuzzing-obstacles` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `libfuzzer` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `cargo-fuzz` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `atheris` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `ossfuzz` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `aflpp` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `supply-chain-risk-auditor` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `insecure-defaults` | 未查到 | 跳过：专业审计方向；已有 security-and-hardening |
| `sharp-edges` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `variant-analysis` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `fp-check` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `guidelines-advisor` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `entry-point-analyzer` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `token-integration-analyzer` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |
| `spec-to-code-compliance` | `trailofbits/skills` | 跳过：专业审计方向；已有 security-and-hardening |

## ❌ 未安装：已从 CATEGORIES 移除

共 172 个。不打算装；以后要装，先把它加回 `CATEGORIES`，否则会进“未分类”。

### Analytics Engineering & LLM Operations（16）

| Skill | 上游仓库 | 建议 |
|---|---|---|
| `adding-dbt-unit-test` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `answering-natural-language-questions-with-dbt` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `building-dbt-semantic-layer` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `configuring-dbt-mcp-server` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `creating-mermaid-dbt-dag` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `fetching-dbt-docs` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `running-dbt-commands` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `troubleshooting-dbt-job-errors` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `using-dbt-for-analytics-engineering` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `working-with-dbt-mesh` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `migrating-dbt-core-to-fusion` | 未查到 | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `migrating-dbt-project-across-platforms` | `dbt-labs/dbt-agent-skills` | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `langfuse` | 未查到 | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `phoenix-cli` | 未查到 | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `phoenix-evals` | 未查到 | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |
| `llm-observability-evals` | 未查到 | 跳过：dbt 数据仓库 / LLM 应用运维才需要（已移除这个领域） |

### 生物相关（156）

参考表 8 个生物领域的全部技能，加上 vault-meta 里的 `bio-orchestrator`。

- **Genomics, Variants & Population Genetics（34）**：`variant-annotation`, `vcf-annotator`, `clinical-variant-reporter`, `gwas-pipeline`, `gwas-lookup`, `gwas-prs`, `gwas-catalog-region-fetch`, `fine-mapping`, `mendelian-randomisation`, `ld-1000g-region-compute`, `eqtl-catalogue-region-fetch`, `ukb-ppp-region-fetch`, `locuscompare-region-render`, `hla-typing`, `archaic-introgression`, `dnasp`, `fastreer`, `tiledbvcf`, `pysam`, `wgs-prs`, `sample-qc-triage`, `equity-scorer`, `claw-ancestry-pca`, `genome-compare`, `genome-match`, `recombinator`, `soul2dna`, `geniml`, `gtars`, `polars-bio`, `nfcore-sarek-wrapper`, `pacsomatic`, `marker-dominance-mapper`, `pybedtools`
- **Single-Cell, RNA-seq & Functional Genomics（23）**：`scanpy`, `anndata`, `scvi-tools`, `scvelo`, `cellxgene-census`, `scrna-embedding`, `scrna-orchestrator`, `nfcore-scrnaseq-wrapper`, `bulk-rnaseq`, `rnaseq-de`, `pydeseq2`, `nfcore-rnaseq-wrapper`, `rare-disease-rnaseq`, `de-summary`, `diff-visualizer`, `arboreto`, `deeptools`, `pathway-enricher`, `pathway-enrichment`, `spatialdata-squidpy`, `harmonypy`, `scirpy-immune-repertoire`, `seurat`
- **Proteomics & Metabolomics（7）**：`proteomics-de`, `proteomics-clock`, `affinity-proteomics`, `pyopenms`, `matchms`, `glycoengineering`, `fragpipe-pyteomics-proteomics`
- **Drug Discovery, Cheminformatics & Structural Biology（21）**：`rdkit`, `datamol`, `deepchem`, `molfeat`, `medchem`, `pytdc`, `torchdrug`, `diffdock`, `struct-predictor`, `esm`, `molecular-dynamics`, `cobrapy`, `rowan`, `adaptyv`, `target-validation-scorer`, `drug-repurposing-screen`, `depmap`, `crispr-screen-triage`, `omics-target-evidence-mapper`, `colabfold`, `vmd-mdanalysis-viz`
- **Sequence Analysis, NGS & Phylogenetics（22）**：`biopython`, `bioservices`, `gget`, `scikit-bio`, `phylogenetics`, `phylogenetics-builder`, `etetoolkit`, `busco-assessor`, `analyze-fasta`, `seq-wrangler`, `multiqc-reporter`, `bioqc-mcp`, `claw-metagenomics`, `ncbi-datasets`, `bioconductor-bridge`, `gi-annotation`, `gi-chromatin`, `gi-enhancer`, `gi-expression`, `gi-promoter`, `gi-splice`, `ngs-cli-toolkit`
- **Bio Databases, Lab & Cloud Platforms（22）**：`database-lookup`, `primekg`, `turingdb-graph`, `clinpgx`, `article-data-fetcher`, `ukb-navigator`, `galaxy-bridge`, `flow-bio`, `dnanexus-integration`, `latchbio-integration`, `benchling-integration`, `labstep`, `labarchive-integration`, `omero-integration`, `lamindb`, `protocols-io`, `protocolsio-integration`, `ginkgo-cloud-lab`, `opentrons-integration`, `pylabrobot`, `illumina-bridge`, `bigquery-public`
- **Clinical, Medical & Pharmacogenomics（13）**：`clinical-reports`, `clinical-decision-support`, `treatment-plans`, `clinical-trial-finder`, `wes-clinical-report-en`, `wes-clinical-report-es`, `pharmgx-reporter`, `nutrigx-advisor`, `drug-photo`, `pyhealth`, `iso-13485-certification`, `profile-report`, `methylation-clock`
- **Imaging, Microscopy & Biosignals（13）**：`cell-detection`, `histolab`, `pathml`, `pydicom`, `neuropixels-analysis`, `flowio`, `neurokit2`, `bids`, `imaging-data-commons`, `cellpose-cell-segmentation`, `cellpose-stardist-bioimage`, `monai-medical-imaging-ai`, `napari-viz`
- **Vault, Skills & Workflow Meta（1）**：`bio-orchestrator`

## ➕ 已安装但不在参考表中

### K-Dense 专家 profile（504）

来自 `K-Dense-AI/scientific-agents`（MIT），pin 在 commit `896ed6e`（2026-06-04），由 [`.skill-vault/import-scientific-agents.py`](../.skill-vault/import-scientific-agents.py) 导入：503 个职业专家 profile，加分发技能 [scientific-agents](notes/scientific-expert-profiles/scientific-agents.md)。全部列在 [Scientific Expert Profiles](maps/scientific-expert-profiles.md)。上游最新版比 pin 新 16 个提交，改过 216 个 profile；要更新就 checkout 新版、改 `PINNED_COMMIT` 后重跑导入。

### 自己加的（8）

| Skill | 领域 | 描述 |
|---|---|---|
| [constraint-driven-development](notes/software-dev/constraint-driven-development.md) | Software Development & Engineering | Establishes a project's quality bar as a written contract and stops agents quietly lowering it |
| [docker-expert](notes/cloud-devops/docker-expert.md) | Cloud, Infra & MLOps | You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns... |
| [kubernetes-specialist](notes/cloud-devops/kubernetes-specialist.md) | Cloud, Infra & MLOps | Use when deploying or managing Kubernetes workloads |
| [pi-agent](notes/software-dev/pi-agent.md) | Software Development & Engineering | Builds with and operates Pi, the minimal terminal coding harness |
| [pybamm](notes/quantum-physics/pybamm.md) | Quantum, Physics & Materials | Simulates lithium-ion battery charge, discharge and rest experiments with PyBaMM, records parameter-set provenance, checks mesh and solver sensitivity, and compares predicted voltage... |
| [rebuttal-guidance](notes/research-writing/rebuttal-guidance.md) | Scientific Writing, Figures & Publishing | Provides actionable peer-review rebuttal guidance (not full rebuttal prose) using conditional persuasion P(Z\|X,Y): match reviewer mindset X, recommend strategy Y, optionally ground in... |
| [statistical-power](notes/data-science-compute/statistical-power.md) | Data Science, Stats & Scientific Computing | Calculates sample sizes and statistical power for study planning |
| [uncertainty-and-units](notes/data-science-compute/uncertainty-and-units.md) | Data Science, Stats & Scientific Computing | Tracks physical units and propagates measurement uncertainty in scientific calculations using pint and uncertainties |

## ✅ 已安装（在参考表中）

共 145 个，描述见各领域 map 或 [Skills Index](index.md)。

- **[Machine Learning & AI](maps/ml-ai.md)（11）**：[aeon](notes/ml-ai/aeon.md), [hugging-science](notes/ml-ai/hugging-science.md), [pufferlib](notes/ml-ai/pufferlib.md), [pytorch-lightning](notes/ml-ai/pytorch-lightning.md), [scikit-learn](notes/ml-ai/scikit-learn.md), [shap](notes/ml-ai/shap.md), [stable-baselines3](notes/ml-ai/stable-baselines3.md), [timesfm-forecasting](notes/ml-ai/timesfm-forecasting.md), [torch-geometric](notes/ml-ai/torch-geometric.md), [transformers](notes/ml-ai/transformers.md), [umap-learn](notes/ml-ai/umap-learn.md)
- **[Data Science, Stats & Scientific Computing](maps/data-science-compute.md)（18）**：[adjusttext](notes/data-science-compute/adjusttext.md), [dask](notes/data-science-compute/dask.md), [exploratory-data-analysis](notes/data-science-compute/exploratory-data-analysis.md), [geomaster](notes/data-science-compute/geomaster.md), [geopandas](notes/data-science-compute/geopandas.md), [matplotlib](notes/data-science-compute/matplotlib.md), [networkx](notes/data-science-compute/networkx.md), [optimize-for-gpu](notes/data-science-compute/optimize-for-gpu.md), [polars](notes/data-science-compute/polars.md), [pymc](notes/data-science-compute/pymc.md), [pymoo](notes/data-science-compute/pymoo.md), [seaborn](notes/data-science-compute/seaborn.md), [simpy](notes/data-science-compute/simpy.md), [statistical-analysis](notes/data-science-compute/statistical-analysis.md), [statsmodels](notes/data-science-compute/statsmodels.md), [sympy](notes/data-science-compute/sympy.md), [vaex](notes/data-science-compute/vaex.md), [zarr-python](notes/data-science-compute/zarr-python.md)
- **[Quantum, Physics & Materials](maps/quantum-physics.md)（4）**：[cirq](notes/quantum-physics/cirq.md), [pennylane](notes/quantum-physics/pennylane.md), [qiskit](notes/quantum-physics/qiskit.md), [qutip](notes/quantum-physics/qutip.md)
- **[Scientific Writing, Figures & Publishing](maps/research-writing.md)（19）**：[benchmark-paper-template](notes/research-writing/benchmark-paper-template.md), [citation-management](notes/research-writing/citation-management.md), [figure-designer](notes/research-writing/figure-designer.md), [intro-drafter](notes/research-writing/intro-drafter.md), [latex-posters](notes/research-writing/latex-posters.md), [markdown-mermaid-writing](notes/research-writing/markdown-mermaid-writing.md), [peer-review](notes/research-writing/peer-review.md), [pptx-posters](notes/research-writing/pptx-posters.md), [pre-submission-reviewer](notes/research-writing/pre-submission-reviewer.md), [pyzotero](notes/research-writing/pyzotero.md), [research-grants](notes/research-writing/research-grants.md), [scholar-evaluation](notes/research-writing/scholar-evaluation.md), [scientific-critical-thinking](notes/research-writing/scientific-critical-thinking.md), [scientific-schematics](notes/research-writing/scientific-schematics.md), [scientific-slides](notes/research-writing/scientific-slides.md), [scientific-visualization](notes/research-writing/scientific-visualization.md), [scientific-writing](notes/research-writing/scientific-writing.md), [tech-paper-template](notes/research-writing/tech-paper-template.md), [venue-templates](notes/research-writing/venue-templates.md)
- **[Academic Paper & Nature Pipelines](maps/academic-pipelines.md)（14）**：[academic-paper](notes/academic-pipelines/academic-paper.md), [academic-paper-reviewer](notes/academic-pipelines/academic-paper-reviewer.md), [academic-pipeline](notes/academic-pipelines/academic-pipeline.md), [deep-research](notes/academic-pipelines/deep-research.md), [nature-academic-search](notes/academic-pipelines/nature-academic-search.md), [nature-citation](notes/academic-pipelines/nature-citation.md), [nature-data](notes/academic-pipelines/nature-data.md), [nature-figure](notes/academic-pipelines/nature-figure.md), [nature-paper2ppt](notes/academic-pipelines/nature-paper2ppt.md), [nature-polishing](notes/academic-pipelines/nature-polishing.md), [nature-reader](notes/academic-pipelines/nature-reader.md), [nature-response](notes/academic-pipelines/nature-response.md), [nature-reviewer](notes/academic-pipelines/nature-reviewer.md), [nature-writing](notes/academic-pipelines/nature-writing.md)
- **[Literature Search & Knowledge Discovery](maps/literature-discovery.md)（6）**：[defuddle](notes/literature-discovery/defuddle.md), [exa-search](notes/literature-discovery/exa-search.md), [literature-review](notes/literature-discovery/literature-review.md), [paper-lookup](notes/literature-discovery/paper-lookup.md), [parallel-web](notes/literature-discovery/parallel-web.md), [research-lookup](notes/literature-discovery/research-lookup.md)
- **[Documents, Office & Media](maps/documents-office.md)（6）**：[docx](notes/documents-office/docx.md), [generate-image](notes/documents-office/generate-image.md), [markitdown](notes/documents-office/markitdown.md), [pdf](notes/documents-office/pdf.md), [pptx](notes/documents-office/pptx.md), [xlsx](notes/documents-office/xlsx.md)
- **[Cloud, Infra & MLOps](maps/cloud-devops.md)（11）**：[aws-agentic-ai](notes/cloud-devops/aws-agentic-ai.md), [aws-cdk-development](notes/cloud-devops/aws-cdk-development.md), [aws-cost-operations](notes/cloud-devops/aws-cost-operations.md), [aws-mcp-setup](notes/cloud-devops/aws-mcp-setup.md), [aws-serverless-eda](notes/cloud-devops/aws-serverless-eda.md), [ci-cd-and-automation](notes/cloud-devops/ci-cd-and-automation.md), [devcontainer-setup](notes/cloud-devops/devcontainer-setup.md), [hf-cli](notes/cloud-devops/hf-cli.md), [modal](notes/cloud-devops/modal.md), [modern-python](notes/cloud-devops/modern-python.md), [shipping-and-launch](notes/cloud-devops/shipping-and-launch.md)
- **[Software Development & Engineering](maps/software-dev.md)（30）**：[api-and-interface-design](notes/software-dev/api-and-interface-design.md), [brainstorming](notes/software-dev/brainstorming.md), [code-review-and-quality](notes/software-dev/code-review-and-quality.md), [code-simplification](notes/software-dev/code-simplification.md), [context-engineering](notes/software-dev/context-engineering.md), [debugging-and-error-recovery](notes/software-dev/debugging-and-error-recovery.md), [deprecation-and-migration](notes/software-dev/deprecation-and-migration.md), [dispatching-parallel-agents](notes/software-dev/dispatching-parallel-agents.md), [documentation-and-adrs](notes/software-dev/documentation-and-adrs.md), [doubt-driven-development](notes/software-dev/doubt-driven-development.md), [executing-plans](notes/software-dev/executing-plans.md), [finishing-a-development-branch](notes/software-dev/finishing-a-development-branch.md), [git-workflow-and-versioning](notes/software-dev/git-workflow-and-versioning.md), [incremental-implementation](notes/software-dev/incremental-implementation.md), [observability-and-instrumentation](notes/software-dev/observability-and-instrumentation.md), [opensrc](notes/software-dev/opensrc.md), [planning-and-task-breakdown](notes/software-dev/planning-and-task-breakdown.md), [receiving-code-review](notes/software-dev/receiving-code-review.md), [requesting-code-review](notes/software-dev/requesting-code-review.md), [source-driven-development](notes/software-dev/source-driven-development.md), [spec-driven-development](notes/software-dev/spec-driven-development.md), [subagent-driven-development](notes/software-dev/subagent-driven-development.md), [systematic-debugging](notes/software-dev/systematic-debugging.md), [test-driven-development](notes/software-dev/test-driven-development.md), [using-agent-skills](notes/software-dev/using-agent-skills.md), [using-git-worktrees](notes/software-dev/using-git-worktrees.md), [using-superpowers](notes/software-dev/using-superpowers.md), [verification-before-completion](notes/software-dev/verification-before-completion.md), [writing-plans](notes/software-dev/writing-plans.md), [writing-skills](notes/software-dev/writing-skills.md)
- **[Vault, Skills & Workflow Meta](maps/vault-meta.md)（5）**：[auditing-skills](notes/vault-meta/auditing-skills.md), [autoskill](notes/vault-meta/autoskill.md), [find-skills](notes/vault-meta/find-skills.md), [get-available-resources](notes/vault-meta/get-available-resources.md), [mcp-builder](notes/vault-meta/mcp-builder.md)
- **[Reasoning, Ideation & Decision](maps/reasoning-ideation.md)（9）**：[consciousness-council](notes/reasoning-ideation/consciousness-council.md), [hypogenic](notes/reasoning-ideation/hypogenic.md), [hypothesis-generation](notes/reasoning-ideation/hypothesis-generation.md), [idea-evaluator](notes/reasoning-ideation/idea-evaluator.md), [idea-refine](notes/reasoning-ideation/idea-refine.md), [interview-me](notes/reasoning-ideation/interview-me.md), [scientific-brainstorming](notes/reasoning-ideation/scientific-brainstorming.md), [vibe-research-workflow](notes/reasoning-ideation/vibe-research-workflow.md), [what-if-oracle](notes/reasoning-ideation/what-if-oracle.md)
- **[Web Automation, Frontend & Design](maps/web-automation-frontend.md)（7）**：[agent-browser](notes/web-automation-frontend/agent-browser.md), [browser-testing-with-devtools](notes/web-automation-frontend/browser-testing-with-devtools.md), [frontend-design](notes/web-automation-frontend/frontend-design.md), [frontend-ui-engineering](notes/web-automation-frontend/frontend-ui-engineering.md), [performance-optimization](notes/web-automation-frontend/performance-optimization.md), [playwright-best-practices](notes/web-automation-frontend/playwright-best-practices.md), [webapp-testing](notes/web-automation-frontend/webapp-testing.md)
- **[Security & Auditing](maps/security-auditing.md)（5）**：[agentic-actions-auditor](notes/security-auditing/agentic-actions-auditor.md), [gh-cli](notes/security-auditing/gh-cli.md), [property-based-testing](notes/security-auditing/property-based-testing.md), [security-and-hardening](notes/security-auditing/security-and-hardening.md), [zeroize-audit](notes/security-auditing/zeroize-audit.md)
