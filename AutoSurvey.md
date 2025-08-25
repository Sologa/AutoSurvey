

# AutoSurvey: Large Language Models Can Automatically Write Surveys

**Authors:** Yidong Wang; Qi Guo; Wenjin Yao; Hongbo Zhang; Xin Zhang; Zhen Wu; Meishan Zhang; Xinyu Dai; Min Zhang; Qingsong Wen; Wei Ye; Shikun Zhang; Yue Zhang  
**Affiliations:** Westlake University; Peking University; Nanjing University; Harbin Institute of Technology (Shenzhen); Squirrel AI  
**Status:** Preprint (Under review)  
**Project Resources:** https://github.com/AutoSurveys/AutoSurvey

---

## Abstract
This paper introduces **AutoSurvey**, a speedy and well‑organized methodology for automating the creation of comprehensive literature surveys in rapidly evolving fields like artificial intelligence. Traditional survey writing struggles with scale and complexity; LLMs are promising but face **context window limits**, **parametric knowledge constraints**, and the **lack of evaluation benchmarks**. AutoSurvey addresses these via a four‑phase pipeline—**initial retrieval & outline generation**, **parallel subsection drafting**, **integration & refinement**, and **rigorous evaluation & iteration**—plus **Real‑time Knowledge Update** (RAG) and a **Multi‑LLM‑as‑Judge** evaluation. Experiments across 8k/16k/32k/64k‑token surveys show high citation and content quality, approaching human performance while being dramatically faster.

---

