from pathlib import Path
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

DEFAULT_TERMS = [
    "The student shall follow the instructions of the host organization and the institution's internship coordinator.",
    "The student shall maintain professional conduct, confidentiality and attendance during the internship.",
    "The student shall submit periodic progress reports and a final internship report as directed by the institution.",
    "Any change in internship duration, role or organization must be reported to the institution for review.",
    "The internship completion and marks are subject to review of submitted work and applicable institutional requirements.",
]
DRAFT_NOTICE = "DRAFT TERMS: Replace these sample terms with the institution's approved internship rules before official use."

def generate_offer_letter(output_path, student, internship, application_id, terms=None):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="LetterTitle", parent=styles["Title"], alignment=TA_CENTER,
                              textColor=colors.HexColor("#153B5B"), fontSize=17, leading=22))
    story = [
        Paragraph("INTERNSHIP APPROVAL & OFFER LETTER", styles["LetterTitle"]),
        Spacer(1, 8),
        Paragraph(f"Reference: IAP/{application_id:04d} &nbsp;&nbsp;&nbsp; Date: {date.today().strftime('%d %B %Y')}", styles["Normal"]),
        Spacer(1, 14),
        Paragraph(f"To,<br/><b>{student['full_name']}</b><br/>Student ID: {student['student_id']}<br/>Department: {student['department']}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Subject: Approval and authorization for internship", styles["Heading2"]),
        Paragraph(
            f"This letter confirms that the internship application of <b>{student['full_name']}</b> "
            f"for <b>{internship['title']}</b> at <b>{internship['company']}</b> has received "
            "the required HOD and Internship Head approvals in the portal.",
            styles["BodyText"]
        ),
        Spacer(1, 10),
        Paragraph("<b>Internship details</b>", styles["Heading2"]),
    ]
    data = [
        ["Internship", internship["title"]],
        ["Organization", internship["company"]],
        ["Domain", internship["department"]],
        ["Duration", internship["duration"]],
        ["Mode", internship["mode"]],
        ["Expected hours", str(internship["total_hours"])],
    ]
    table = Table(data, colWidths=[125, 360])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#E7F0F6")),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#183047")),
        ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#B8C9D6")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("PADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story += [table, Spacer(1, 12), Paragraph("Terms and conditions", styles["Heading2"])]
    for idx, term in enumerate(terms or DEFAULT_TERMS, 1):
        story.append(Paragraph(f"{idx}. {term}", styles["BodyText"]))
        story.append(Spacer(1, 4))
    story += [
        Spacer(1, 8),
        Paragraph(f"<i>{DRAFT_NOTICE}</i>", styles["Italic"]),
        Spacer(1, 28),
    ]
    signature_data = [
        ["____________________________", "____________________________"],
        ["HOD", "Internship Head"],
        ["Institution", "Institution"],
    ]
    sig = Table(signature_data, colWidths=[242, 242])
    sig.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,1), (-1,1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#183047")),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(sig)
    SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=48, leftMargin=48,
                      topMargin=48, bottomMargin=48).build(story)
    return output_path
