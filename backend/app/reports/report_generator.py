import os
from typing import List
from app.models.db_models import Project, CryptoAsset, RiskAssessment
from app.reports.executive_summary import ExecutiveSummaryGenerator
from app.reports.pdf_generator import PDFReportGenerator


class ReportGenerator:
    def __init__(self):
        self.exec_gen = ExecutiveSummaryGenerator()
        self.pdf_gen = PDFReportGenerator()

    def create_project_report(self, project: Project, assets: List[CryptoAsset], risks: List[RiskAssessment], output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        summary_text = self.exec_gen.generate_summary_text(project, assets, risks)
        lines = summary_text.splitlines()

        file_path = os.path.join(output_dir, f"report_{project.id}.pdf")
        self.pdf_gen.generate_pdf(file_path, f"ECDAT Cryptographic Report - {project.name}", lines)

        return file_path