## Table of Contents
- [AutoSurvey: Large Language Models Can Automatically Write Surveys](#autosurvey-large-language-models-can-automatically-write-surveys)
  - [Abstract](#abstract)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Methodology](#2-methodology)
    - [2.1 Phase 1: Initial Retrieval \& Outline Generation](#21-phase-1-initial-retrieval--outline-generation)
    - [2.2 Phase 2: Subsection Drafting](#22-phase-2-subsection-drafting)
    - [2.3 Phase 3: Integration \& Refinement](#23-phase-3-integration--refinement)
    - [2.4 Phase 4: Rigorous Evaluation \& Iteration](#24-phase-4-rigorous-evaluation--iteration)
    - [2.5 Algorithm 1: Pseudocode](#25-algorithm-1-pseudocode)
  - [3. Experiments](#3-experiments)
    - [3.1 Setup](#31-setup)
    - [3.2 Metrics](#32-metrics)
    - [3.3 Baselines \& Implementation Details](#33-baselines--implementation-details)
    - [3.4 Main Results](#34-main-results)
    - [3.5 Meta‑Evaluation](#35-metaevaluation)
    - [3.6 Ablation Study](#36-ablation-study)
    - [3.7 Effect of Iterations](#37-effect-of-iterations)
    - [3.8 Knowledge Utility Study](#38-knowledge-utility-study)
  - [4. Related Work](#4-related-work)
  - [5. Limitation](#5-limitation)
  - [6. Conclusion](#6-conclusion)
  - [Appendix A. Topics \& Human‑Writing Surveys](#appendix-a-topics--humanwriting-surveys)
  - [Appendix B. Implementation Details](#appendix-b-implementation-details)
  - [Appendix C. Evaluation Details](#appendix-c-evaluation-details)
  - [Appendix D. Cost Analysis](#appendix-d-cost-analysis)
  - [Appendix E. Societal Impact \& Ethics](#appendix-e-societal-impact--ethics)
  - [Appendix F. Prompts Used in AutoSurvey](#appendix-f-prompts-used-in-autosurvey)
    - [Rough Outline Prompt](#rough-outline-prompt)
    - [Subsection Outline Prompt](#subsection-outline-prompt)
    - [Merging Outline Prompt](#merging-outline-prompt)
    - [Subsection Writing Prompt](#subsection-writing-prompt)
    - [Citation Reflection Prompt](#citation-reflection-prompt)
    - [Coherency Refinement Prompt](#coherency-refinement-prompt)
  - [Example Generated Survey (Excerpt)](#example-generated-survey-excerpt)
  - [References](#references)

---

## 1. Introduction
Survey papers provide comprehensive overviews of research developments, trends, and future directions. In the LLM era, the literature volume is exploding—e.g., in the first four months of 2024 alone, 4,000+ papers containing “Large Language Model” were submitted to arXiv (Figure 1a). Despite more surveys (Figure 1b), gaps remain (Figure 1c), where topic clusters still lack comprehensive surveys. 

**Challenges for LLM‑authored surveys:**  
1) **Context windows:** Inputs may require hundreds of papers; outputs themselves can be tens of thousands of tokens, exceeding typical LLM output limits.  
2) **Parametric knowledge limits:** Solely relying on model internals risks hallucinations and missing the latest studies.  
3) **Evaluation:** Scalable, rigorous benchmarks for long‑form survey quality are scarce.

**AutoSurvey** is proposed to address these with:  
- **Logical parallel generation** (two‑stage: outline, then parallel subsection drafting; followed by global revision/merging).  
- **Real‑time knowledge update** via **Retrieval‑Augmented Generation (RAG)**.  
- **Multi‑LLM‑as‑Judge** evaluation for **Citation Quality** (recall, precision) and **Content Quality** (coverage, structure, relevance), calibrated with human experts.

**Headline results (64k tokens):** Citation Recall **82.25%**, Precision **77.41%** (vs. naive RAG LLM 68.79/61.97; humans 86.33/77.78). Content Quality: Coverage **4.73**, Structure **4.33**, Relevance **4.86** (humans 5.00/4.66/5.00). Spearman correlation with human ranking strongest with mixed LLM judges (**ρ=0.5429**).

> **Note:** Figures are described textually here; the original includes plots for paper/survey growth and T‑SNE clusters illustrating under‑served topics.

---

## 2. Methodology
AutoSurvey is a four‑phase pipeline (see also Figure 2 in the paper):

### 2.1 Phase 1: Initial Retrieval & Outline Generation
- Use embedding‑based retrieval over a publications database to get an initial pool \(P_{init}\) for topic \(T\).
- Generate **multiple outlines in parallel** (due to long contexts), then **merge** them into a final comprehensive outline **O** with section names **and brief descriptions**.

### 2.2 Phase 2: Subsection Drafting
- For each outline section \(O_i\), retrieve section‑specific references \(P_{sec}\) and **draft** subsection \(S_i\) in parallel using specialized LLMs.
- Explicit in‑text citations of paper titles (e.g., `[Paper Title]`) are required; citations are later mapped to arXiv entries.

### 2.3 Phase 3: Integration & Refinement
- **Refine** each subsection (readability, redundancy removal, local coherence) → **R_i**.
- **Merge** all refined sections into a single document **F**, checking and correcting citations during polishing.

### 2.4 Phase 4: Rigorous Evaluation & Iteration
- **Multi‑LLM‑as‑Judge** evaluates **Citation Quality** (Recall/Precision) and **Content Quality** (Coverage/Structure/Relevance; 5‑point rubric), calibrated by human experts.  
- Run N trials and **select the best** document **F_best**.

### 2.5 Algorithm 1: Pseudocode
```text
ALGORITHM 1  AUTOSURVEY: Automated Survey Creation Using LLMs
Input: Topic T, publications database D  |  Output: Final survey F_best
for trial t = 1..N do
  # Phase 1: Initial Retrieval & Outline Generation
  P_init ← Retrieve(T, D)
  O ← Outline(T, P_init)
  # Phase 2: Subsection Drafting (parallel)
  for each section O_i in O in parallel do
    P_sec ← Retrieve(O_i, D)
    S_i ← Draft(O_i, P_sec)
  end for
  # Phase 3: Integration & Refinement
  R_i ← Refine(S_i)  (context-aware polishing & citation checking)
  F_t ← Merge(R_1..R_n)
end for
# Phase 4: Rigorous Evaluation & Iteration
F_best ← Evaluate(F_1..F_N)
return F_best
```

---

## 3. Experiments

### 3.1 Setup
- **Writer (drafting):** Claude‑3‑Haiku (fast, cost‑effective, 200k tokens).  
- **Judges:** GPT‑4 (gpt‑4‑0125‑preview), Claude‑3‑Haiku, Gemini‑1.5‑Pro; also a **mixture** judge.  
- **Survey lengths:** 8k, 16k, 32k, 64k tokens.

**Survey Creation Speed** (human model): let \(L\) be length, \(E\) experts, \(M\) tokens/hour/expert, prep time \(T_r\), writing time \(T_w=L/(E\cdot M)\), editing \(T_e=\tfrac{1}{2}T_w\). Total:  
\[\text{Time} = T_r + T_w + T_e = T_r + \frac{L}{E M} + \frac{1}{2}\cdot\frac{L}{E M}.\]
Speed = \(1/\text{Time}\) surveys/hour. For LLM methods, speed counts total API time.

### 3.2 Metrics
**Citation Quality** (adapted from [27]): extract claims \(c_i\) (sentences with citations), use NLI model \(h\) to test support by references \(Ref_i\).
- **Recall:** \(\frac{\sum_i h(c_i, Ref_i)}{|C|}\).
- **Precision:** with \(g(c_i, r_{ik})\) indicating relevance of a cited paper \(r_{ik}\):  
\(\text{Precision}=\frac{\sum_i \sum_k h(c_i, Ref_i) \cap g(c_i, r_{ik})}{\sum_i |Ref_i|}\).

**Content Quality** (LLM‑as‑Judge, 1–5):  
- **Coverage** (topic breadth), **Structure** (organization & coherence), **Relevance** (on‑topic focus). Calibrated by human experts; rubric in Table 1.

### 3.3 Baselines & Implementation Details
- **Baselines:** (i) Human‑written surveys from arXiv; (ii) **Naive RAG‑based LLM** (iteratively write to target length with same number of references as AutoSurvey).  
- **Retrieval DB:** 530k CS papers (arXiv).  
- **Initial drafting:** retrieve 1200 topic‑relevant papers; split into 30k‑token windows; generate/merge outlines using **abstracts**. Predetermine **8 sections**.  
- **Subsection drafting:** per section, retrieve **60 papers** by subsection description; use up to first **1,500 tokens** of each paper’s main body.  
- **Polishing:** same references provided; **iterations N=2**.  
- **Embedding model:** `nomic-embed-text-v1.5`.  
- **API params:** temperature=1; other defaults.  
- **Length bucketing:** 8k: (8–16k); 16k: (16–32k); etc.

### 3.4 Main Results
**Table 1. Content Quality Criteria (5‑point rubric)**

| Criterion | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|
| **Coverage** | Very limited; key areas missing | Partial; notable omissions | Generally comprehensive; a few key points missing | Covers most key areas; minor omissions | Fully comprehensive on key & peripheral topics |
| **Structure** | No clear logic; hard to follow | Weak flow; some disorder | Reasonable overall; some links/transitions need work | Good consistency; natural transitions | Tight structure; clear logic; smooth transitions |
| **Relevance** | Off‑topic/outdated | Some digressions | Generally on topic | Mostly focused; infrequent digressions | Exceptionally focused and on topic |

**Table 2. Human vs. Naive RAG LLM vs. AutoSurvey**

| Survey Length | Method | Speed (surveys/hr) | Citation Recall | Citation Precision | Coverage | Structure | Relevance | Avg. |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **8k** | Human | 0.16 | 80.00 | 87.50 | 4.50 | 4.16 | 5.00 | 4.52 |
|  | Naive RAG LLM | 79.67 | 78.14±5.23 | 71.92±6.83 | 4.40±0.48 | 3.86±0.71 | 4.86±0.33 | 4.33 |
|  | **AutoSurvey** | **107.00** | **82.48±2.77** | **77.42±3.28** | **4.60±0.48** | **4.46±0.49** | **4.80±0.39** | **4.61** |
| **16k** | Human | 0.14 | 88.52 | 79.63 | 4.66 | 4.38 | 5.00 | 4.66 |
|  | Naive RAG LLM | 43.41 | 71.48±12.50 | 65.31±15.36 | 4.46±0.49 | 3.66±0.69 | 4.73±0.44 | 4.23 |
|  | **AutoSurvey** | **95.51** | **81.34±3.65** | **76.94±1.93** | **4.66±0.47** | **4.33±0.59** | **4.86±0.33** | **4.60** |
| **32k** | Human | 0.10 | 88.57 | 77.14 | 4.66 | 4.50 | 5.00 | 4.71 |
|  | Naive RAG LLM | 22.64 | 79.88±4.35 | 65.03±8.39 | 4.41±0.64 | 3.75±0.72 | 4.66±0.47 | 4.23 |
|  | **AutoSurvey** | **91.46** | **83.14±2.44** | **78.04±3.14** | **4.73±0.44** | **4.26±0.69** | **4.80±0.54** | **4.58** |
| **64k** | Human | 0.07 | 86.33 | 77.78 | 5.00 | 4.66 | 5.00 | 4.88 |
|  | Naive RAG LLM | 12.56 | 68.79±11.00 | 61.97±13.45 | 4.40±0.61 | 3.66±0.47 | 4.66±0.47 | 4.19 |
|  | **AutoSurvey** | **73.59** | **82.25±3.64** | **77.41±3.84** | **4.73±0.44** | **4.33±0.47** | **4.86±0.33** | **4.62** |

**Observations:** AutoSurvey is vastly faster than human writing and faster than naive RAG at long lengths; it matches or approaches human citation/content quality and surpasses naive RAG notably on **Structure** and **Citation Precision**.

### 3.5 Meta‑Evaluation
Human experts perform pairwise comparisons (“which is better?”) to rank 20 surveys. LLM judge rankings correlate positively with human rankings; the **mixture** judge achieves the highest **Spearman’s ρ ≈ 0.543**.

### 3.6 Ablation Study
**Table 3. Component Ablations**

| Method | Citation Recall | Citation Precision | Coverage | Structure | Relevance | Avg. |
|---|---:|---:|---:|---:|---:|---:|
| AutoSurvey | 83.48±5.05 | 77.15±6.05 | 4.70±0.45 | 4.16±0.73 | 4.93±0.30 | 4.57 |
| w/o Retrieval | 60.11±6.42 | 51.65±6.33 | 4.51±0.49 | 4.01±0.74 | 4.88±0.32 | 4.44 |
| w/o Reflection | 83.23±3.82 | 76.36±4.08 | 4.76±0.42 | 4.13±0.76 | 4.88±0.32 | 4.56 |

**Takeaway:** Retrieval is critical for citation quality; reflection primarily improves structure/coherence.

**Table 4. Base LLM Writer Variants**

| Base LLM | Citation Recall | Citation Precision | Coverage | Structure | Relevance | Avg. |
|---|---:|---:|---:|---:|---:|---:|
| GPT‑4 | 80.25±4.19 | 78.83±7.00 | 4.80±0.54 | 4.46±0.49 | 4.86±0.33 | 4.70 |
| Claude‑Haiku | 82.45±2.77 | 76.31±2.18 | 4.66±0.47 | 4.26±0.67 | 4.86±0.33 | 4.58 |
| Gemini‑1.5‑Pro | 78.13±2.39 | 71.24±3.28 | 4.86±0.33 | 4.33±0.78 | 4.93±0.25 | 4.69 |
| **Human** | **85.86** | **80.51** | **4.71** | **4.43** | **5.00** | **4.70** |

### 3.7 Effect of Iterations
Increasing iterations from 1→5 slightly improves average content quality, with diminishing returns after **2** iterations (see figure description in the paper).

### 3.8 Knowledge Utility Study
50 multiple‑choice questions across 5 topics. Accuracy (Claude) under different references:

**Table 5. Accuracy with Different References**

| Method | Accuracy |
|---|---:|
| Direct (no refs) | 58.40±4.96 |
| Naive RAG LLM (32k survey) | 65.20±8.06 |
| **AutoSurvey (32k survey)** | **67.60±4.96** |
| Upper‑bound (20 option‑related papers, 30k tokens) | 73.60±3.44 |

AutoSurvey improves over direct answering by **+9.2%**, and over naive RAG surveys by **+2.4%**.

---

## 4. Related Work
**Long‑form generation**: context extension (positional interpolation; LongLoRA; long‑term memory), memory‑augmented approaches (RecurrentGPT; Temp‑LoRA), and hierarchical modeling. **Automatic writing**: RAG for cited claims, IRP (plan‑retrieve‑paraphrase), outline‑driven generation (PaperRobot; STORM). AutoSurvey targets **long (up to 64k tokens)** academic reviews with combined **outline→parallel drafting→polish** and rigorous evaluation.

## 5. Limitation
Manual analysis of 100 unsupported claims shows error types: **Misalignment (39%)**, **Misinterpretation (10%)**, **Overgeneralization (51%)**—indicating reliance on parametric knowledge persists. Additional societal/ethical considerations appear in Appendix E.

## 6. Conclusion
AutoSurvey automates comprehensive survey writing by combining retrieval, parallel drafting, refinement, and multi‑LLM evaluation. It approaches human quality while being vastly faster, offering a scalable tool for synthesizing fast‑moving literatures like LLM research.

---

## Appendix A. Topics & Human‑Writing Surveys
**20 topics** spanning LLM subareas; selection balanced breadth and Google Scholar citations. (Human‑written surveys excluded from retrieval during evaluation.)

**Table 6. Topics & Example Survey Titles (Citations)**

| Topic | Survey Title | Cites |
|---|---|---:|
| In‑context Learning | A Survey for In‑Context Learning | 323 |
| LLMs for Recommendation | A Survey on Large Language Models for Recommendation | 55 |
| LLM‑Generated Texts Detection | A Survey of Detecting LLM‑Generated Texts | 42 |
| Explainability for LLMs | Explainability for Large Language Models | 25 |
| Evaluation of LLMs | A Survey on Evaluation of Large Language Models | 183 |
| LLM‑based Agents | A Survey on Large Language Model based Autonomous Agents | 101 |
| LLMs in Medicine | A Survey of Large Language Models in Medicine | 234 |
| Domain Specialization | Domain Specialization as the Key to Make LLMs Disruptive | 14 |
| Challenges in Education | Practical and Ethical Challenges of LLMs in Education | 53 |
| Alignment of LLMs | Aligning Large Language Models with Human | 53 |
| ChatGPT | A Survey on ChatGPT and Beyond | 144 |
| Instruction Tuning | Instruction Tuning for Large Language Models | 45 |
| LLMs for IR | Large Language Models for Information Retrieval | 22 |
| Safety | Towards Safer Generative Language Models | 17 |
| Chain of Thought | A Survey of Chain of Thought Reasoning | 13 |
| Hallucination | A Survey on Hallucination in LLMs | 116 |
| Bias & Fairness | Bias and Fairness in Large Language Models | 12 |
| Large Multi‑Modal LMs | Large‑scale Multi‑Modal Pre‑trained Models | 61 |
| Acceleration | A Survey on Model Compression & Acceleration for PLMs | 22 |
| LLMs for SE | Large Language Models for Software Engineering | 49 |

---

## Appendix B. Implementation Details
- **Embeddings:** `nomic-embed-text-v1.5`. Store embeddings of **title + abstract** per paper (no chunking necessary for abstracts).  
- **Retrieval & mapping:** retrieve by abstract similarity; generated citation titles are embedded and mapped to closest paper titles in DB to ensure existence.  
- **API parameters:** temperature = 1. Length variability leads to bucketing by final token count: 8–16k → 8k, 16–32k → 16k, etc.

---

## Appendix C. Evaluation Details
- **Claims:** any sentence with ≥1 citation.  
- **Humans:** three PhD students (LLM survey experience) scored per rubric; final rankings aggregate scores.

---

## Appendix D. Cost Analysis
**Table 7. Average Token Usage & Cost (32k‑token survey)**

| Input tokens | Output tokens | Claude‑Haiku | Gemini‑1.5‑Pro | GPT‑4 |
|---:|---:|---:|---:|---:|
| 3,009.7k | 112.9k | **$0.89** | $11.72 | $33.48 |

---

## Appendix E. Societal Impact & Ethics
AutoSurvey can help fill survey gaps across fields by integrating specialized databases, but **citation errors** still occur; content is **for reference**. All evaluation participants were compensated; all data sourced from arXiv under non‑commercial use.

---

## Appendix F. Prompts Used in AutoSurvey
Below are the key prompts used by the system (condensed for readability). Replace placeholders in brackets.

### Rough Outline Prompt
```text
You want to write an overall and comprehensive academic survey about [TOPIC].
You are provided with a list of papers related to the topic:
---
[PAPER LIST]
---
Draft an outline with a title and [SECTION NUM] sections.
Each section has a brief description of what to write.
Return format:
Title: [TITLE]
Section 1: [NAME]
Description 1: [ONE‑SENTENCE DESCRIPTION]
...
Section K: [NAME]
Description K: [ONE‑SENTENCE DESCRIPTION]
```

### Subsection Outline Prompt
```text
Topic: [TOPIC]
Overall outline:
[OVERALL OUTLINE]
Enrich section [SECTION NAME] by generating several subsections with one‑sentence descriptions.
Use references:
[PAPER LIST]
Return only the subsection outline in the given format.
```

### Merging Outline Prompt
```text
Given multiple candidate outlines for [TOPIC], merge into a final outline that is comprehensive and logical.
Return in the standard outline format (Title, Sections + Descriptions).
```

### Subsection Writing Prompt
```text
Topic: [TOPIC]
Overall outline:
[OVERALL OUTLINE]
References:
[PAPER LIST]
Write the subsection "[SUBSECTION NAME]" with >[WORD NUM] words.
Guidelines: cite specific claims using [paper_title].
Return only the subsection content.
```

### Citation Reflection Prompt
```text
Topic: [TOPIC]
References:
[PAPER LIST]
Subsection:
[SUBSECTION]
Check each [paper_title] citation. If a citation does not support the sentence, correct or remove it.
Return only the corrected subsection (do not change other text).
```

### Coherency Refinement Prompt
```text
Refine the target subsection to improve coherence with its previous and following subsections.
Keep the core information intact. Do not change citations in []!
Return the refined subsection only.
```

---

## Example Generated Survey (Excerpt)
**Comprehensive Survey on Emotion Recognition Using Large Language Models**  
(Outline and excerpt provided in the paper; includes Introduction; Techniques; Enhancements; Challenges & Ethics; Applications; References.)

---

## References
[1]–[48] Full reference list as given in the paper, including works on surveys, LLM evaluation, RAG, long‑context modeling, hierarchical generation, and prompting.  

**Selected examples:**
- Achiam et al. (2023). *GPT‑4 Technical Report.*
- Gao et al. (2023). *Enabling LLMs to Generate Text with Citations.*
- Lewis et al. (2020). *Retrieval‑Augmented Generation for Knowledge‑Intensive NLP.*
- Zheng et al. (2024). *Judging LLM‑as‑a‑Judge with MT‑Bench and Chatbot Arena.*
- Zhou et al. (2023). *RecurrentGPT.*

> For the complete enumerated list [1]–[48], see the original paper’s References section.