from fpdf import FPDF

class StatementPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Workplace Pension Statement", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 8, "Issued by: Pension Portal Ltd.", ln=True, align="C")
        self.ln(5)

    def add_statement(self, data):
        self.set_font("Arial", "", 11)

        def section(title):
            self.set_font("Arial", "B", 12)
            self.set_text_color(0, 51, 102)
            self.cell(0, 10, title, ln=True)
            self.set_text_color(0, 0, 0)
            self.set_font("Arial", "", 11)

        def row(key, value):
            self.set_x(15)
            self.set_font("Arial", "B", 11)
            self.cell(65, 8, f"{key}:", 0)
            self.set_font("Arial", "", 11)
            self.cell(0, 8, str(value), ln=True)

        # Section 1: Personal Info
        section("Member Details")
        row("Name", data.get("Employee Name", "—"))
        row("National Insurance (NI)", "***-**-123")  # Masked example
        row("Employer", data.get("Employer Name", "—"))
        self.ln(3)

        # Section 2: Statement Summary
        section("Statement Summary")
        row("Statement ID", data["Statement ID"])
        row("Statement Period", data["Period"])
        row("Date Issued", data["Date Issued"])
        row("Pension Account Number", data["Pension Account"])
        row("Risk Profile", data["Risk Profile"])
        self.ln(3)

        # Section 3: Contributions
        section("Contribution Summary")
        row("Annual Salary", data["Salary"])
        row("Employer Contribution", data["Employer Contribution"])
        row("Employee Contribution", data["Employee Contribution"])
        row("Total Contribution", data["Total Contribution"])
        self.ln(3)

        # Section 4: Investment Information
        section("Investment Information")
        row("Fund Name", data["Fund Name"])
        row("Fund Performance", data["Fund Performance"])
        row("Current Pot Value", data["Pot Value"])
        self.ln(3)

        # Section 5: GDPR & Footer
        section("Privacy Notice")
        self.set_x(15)
        self.set_font("Arial", "", 10)
        self.multi_cell(180, 6, data.get("GDPR Notice", "—"))
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "Pension Portal Ltd. | Generated for personal use only | © 2025", 0, 0, "C")
