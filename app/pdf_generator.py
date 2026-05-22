from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors


def generate_pdf(cv_data: dict, output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # =========================
    # Custom styles
    # =========================

    name_style = ParagraphStyle(
        name="Name",
        fontSize=18,
        leading=22,
        spaceAfter=6,
        textColor=colors.black,
        bold=True
    )

    header_style = ParagraphStyle(
        name="Header",
        fontSize=12,
        leading=14,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.black,
        bold=True
    )

    normal_style = ParagraphStyle(
        name="Normal",
        fontSize=10,
        leading=14,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        name="Bullet",
        fontSize=10,
        leftIndent=10,
        bulletIndent=0,
        spaceAfter=2
    )

    elements = []

    # =========================
    # HEADER
    # =========================

    elements.append(Paragraph(cv_data.get("name", ""), name_style))

    contact = " | ".join([
        cv_data.get("email", ""),
        cv_data.get("phone", ""),
        cv_data.get("location", "")
    ])

    elements.append(Paragraph(contact, normal_style))
    elements.append(Spacer(1, 10))

    # =========================
    # SUMMARY
    # =========================

    if cv_data.get("summary"):
        elements.append(Paragraph("PROFESSIONAL SUMMARY", header_style))
        elements.append(Paragraph(cv_data["summary"], normal_style))

    # =========================
    # EXPERIENCE
    # =========================

    if cv_data.get("experience"):
        elements.append(Paragraph("EXPERIENCE", header_style))

        for exp in cv_data["experience"]:
            title_line = f"<b>{exp.get('role')}</b> — {exp.get('company')} ({exp.get('dates')})"
            elements.append(Paragraph(title_line, normal_style))

            for bullet in exp.get("highlights", []):
                elements.append(Paragraph(f"• {bullet}", bullet_style))

            elements.append(Spacer(1, 6))

    # =========================
    # SKILLS
    # =========================

    if cv_data.get("skills"):
        elements.append(Paragraph("SKILLS", header_style))
        skills_text = ", ".join(cv_data["skills"])
        elements.append(Paragraph(skills_text, normal_style))

    # =========================
    # EDUCATION
    # =========================

    if cv_data.get("education"):
        elements.append(Paragraph("EDUCATION", header_style))

        for edu in cv_data["education"]:
            edu_line = f"<b>{edu.get('degree')}</b> — {edu.get('institution')} ({edu.get('dates')})"
            elements.append(Paragraph(edu_line, normal_style))

    doc.build(elements)