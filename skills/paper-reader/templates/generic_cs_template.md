# Paper Reading Report: {Title}

## 1. Paper Metadata

| Item | Content |
|------|---------|
| Title | {Full paper title} |
| Authors | {Authors with affiliations} |
| Venue / Year | {Conference or journal, year} |
| DOI / Link | {URL} |
| Code / Data | {URL or "Not available"} |

## 2. One-Sentence Summary

> {Core contribution in one sentence, ≤50 words}

## 3. Core Contributions

1. **{Contribution 1}**: {Brief description}
2. **{Contribution 2}**: {Brief description}
3. **{Contribution 3}**: {Brief description}

## 4. Problem Setting

### 4.1 What problem does this paper solve?

### 4.2 Why is this problem important?

### 4.3 What are the limitations of prior work?

### 4.4 What is the key insight or novel idea?

## 5. Method

> **REPRODUCIBILITY REQUIREMENT:** The method description must be detailed enough that a researcher in the same field could reimplement the approach. For each component, describe: trigger conditions → inputs → step-by-step procedure → outputs → parameters with values. Distinguish three layers clearly:
> 1. **Static structure** — what the model/architecture/schema looks like
> 2. **Construction** — how it is built, trained, or learned from data
> 3. **Inference** — how it is used at runtime to produce results
> Do not conflate these three layers. If the paper provides pseudocode, describe it faithfully without compression.

### 5.1 High-Level Overview

{Describe the overall pipeline, architecture, or approach. Include a diagram description if applicable. Distinguish the offline phase from the online phase here.}

### 5.2 Formal Problem Definition

{State the problem formally if the paper does so. Include key notation.}

### 5.3 Key Algorithm / Mechanism

{Describe the core algorithm, mechanism, or design. Be specific — include all steps, components, and their interactions. For each step, answer: when does it trigger? what does it do (inputs→outputs)? how is it parameterized?}

### 5.4 Design Decisions and Justifications

{What non-obvious design choices did the authors make, and why?}

### 5.5 Training / Inference Procedure (if ML paper)

{Describe the training procedure, loss function, optimization, inference. Mark "Not applicable" for non-ML papers. Separate training (model construction) from inference (model usage) clearly.}

### 5.6 Complexity Analysis

{Time complexity, space complexity, or other theoretical guarantees if provided. Break down by algorithm/component if the paper provides multiple analyses.}

## 6. Key Formulas

{List all important formulas with explanations. Skip if the paper has no significant formulas.}

### Formula 1: {Purpose}

$$
{formula}
$$

- **Meaning**: {One-sentence explanation}
- **Notation**: {Symbol definitions}

## 7. Key Figures and Tables

{Describe important figures and tables. If images are available, reference them.}

### Figure 1: {Caption}

{Description of what the figure shows and key takeaways.}

### Table 1: {Caption}

{Table content or summary. Key findings from the table.}

## 8. Experiments

### 8.1 Experimental Setup

| Item | Detail |
|------|--------|
| Datasets | {Names, sizes, splits} |
| Baselines | {Methods compared against} |
| Metrics | {Evaluation metrics used} |
| Hardware | {CPU, GPU, memory} |
| Software | {OS, libraries, versions} |

### 8.2 Implementation Details

{Hyperparameters, random seeds, data preprocessing, any details needed for reproduction.}

### 8.3 Main Results

{Quantitative results. Include exact numbers. Which baseline does the proposed method outperform, and by how much?}

### 8.4 Ablation Studies

{What components were ablated? What was the impact of each?}

### 8.5 Case Studies / Qualitative Results

{Any case studies, visualizations, or qualitative analysis.}

## 9. Critical Analysis

### 9.1 Strengths

1. {Strength 1}
2. {Strength 2}
3. {Strength 3}

### 9.2 Limitations (acknowledged by authors)

1. {Limitation 1}
2. {Limitation 2}

### 9.3 Potential Issues (not acknowledged by authors)

1. {Issue 1}
2. {Issue 2}

### 9.4 Key Assumptions

{What assumptions does the method rely on? How valid are they?}

### 9.5 Fairness of Experimental Comparison

{Is the comparison against baselines fair? Are there any confounding factors?}

## 10. Reproducibility Assessment

| Criterion | Status | Detail |
|-----------|--------|--------|
| Code available | Yes / No / Partial | {Link or explanation} |
| Data available | Yes / No / Partial | {Link or explanation} |
| Hyperparameters specified | Yes / No / Partial | {What is missing} |
| Hardware/software specified | Yes / No / Partial | {What is missing} |
| Evaluation protocol clear | Yes / No / Partial | {What is missing} |
| Estimated effort to reproduce | Low / Medium / High / Impossible | {Justification} |

## 11. Impact and Future Work

### 11.1 Potential Applications Beyond the Paper's Domain

### 11.2 Future Work Suggested by Authors

### 11.3 Your Own Ideas for Extensions

## 12. Q&A Log

{This section is populated during the Questioner-Reader Q&A phase. Each Q&A pair is recorded here.}

### Q1: {Question}

**A:** {Answer}
**Status:** Resolved / Unresolved

## 13. Reviewer Notes

{This section is populated during the Reviewer arbitration phase. All identified inconsistencies and their resolutions are recorded here.}

### Inconsistency 1

- **Section**: {section name}
- **Reader report**: {excerpt}
- **Questioner report**: {excerpt}
- **Ground truth (from paper)**: {excerpt}
- **Resolution**: {description}
