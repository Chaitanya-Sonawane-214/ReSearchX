"""One-off generator for the preloaded demo paper (spec section 22).

Run with:  python -m data.generate_sample   (from the backend/ directory)

Produces data/sample_paper.pdf — a plausible, well-structured research paper
so the full pipeline (parsing, all 7 agents, aggregation, similarity,
reviewer matching) can be demonstrated without the presenter hunting for a
real PDF. Built with fpdf2's built-in Helvetica font, so it needs no
external assets and works fully offline.
"""
from __future__ import annotations

import os
from fpdf import FPDF

TITLE = "AI-Driven Carbon Emission Prediction Using Multi-Agent Systems"
AUTHORS = "A. Sharma, R. Mehta, S. Patel"
AFFILIATION = "Department of Computer Science, National Institute of Technology"

ABSTRACT = (
    "Accurate carbon emission forecasting is critical for climate policy and industrial "
    "planning, yet existing single-model approaches struggle to capture the heterogeneous "
    "signals produced by energy, transport and manufacturing sectors. This paper proposes a "
    "multi-agent system in which specialized forecasting agents collaborate to predict "
    "sector-level carbon emissions and a coordinator agent aggregates their outputs into a "
    "unified estimate. We evaluate the framework on a five-year multi-sector emissions "
    "dataset and show that the multi-agent approach demonstrates a 14% reduction in mean "
    "absolute error compared to a single centralized regression model [1], [2]. We further "
    "discuss the reproducibility, limitations, and future directions of the proposed system."
)

INTRODUCTION = (
    "Climate change mitigation strategies increasingly rely on accurate, sector-aware carbon "
    "emission forecasts to guide policy decisions [3]. Traditional statistical time-series "
    "models such as ARIMA and single deep learning regressors are typically trained on "
    "aggregated national-level data, which masks important heterogeneity between sectors such "
    "as energy generation, transportation, and manufacturing [4], [5]. This paper proposes a "
    "novel multi-agent system in which each agent specializes in a distinct emission source "
    "and a coordinator agent reconciles their predictions into a single, interpretable "
    "forecast. Our contribution is threefold: (1) a modular multi-agent forecasting "
    "architecture, (2) an empirical study across three real-world sectors, and (3) an "
    "analysis of the interpretability benefits this architecture provides over a monolithic "
    "model. We address the problem of sector-level emission forecasting by decomposing it "
    "into cooperating sub-problems, each solved by a dedicated agent."
)

RELATED_WORK = (
    "Prior work on emission forecasting has largely focused on centralized statistical models "
    "[6], [7]. Multi-agent systems have been explored extensively in traffic simulation [8] "
    "and smart-grid load balancing [9], [10], but their application to carbon emission "
    "forecasting remains limited. Recent transformer-based forecasting models [11] show "
    "strong performance on aggregated series but do not decompose emissions by sector. Our "
    "work builds on the coordination strategies proposed in multi-agent reinforcement "
    "learning literature [12] and adapts them to a supervised forecasting setting, connecting "
    "this line of research directly to the proposed methodology described in Section 3."
)

METHODOLOGY = (
    "The proposed framework consists of three sector-specialist agents (Energy, Transport, "
    "Manufacturing) and one Coordinator agent. Each specialist agent is implemented as a "
    "gradient-boosted regression model trained on sector-specific features (fuel mix, vehicle "
    "counts, industrial output). The Coordinator agent receives each specialist's prediction "
    "along with a learned confidence weight and produces the final estimate as:\n\n"
    "        E_total = w1*E_energy + w2*E_transport + w3*E_manufacturing     (1)\n\n"
    "where the weights w1, w2, w3 are learned jointly via a shallow meta-regressor trained on "
    "a held-out validation split (Table 1). Training used a dataset of 5 years of monthly "
    "sector-level emissions collected from public national energy reports. The dataset is "
    "publicly available and the implementation, including hyperparameters and training "
    "scripts, is released alongside this paper to support reproducibility."
)

RESULTS = (
    "We evaluate the multi-agent framework against a single centralized gradient-boosted "
    "regressor trained on the full concatenated feature set. Figure 1 shows the system "
    "architecture, and Figure 2 shows prediction accuracy across training epochs. Table 2 "
    "reports mean absolute error (MAE) per sector. The multi-agent approach achieves a mean "
    "absolute error of 4.8 (versus 5.6 for the baseline), a 14% relative improvement. "
    "Ablating the Coordinator agent (using simple averaging instead of learned weights) "
    "increases MAE to 5.2, confirming the coordinator's contribution. The loss curve is "
    "computed as:\n\n"
    "        L = (1/N) * sum((y_pred - y_true)^2)     (2)\n\n"
    "and converges within 40 epochs across all three specialist agents."
)

DISCUSSION = (
    "The sector-specialist decomposition improves both accuracy and interpretability: "
    "policy analysts can inspect each agent's contribution independently rather than treating "
    "the forecast as a black box. The learned coordinator weights also reveal which sectors "
    "dominate the national emissions trend during different seasons, which single-model "
    "baselines cannot expose directly."
)

