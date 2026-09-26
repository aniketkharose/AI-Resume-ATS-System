from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_ats_report(
    output_path: str | Path,
    ats_result: dict[str, Any],
    feedback: dict[str, Any],
    recommendations: dict[str, Any],
    filename: str = "Resume",
) -> str:
    """
    Generate a professional PDF ATS analysis report.

    The report contains:
    - Resume filename
    - Final ATS score
    - Component scores
    - Strengths
    - Missing skills
    - Related skills
    - Recommendations
    """

    output_path = Path(output_path)

    # --------------------------------------------------------
    # PDF document
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=5,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
    )

    story = []

    # ========================================================
    # HEADER
    # ========================================================

    story.append(
        Paragraph(
            "AI Resume ATS Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Resume: {filename}",
            subtitle_style,
        )
    )

    # ========================================================
    # ATS SCORE
    # ========================================================

    ats_score = ats_result.get(
        "ats_score",
        0,
    )

    story.append(
        Paragraph(
            "ATS SCORE",
            heading_style,
        )
    )

    score_table = Table(
        [
            [
                Paragraph(
                    f"<b>{ats_score}/100</b>",
                    ParagraphStyle(
                        "Score",
                        parent=styles["Normal"],
                        alignment=TA_CENTER,
                        fontSize=24,
                    ),
                )
            ]
        ],
        colWidths=[55 * mm],
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
            ]
        )
    )

    story.append(score_table)
    story.append(Spacer(1, 10))

    # ========================================================
    # COMPONENT SCORES
    # ========================================================

    story.append(
        Paragraph(
            "Score Breakdown",
            heading_style,
        )
    )

    components = ats_result.get(
        "components",
        {},
    )

    weights = ats_result.get(
        "weights",
        {},
    )

    weighted = ats_result.get(
        "weighted_contribution",
        {},
    )

    score_data = [
        [
            "Component",
            "Score",
            "Weight",
            "Contribution",
        ]
    ]

    for name, score in components.items():

        score_data.append(
            [
                name.replace(
                    "_",
                    " ",
                ).title(),
                f"{score}/100",
                f"{weights.get(name, 0)}%",
                f"+{weighted.get(name, 0)}",
            ]
        )

    score_table = Table(
        score_data,
        colWidths=[
            70 * mm,
            30 * mm,
            25 * mm,
            35 * mm,
        ],
        repeatRows=1,
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8.5,
                ),
            ]
        )
    )

    story.append(score_table)

    # ========================================================
    # SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Analysis Summary",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            feedback.get(
                "summary",
                "No summary available.",
            ),
            body_style,
        )
    )

    # ========================================================
    # STRENGTHS
    # ========================================================

    story.append(
        Paragraph(
            "Strengths",
            heading_style,
        )
    )

    strengths = feedback.get(
        "strengths",
        [],
    )

    if strengths:

        for strength in strengths:

            story.append(
                Paragraph(
                    f"• {strength}",
                    body_style,
                )
            )

    else:

        story.append(
            Paragraph(
                "No major strengths identified.",
                body_style,
            )
        )

    # ========================================================
    # MISSING SKILLS
    # ========================================================

    story.append(
        Paragraph(
            "Missing Skills",
            heading_style,
        )
    )

    missing_skills = feedback.get(
        "missing_skills",
        [],
    )

    if missing_skills:

        missing_data = [
            [
                "Skill",
                "Priority",
            ]
        ]

        for item in missing_skills:

            missing_data.append(
                [
                    item.get(
                        "skill",
                        "Unknown",
                    ),
                    item.get(
                        "priority",
                        "general",
                    ),
                ]
            )

        missing_table = Table(
            missing_data,
            colWidths=[
                100 * mm,
                45 * mm,
            ],
            repeatRows=1,
        )

        missing_table.setStyle(
            TableStyle(
                [
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            )
        )

        story.append(missing_table)

    else:

        story.append(
            Paragraph(
                "No missing JD skills detected.",
                body_style,
            )
        )

    # ========================================================
    # RELATED SKILLS
    # ========================================================

    related_skills = feedback.get(
        "related_skills",
        [],
    )

    if related_skills:

        story.append(
            Paragraph(
                "Related Skills",
                heading_style,
            )
        )

        for item in related_skills:

            story.append(
                Paragraph(
                    (
                        f"• {item.get('jd_skill')} "
                        f"→ {item.get('resume_skill')} "
                        f"(similarity: "
                        f"{item.get('similarity')})"
                    ),
                    body_style,
                )
            )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    story.append(
        Paragraph(
            "Recommendations",
            heading_style,
        )
    )

    all_recommendations = recommendations.get(
        "recommendations",
        [],
    )

    if all_recommendations:

        for item in all_recommendations:

            recommendation = item.get(
                "recommendation",
                "",
            )

            action = item.get(
                "suggested_action",
                "",
            )

            priority = item.get(
                "priority",
                "general",
            )

            story.append(
                Paragraph(
                    f"<b>[{priority.upper()}]</b> "
                    f"{recommendation}",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"Action: {action}",
                    small_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    4,
                )
            )

    else:

        story.append(
            Paragraph(
                "No major recommendations.",
                body_style,
            )
        )

    # ========================================================
    # FOOTER NOTE
    # ========================================================

    story.append(
        Spacer(
            1,
            15,
        )
    )

    story.append(
        Paragraph(
            "Generated by AI Resume ATS System.",
            small_style,
        )
    )

    document.build(story)

    return str(output_path)