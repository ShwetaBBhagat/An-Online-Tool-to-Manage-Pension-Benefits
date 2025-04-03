from fpdf import FPDF

class StatementPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Monthly Pension Statement", ln=True, align="C")
        self.ln(5)

    def add_statement(self, data):
        self.set_font("Arial", size=12)
        for key, value in data.items():
            self.cell(0, 10, f"{key}: {value}", ln=True)