LIMITATIONS = (
    "This study has several limitations. The dataset covers three sectors and a single "
    "country's reporting standards, so generalization to other regions with different data "
    "collection practices is untested. The confidence-weighting scheme assumes each "
    "specialist's error is independent, which may not hold under systemic shocks such as "
    "policy changes. We view extending the framework to additional sectors and cross-country "
    "validation as important future work."
)

CONCLUSION = (
    "We presented a multi-agent framework for sector-aware carbon emission forecasting and "
    "showed it outperforms a centralized baseline while improving interpretability. Future "
    "work includes extending the framework to additional sectors, incorporating "
    "uncertainty estimates, and validating across multiple countries' reporting standards."
)

REFERENCES = [
    "Sharma, A., Mehta, R. Multi-Agent Forecasting for Environmental Systems. J. Env. Informatics, 2022.",
    "Patel, S. et al. Ensemble Learning for Emission Estimation. IEEE Trans. Sustainable Computing, 2021.",
    "IPCC. Climate Change Mitigation Pathways Report. 2021.",
    "Box, G., Jenkins, G. Time Series Analysis: Forecasting and Control. 1976.",
    "Zhang, Y. et al. Deep Learning for Energy Demand Forecasting. Applied Energy, 2020.",
    "Lee, K., Kim, J. Sector-Level Emission Modeling with Gradient Boosting. Energy Reports, 2021.",
    "Chen, H. et al. National Emission Trends: A Statistical Review. Climate Policy, 2019.",
    "Wooldridge, M. An Introduction to MultiAgent Systems. Wiley, 2009.",
    "Bazzan, A. Multi-Agent Systems for Traffic and Transportation. IGI Global, 2010.",
    "Kumar, R. et al. Multi-Agent Coordination for Smart Grid Load Balancing. IEEE Access, 2020.",
    "Singh, P. et al. Decentralized Load Forecasting via Cooperative Agents. Applied Soft Computing, 2019.",
    "Vaswani, A. et al. Attention Is All You Need. NeurIPS, 2017.",
    "Lowe, R. et al. Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments. NeurIPS, 2017.",
    "Friedman, J. Greedy Function Approximation: A Gradient Boosting Machine. Annals of Statistics, 2001.",
    "Breiman, L. Random Forests. Machine Learning, 2001.",
    "Hyndman, R., Athanasopoulos, G. Forecasting: Principles and Practice. OTexts, 2018.",
    "Gao, Y. et al. Interpretable Machine Learning for Climate Science. Nature Climate Change, 2022.",
    "Ribeiro, M. et al. Why Should I Trust You? Explaining Predictions. KDD, 2016.",
    "International Energy Agency. Global Energy Review. 2022.",
    "Sutton, R., Barto, A. Reinforcement Learning: An Introduction. MIT Press, 2018.",
]


class ResearchPaperPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def _heading(pdf: ResearchPaperPDF, text: str):
    pdf.ln(3)
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def _body(pdf: ResearchPaperPDF, text: str):
    pdf.set_font("helvetica", "", 10.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 5.6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def _caption(pdf: ResearchPaperPDF, text: str):
    pdf.set_font("helvetica", "I", 9.5)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def build_pdf() -> bytes:
    pdf = ResearchPaperPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(20, 18, 20)
    pdf.set_title(TITLE)
    pdf.set_author(AUTHORS)
    pdf.add_page()

    pdf.set_font("helvetica", "B", 17)
    pdf.set_text_color(10, 10, 10)
    pdf.multi_cell(0, 8, TITLE, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 6, AUTHORS, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "I", 9.5)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, AFFILIATION, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    _heading(pdf, "Abstract")
    _body(pdf, ABSTRACT)

    _heading(pdf, "1. Introduction")
    _body(pdf, INTRODUCTION)

    _heading(pdf, "2. Related Work")
    _body(pdf, RELATED_WORK)

    _heading(pdf, "3. Methodology")
    _body(pdf, METHODOLOGY)
    _caption(pdf, "Figure 1: System architecture showing the three specialist agents feeding "
                  "the Coordinator agent, which produces the final emission estimate.")
    _caption(pdf, "Table 1: Dataset statistics per sector (samples, feature count, date range).")

    _heading(pdf, "4. Results")
    _body(pdf, RESULTS)
    _caption(pdf, "Figure 2: Prediction accuracy (MAE) over training epochs for each specialist agent.")
    _caption(pdf, "Table 2: Mean absolute error per sector, multi-agent vs. centralized baseline.")

    _heading(pdf, "5. Discussion")
    _body(pdf, DISCUSSION)

    _heading(pdf, "6. Limitations")
    _body(pdf, LIMITATIONS)

    _heading(pdf, "7. Conclusion")
    _body(pdf, CONCLUSION)

    _heading(pdf, "References")
    pdf.set_font("helvetica", "", 9.5)
    pdf.set_text_color(30, 30, 30)
    for i, ref in enumerate(REFERENCES, start=1):
        pdf.multi_cell(0, 5, f"[{i}] {ref}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

    return bytes(pdf.output())


def main():
    out_path = os.path.join(os.path.dirname(__file__), "sample_paper.pdf")
    with open(out_path, "wb") as f:
        f.write(build_pdf())
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
