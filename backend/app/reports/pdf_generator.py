import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class PDFReportGenerator:
    def generate_pdf(self, output_path: str, title: str, content_lines: list[str]) -> str:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, title)

        c.setFont("Helvetica", 10)
        y = height - 80

        for line in content_lines:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 50
            c.drawString(50, y, line[:100])
            y -= 15

        c.save()
        return output_path
