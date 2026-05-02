#!/usr/bin/env python3
"""Generate a TOPdesk PBIP/PBIR report project from the exported TMDL model."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path


REPORT_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json"
PAGE_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
VISUAL_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"
PBIR_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json"
PBISM_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json"


def slug(value: str, max_len: int = 34) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "", value.title())
    return (cleaned or "Item")[:max_len]


def literal(value: str) -> dict:
    return {"expr": {"Literal": {"Value": value}}}


def text_literal(value: str) -> dict:
    return literal("'" + value.replace("'", "''") + "'")


def color_literal(value: str) -> dict:
    return {"solid": {"color": literal("'" + value + "'")}}


def measure(table: str, name: str) -> dict:
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": name,
        }
    }


def column(table: str, name: str) -> dict:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": name,
        }
    }


def projection(field: dict, query_ref: str, display_name: str | None = None) -> dict:
    item = {"field": field, "queryRef": query_ref}
    if display_name:
        item["displayName"] = display_name
    return item


def title_objects(title: str, subtitle: str | None = None) -> dict:
    objects = {
        "title": [
            {
                "properties": {
                    "show": literal("true"),
                    "text": text_literal(title),
                    "fontSize": literal("13D"),
                    "bold": literal("true"),
                    "fontColor": color_literal("#1D2939"),
                    "titleWrap": literal("true"),
                }
            }
        ],
        "background": [
            {
                "properties": {
                    "show": literal("true"),
                    "color": color_literal("#FFFFFF"),
                    "transparency": literal("0D"),
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": literal("true"),
                    "color": color_literal("#D0D5DD"),
                    "radius": literal("4D"),
                }
            }
        ],
        "visualHeader": [{"properties": {"show": literal("false")}}],
    }
    if subtitle:
        objects["subTitle"] = [
            {
                "properties": {
                    "show": literal("true"),
                    "text": text_literal(subtitle),
                    "fontSize": literal("9D"),
                    "fontColor": color_literal("#667085"),
                }
            }
        ]
    return objects


def visual_container(name: str, visual_type: str, x: int, y: int, width: int, height: int, z: int, query: dict | None, title: str, subtitle: str | None = None) -> dict:
    visual = {
        "visualType": visual_type,
        "visualContainerObjects": title_objects(title, subtitle),
    }
    if query:
        visual["query"] = query
    return {
        "$schema": VISUAL_SCHEMA,
        "name": name,
        "position": {"x": x, "y": y, "z": z, "width": width, "height": height, "tabOrder": z},
        "visual": visual,
    }


def textbox(name: str, x: int, y: int, width: int, height: int, z: int, title: str, body: str) -> dict:
    return visual_container(name, "textbox", x, y, width, height, z, None, title, body)


def card(name: str, x: int, y: int, title: str, measure_name: str, subtitle: str = "") -> dict:
    return visual_container(
        name,
        "cardVisual",
        x,
        y,
        276,
        105,
        int(name[-2:], 16) if re.search(r"[0-9A-Fa-f]{2}$", name) else 10,
        {
            "queryState": {
                "Values": {
                    "projections": [
                        projection(measure("FactIncident", measure_name), f"FactIncident.{measure_name}", title)
                    ]
                }
            }
        },
        title,
        subtitle or measure_name,
    )


def bar(name: str, x: int, y: int, width: int, height: int, title: str, category_table: str, category_col: str, measure_name: str) -> dict:
    return visual_container(
        name,
        "barChart",
        x,
        y,
        width,
        height,
        int(name[-2:], 16) if re.search(r"[0-9A-Fa-f]{2}$", name) else 30,
        {
            "queryState": {
                "Category": {
                    "projections": [
                        projection(column(category_table, category_col), f"{category_table}.{category_col}", category_col)
                    ]
                },
                "Y": {
                    "projections": [
                        projection(measure("FactIncident", measure_name), f"FactIncident.{measure_name}", measure_name)
                    ]
                },
            }
        },
        title,
        f"{measure_name} by {category_col}",
    )


def line(name: str, x: int, y: int, width: int, height: int, title: str, measure_name: str) -> dict:
    return visual_container(
        name,
        "lineChart",
        x,
        y,
        width,
        height,
        int(name[-2:], 16) if re.search(r"[0-9A-Fa-f]{2}$", name) else 40,
        {
            "queryState": {
                "Category": {
                    "projections": [projection(column("DimDate", "Date"), "DimDate.Date", "Date")]
                },
                "Y": {
                    "projections": [
                        projection(measure("FactIncident", measure_name), f"FactIncident.{measure_name}", measure_name)
                    ]
                },
            },
            "sortDefinition": {
                "sort": [{"field": column("DimDate", "Date"), "direction": "Ascending"}],
                "isDefaultSort": False,
            },
        },
        title,
        f"Trend: {measure_name}",
    )


def table(name: str, x: int, y: int, width: int, height: int, title: str, fields: list[tuple[str, str, str]]) -> dict:
    projections = []
    for table_name, field_type, field_name in fields:
        if field_type == "measure":
            field = measure(table_name, field_name)
        else:
            field = column(table_name, field_name)
        projections.append(projection(field, f"{table_name}.{field_name}", field_name))
    return visual_container(
        name,
        "tableEx",
        x,
        y,
        width,
        height,
        int(name[-2:], 16) if re.search(r"[0-9A-Fa-f]{2}$", name) else 50,
        {"queryState": {"Values": {"projections": projections}}},
        title,
        "Detail- und Governance-Liste",
    )


def generic_visual(name: str, visual_type: str, x: int, y: int, width: int, height: int, title: str, roles: dict[str, list[tuple[str, str, str]]], subtitle: str = "") -> dict:
    query_state = {}
    for role_name, fields in roles.items():
        role_projections = []
        for table_name, field_type, field_name in fields:
            field = measure(table_name, field_name) if field_type == "measure" else column(table_name, field_name)
            role_projections.append(projection(field, f"{table_name}.{field_name}", field_name))
        query_state[role_name] = {"projections": role_projections}
    return visual_container(
        name,
        visual_type,
        x,
        y,
        width,
        height,
        int(name[-2:], 16) if re.search(r"[0-9A-Fa-f]{2}$", name) else 70,
        {"queryState": query_state} if query_state else None,
        title,
        subtitle or visual_type,
    )


def slicer(name: str, x: int, y: int, width: int, height: int, title: str, table_name: str, column_name: str) -> dict:
    return generic_visual(name, "slicer", x, y, width, height, title, {"Values": [(table_name, "column", column_name)]}, column_name)


def matrix(name: str, x: int, y: int, width: int, height: int, title: str, row_table: str, row_col: str, value_measure: str, col_table: str | None = None, col_name: str | None = None) -> dict:
    roles = {
        "Rows": [(row_table, "column", row_col)],
        "Values": [("FactIncident", "measure", value_measure)],
    }
    if col_table and col_name:
        roles["Columns"] = [(col_table, "column", col_name)]
    return generic_visual(name, "pivotTable", x, y, width, height, title, roles, value_measure)


def donut(name: str, x: int, y: int, width: int, height: int, title: str, category_table: str, category_col: str, value_measure: str) -> dict:
    return generic_visual(
        name,
        "donutChart",
        x,
        y,
        width,
        height,
        title,
        {"Category": [(category_table, "column", category_col)], "Y": [("FactIncident", "measure", value_measure)]},
        f"{value_measure} by {category_col}",
    )


def gauge(name: str, x: int, y: int, width: int, height: int, title: str, value_measure: str) -> dict:
    return generic_visual(name, "gauge", x, y, width, height, title, {"Y": [("FactIncident", "measure", value_measure)]}, value_measure)


def scatter(name: str, x: int, y: int, width: int, height: int, title: str, category_table: str, category_col: str, x_measure: str, y_measure: str, size_measure: str) -> dict:
    return generic_visual(
        name,
        "scatterChart",
        x,
        y,
        width,
        height,
        title,
        {
            "Category": [(category_table, "column", category_col)],
            "X": [("FactIncident", "measure", x_measure)],
            "Y": [("FactIncident", "measure", y_measure)],
            "Size": [("FactIncident", "measure", size_measure)],
        },
        f"{x_measure} vs {y_measure}",
    )


def decomposition_tree(name: str, x: int, y: int, width: int, height: int, title: str, analyze_measure: str) -> dict:
    return generic_visual(
        name,
        "decompositionTree",
        x,
        y,
        width,
        height,
        title,
        {
            "Analyze": [("FactIncident", "measure", analyze_measure)],
            "ExplainBy": [
                ("FactIncident", "column", "Priority"),
                ("FactIncident", "column", "Category"),
                ("FactIncident", "column", "OperatorGroup"),
                ("FactIncident", "column", "Branch"),
            ],
        },
        "Explain-by drill path",
    )


def key_influencers(name: str, x: int, y: int, width: int, height: int, title: str, analyze_measure: str) -> dict:
    return generic_visual(
        name,
        "keyDriversVisual",
        x,
        y,
        width,
        height,
        title,
        {
            "Analyze": [("FactIncident", "measure", analyze_measure)],
            "ExplainBy": [
                ("FactIncident", "column", "Priority"),
                ("FactIncident", "column", "Category"),
                ("FactIncident", "column", "Status"),
                ("FactIncident", "column", "OperatorGroup"),
            ],
        },
        "Drivers and segments",
    )


def narrative(name: str, x: int, y: int, width: int, height: int, title: str, primary_measure: str) -> dict:
    return generic_visual(
        name,
        "smartNarrative",
        x,
        y,
        width,
        height,
        title,
        {"Values": [("FactIncident", "measure", primary_measure), ("FactIncident", "measure", "Executive Risk Index"), ("FactIncident", "measure", "Value Protection Score")]},
        "Auto narrative inputs",
    )


def qna(name: str, x: int, y: int, width: int, height: int, title: str) -> dict:
    return visual_container(name, "qnaVisual", x, y, width, height, 90, None, title, "Natural language question entry")


def standard_support_visuals(page: dict, ordinal: int, start_z: int) -> dict[str, dict]:
    visuals: dict[str, dict] = {}
    threshold_id = f"Threshold{ordinal:02d}"
    visuals[threshold_id] = table(
        threshold_id,
        24,
        712,
        392,
        136,
        "KPI Thresholds",
        [
            ("KPIThreshold", "column", "KPI"),
            ("KPIThreshold", "column", "Green"),
            ("KPIThreshold", "column", "Red"),
        ],
    )
    action_id = f"Action{ordinal:02d}"
    visuals[action_id] = table(
        action_id,
        444,
        712,
        392,
        136,
        "Action Playbook",
        [
            ("ActionPlaybook", "column", "Priority"),
            ("ActionPlaybook", "column", "Trigger"),
            ("ActionPlaybook", "column", "Owner"),
        ],
    )
    nav_id = f"Nav{ordinal:02d}"
    visuals[nav_id] = table(
        nav_id,
        864,
        712,
        392,
        136,
        "Navigation & Tooltip Guide",
        [
            ("PageNavigationCatalog", "column", "From Page"),
            ("PageNavigationCatalog", "column", "Target Page"),
            ("PageNavigationCatalog", "column", "Button Label"),
        ],
    )
    for idx, visual in enumerate(visuals.values(), start=start_z):
        visual["position"]["z"] = idx
        visual["position"]["tabOrder"] = idx
    return visuals


def advanced_visuals(page: dict, ordinal: int, start_z: int) -> dict[str, dict]:
    visuals: dict[str, dict] = {}
    primary_measure = page["cards"][0][1]
    secondary_measure = page["cards"][1][1]
    tertiary_measure = page["cards"][2][1]
    bar_title, category_table, category_col, bar_measure = page["bar"]
    visuals[f"SlicerDate{ordinal:02d}"] = slicer(f"SlicerDate{ordinal:02d}", 24, 872, 184, 96, "Date", "DimDate", "Date")
    visuals[f"SlicerGroup{ordinal:02d}"] = slicer(f"SlicerGroup{ordinal:02d}", 224, 872, 184, 96, "Operator Group", "DimOperatorGroup", "OperatorGroup")
    visuals[f"SlicerPriority{ordinal:02d}"] = slicer(f"SlicerPriority{ordinal:02d}", 424, 872, 184, 96, "Priority", "FactIncident", "Priority")
    visuals[f"SlicerCategory{ordinal:02d}"] = slicer(f"SlicerCategory{ordinal:02d}", 624, 872, 184, 96, "Category", "FactIncident", "Category")
    visuals[f"SlicerDomain{ordinal:02d}"] = slicer(f"SlicerDomain{ordinal:02d}", 824, 872, 184, 96, "ITIL Domain", "ITILV5KPICatalog", "ITIL V5 Domain")
    visuals[f"SlicerStatus{ordinal:02d}"] = slicer(f"SlicerStatus{ordinal:02d}", 1024, 872, 232, 96, "Status", "FactIncident", "Status")
    visuals[f"Matrix{ordinal:02d}"] = matrix(f"Matrix{ordinal:02d}", 24, 992, 392, 220, "Matrix: Domain x Maturity", "ITILV5KPICatalog", "ITIL V5 Domain", primary_measure, "ITILV5KPICatalog", "Maturity")
    visuals[f"Donut{ordinal:02d}"] = donut(f"Donut{ordinal:02d}", 444, 992, 392, 220, "Distribution", category_table, category_col, bar_measure)
    visuals[f"Gauge{ordinal:02d}"] = gauge(f"Gauge{ordinal:02d}", 864, 992, 392, 220, "Gauge: " + page["cards"][0][0], primary_measure)
    visuals[f"Scatter{ordinal:02d}"] = scatter(f"Scatter{ordinal:02d}", 24, 1236, 392, 240, "Risk vs Value", category_table, category_col, "Executive Risk Index", "Value Protection Score", "Incident Count")
    visuals[f"Decomp{ordinal:02d}"] = decomposition_tree(f"Decomp{ordinal:02d}", 444, 1236, 392, 240, "Decomposition: " + page["cards"][0][0], primary_measure)
    visuals[f"KeyInf{ordinal:02d}"] = key_influencers(f"KeyInf{ordinal:02d}", 864, 1236, 392, 240, "Key Influencers", tertiary_measure)
    visuals[f"Narrative{ordinal:02d}"] = narrative(f"Narrative{ordinal:02d}", 24, 1500, 604, 132, "Smart Narrative", primary_measure)
    visuals[f"Qna{ordinal:02d}"] = qna(f"Qna{ordinal:02d}", 652, 1500, 604, 132, "Q&A")
    for idx, visual in enumerate(visuals.values(), start=start_z):
        visual["position"]["z"] = idx
        visual["position"]["tabOrder"] = idx
    return visuals


PAGES = [
    {
        "name": "Executive Overview",
        "summary": "Board-faehiger Einstieg fuer Service Health, SLA-Risiko, Datenqualitaet und TOPdesk-Steuerung.",
        "cards": [
            ("Incident Count", "Incident Count"),
            ("Open Backlog", "Open Incident Count"),
            ("Service Control", "ITIL Service Control Score"),
            ("Data Foundation", "Data Foundation Score"),
        ],
        "bar": ("Backlog nach Gruppe", "DimOperatorGroup", "OperatorGroup", "Open Incident Count"),
        "line": ("Incident Trend", "Incident Count"),
        "table": ("Executive Entscheidungslog", [("LeadershipQuestion", "column", "Question"), ("LeadershipQuestion", "column", "Decision"), ("LeadershipQuestion", "column", "Primary Measure")]),
    },
    {
        "name": "Service Leadership Cockpit",
        "summary": "Fuehrungssicht fuer Ownership, Routing, Eskalation und Management-Fragen.",
        "cards": [
            ("Routing Coverage", "Routing Coverage %"),
            ("Priority Coverage", "Priority Coverage %"),
            ("Category Coverage", "Category Coverage %"),
            ("Leadership Score", "ITIL Service Control Score"),
        ],
        "bar": ("Routing-Risiko nach Gruppe", "DimOperatorGroup", "OperatorGroup", "Unrouted Incident Count"),
        "line": ("Service Control Trend", "ITIL Service Control Score"),
        "table": ("Leadership Questions", [("LeadershipQuestion", "column", "Question"), ("LeadershipQuestion", "column", "Evidence"), ("LeadershipQuestion", "column", "Decision")]),
    },
    {
        "name": "SLA OLA XLA",
        "summary": "Verbindet SLA-Abdeckung, interne OLA-Steuerung und Experience-Risiko.",
        "cards": [
            ("Missing Target Dates", "Missing Target Date Count"),
            ("Target Date Coverage", "Target Date Coverage %"),
            ("Experience Risk", "ITIL Experience Risk %"),
            ("Experience Health", "ITIL Experience Health Score"),
        ],
        "bar": ("SLA-Risiko nach Prioritaet", "FactIncident", "Priority", "Missing Target Date Count"),
        "line": ("Experience Health Trend", "ITIL Experience Health Score"),
        "table": ("SLA OLA XLA Lens", [("SLAOLAXLALens", "column", "Lens"), ("SLAOLAXLALens", "column", "KPI"), ("SLAOLAXLALens", "column", "Meaning")]),
    },
    {
        "name": "Operations Control",
        "summary": "Operative Last, offene Arbeit, Triage-Qualitaet und No-Owner-Risiken.",
        "cards": [
            ("Open Incidents", "Open Incident Count"),
            ("Closed Incidents", "Closed Incident Count"),
            ("Unrouted", "Unrouted Incident Count"),
            ("Open Backlog %", "Open Backlog %"),
        ],
        "bar": ("Backlog nach Branch", "DimBranch", "Branch", "Open Incident Count"),
        "line": ("Open Backlog Trend", "Open Backlog %"),
        "table": ("Action Playbook", [("ActionPlaybook", "column", "Trigger"), ("ActionPlaybook", "column", "Recommended Action"), ("ActionPlaybook", "column", "Owner")]),
    },
    {
        "name": "Problem Major Incident Radar",
        "summary": "Erkennt Wiederholer, Major-Incident-Kandidaten, Schwachstellen und Problem-Backlog.",
        "cards": [
            ("Problem Coverage", "Problem Candidate Coverage %"),
            ("Flow Blockers", "Flow Blocker Count"),
            ("Reliability Risk", "Reliability Risk %"),
            ("Executive Risk", "Executive Risk Index"),
        ],
        "bar": ("Problem-Signal nach Kategorie", "FactIncident", "Category", "Problem Candidate Coverage %"),
        "line": ("Reliability Risk Trend", "Reliability Risk %"),
        "table": ("Major Problem Radar", [("MajorProblemRadar", "column", "Radar Area"), ("MajorProblemRadar", "column", "Signal"), ("MajorProblemRadar", "column", "Leadership Action")]),
    },
    {
        "name": "Change Risk Stability",
        "summary": "Change-nahe Stoerungen, Stabilitaet, Risiko-Hotspots und Service-Impact.",
        "cards": [
            ("Change Stability", "Change Stability Score"),
            ("Stability Score", "Change Stability Score"),
            ("Reliability Proxy", "Operational Reliability Proxy"),
            ("Service Commitment", "Service Commitment Coverage %"),
        ],
        "bar": ("Change-Risiko nach Service", "FactIncident", "Category", "Change Stability Score"),
        "line": ("Stability Trend", "Change Stability Score"),
        "table": ("Change Stability Lens", [("ChangeStabilityLens", "column", "KPI"), ("ChangeStabilityLens", "column", "Meaning"), ("ChangeStabilityLens", "column", "Leadership Use")]),
    },
    {
        "name": "Knowledge Deflection",
        "summary": "Wissensartikel, Shift-left, Self-Service-Potenzial und Deflection-Luecken.",
        "cards": [
            ("Knowledge Readiness", "Knowledge Deflection Readiness %"),
            ("Automation Candidates", "Automation Candidate Incidents"),
            ("Automation Candidate %", "Automation Candidate %"),
            ("Automation Unlock", "Automation Unlock Score"),
        ],
        "bar": ("Knowledge-Potenzial nach Kategorie", "FactIncident", "Category", "Knowledge Deflection Readiness %"),
        "line": ("Deflection Trend", "Knowledge Deflection Readiness %"),
        "table": ("Knowledge Deflection Lens", [("KnowledgeDeflectionLens", "column", "KPI"), ("KnowledgeDeflectionLens", "column", "Meaning"), ("KnowledgeDeflectionLens", "column", "Leadership Use")]),
    },
    {
        "name": "Continual Improvement Board",
        "summary": "CSI-Register mit Nutzen, Aufwand, Ownern, Hypothesen und messbaren Outcomes.",
        "cards": [
            ("CSI Initiatives", "CSI Initiative Count"),
            ("CSI Ratio", "CSI Conversion Ratio"),
            ("CSI Pressure Gap", "CSI Pressure Gap"),
            ("Value Score", "Value Realization Score"),
        ],
        "bar": ("Verbesserung nach Hebel", "ValueLever", "Lever", "Value Realization Score"),
        "line": ("CSI Trend", "CSI Conversion Ratio"),
        "table": ("CSI Register", [("ContinualImprovementRegister", "column", "Initiative"), ("ContinualImprovementRegister", "column", "Expected Benefit"), ("ContinualImprovementRegister", "column", "Owner")]),
    },
    {
        "name": "Cost Value Of Service",
        "summary": "Wertbeitrag, Kostenhebel, Nachfrage, Automatisierung und Service-Portfolio-Signale.",
        "cards": [
            ("Demand Score", "Demand Structuring Score"),
            ("Cost Readiness", "Cost Reporting Readiness %"),
            ("Value Leakage", "Value Leakage Proxy"),
            ("Value Protection", "Value Protection Score"),
        ],
        "bar": ("Value Lever", "ValueLever", "Lever", "Value Realization Score"),
        "line": ("Value Protection Trend", "Value Protection Score"),
        "table": ("Cost Value Lens", [("CostValueLens", "column", "Value Metric"), ("CostValueLens", "column", "Formula Idea"), ("CostValueLens", "column", "Leadership Use")]),
    },
    {
        "name": "ITIL V5 KPI Portfolio",
        "summary": "ITIL-v5-KPI-Katalog fuer Service, Product, Experience, Risk, Partner und Governance.",
        "cards": [
            ("Service Score", "ITIL Service Control Score"),
            ("Product Score", "ITIL Product Health Score"),
            ("Experience Score", "ITIL Experience Health Score"),
            ("Governance Score", "Governed Reporting Confidence"),
        ],
        "bar": ("ITIL Practice Coverage", "ITILV5KPICatalog", "ITIL V5 Domain", "ITIL Service Control Score"),
        "line": ("Governance Trend", "Governed Reporting Confidence"),
        "table": ("ITIL V5 KPI Catalog", [("ITILV5KPICatalog", "column", "ITIL V5 Domain"), ("ITILV5KPICatalog", "column", "KPI"), ("ITILV5KPICatalog", "column", "Leadership Question")]),
    },
    {
        "name": "AI Governance Readiness",
        "summary": "AI-readiness fuer Datenschutz, Grounding, Data Contracts, Monitoring und Freigaben.",
        "cards": [
            ("AI Governance Risk", "AI Governance Risk %"),
            ("Data Foundation", "Data Foundation Score"),
            ("Data Contracts", "Data Contract Count"),
            ("AI Readiness", "AI Readiness Score"),
        ],
        "bar": ("AI Readiness nach Contract", "DataContractRegistry", "Contract", "AI Readiness Score"),
        "line": ("AI Readiness Trend", "AI Readiness Score"),
        "table": ("Data Contracts", [("DataContractRegistry", "column", "Contract"), ("DataContractRegistry", "column", "Producer"), ("DataContractRegistry", "column", "Consumer")]),
    },
    {
        "name": "Production Readiness",
        "summary": "Betriebsreife fuer RLS, Refresh, Alerts, Drillthrough, Release und Monitoring.",
        "cards": [
            ("Production Score", "Production Readiness Score"),
            ("Security Coverage", "Security Design Coverage"),
            ("Refresh Checks", "Refresh Ops Check Count"),
            ("Release Gates", "Release Gate Count"),
        ],
        "bar": ("Readiness nach Bereich", "ProductionReadinessMatrix", "Readiness Area", "Production Readiness Score"),
        "line": ("Production Readiness Trend", "Production Readiness Score"),
        "table": ("Production Readiness Matrix", [("ProductionReadinessMatrix", "column", "Readiness Area"), ("ProductionReadinessMatrix", "column", "Capability"), ("ProductionReadinessMatrix", "column", "Target State")]),
    },
    {
        "name": "ITIL V5 Operating Model",
        "summary": "Operating-Model-Sicht fuer Incident, Service Desk, Ownership, SLA, Measurement und Risk Treatment.",
        "cards": [
            ("Operating Model", "ITIL V5 Operating Model Score"),
            ("Incident Lifecycle", "Incident Lifecycle Completeness"),
            ("Triage Quality", "Triage Quality Score"),
            ("Ownership Health", "Service Ownership Health"),
        ],
        "bar": ("Operating KPIs nach ITIL Domain", "ITILV5KPICatalog", "ITIL V5 Domain", "ITIL V5 Operating Model Score"),
        "line": ("Operating Model Trend", "ITIL V5 Operating Model Score"),
        "table": ("Operating Model KPI Catalog", [("ITILV5KPICatalog", "column", "ITIL V5 Domain"), ("ITILV5KPICatalog", "column", "KPI"), ("ITILV5KPICatalog", "column", "Current Measure")]),
    },
    {
        "name": "ITIL V5 Practice Maturity",
        "summary": "Practice-Reife fuer Knowledge, Problem, Change, Supplier, Portfolio und Sustainability.",
        "cards": [
            ("Knowledge Practice", "Knowledge Practice Readiness"),
            ("Problem Control", "Problem Control Score"),
            ("Change Enablement", "Change Enablement Readiness"),
            ("Supplier Accountability", "Supplier Accountability Score"),
        ],
        "bar": ("Practice Maturity nach Domain", "ITILV5KPICatalog", "ITIL V5 Domain", "Practice Coverage Score"),
        "line": ("Practice Coverage Trend", "Practice Coverage Score"),
        "table": ("Practice Maturity KPIs", [("ITILV5KPICatalog", "column", "ITIL V5 Domain"), ("ITILV5KPICatalog", "column", "Leadership Question"), ("ITILV5KPICatalog", "column", "Needed Next Data")]),
    },
    {
        "name": "ITIL V5 Risk Value Governance",
        "summary": "Executive-Sicht auf Risk Treatment, Measurement Health, Observability, Value Protection und Improvement Priority.",
        "cards": [
            ("Risk Treatment", "Risk Treatment Readiness"),
            ("Measurement Health", "Measurement System Health"),
            ("Observability", "Operational Observability Score"),
            ("Improvement Priority", "ITIL V5 Improvement Priority Index"),
        ],
        "bar": ("Risk & Value nach ITIL Domain", "ITILV5KPICatalog", "ITIL V5 Domain", "Value Protection Score"),
        "line": ("Measurement Health Trend", "Measurement System Health"),
        "table": ("Risk Value Governance KPIs", [("ITILV5KPICatalog", "column", "ITIL V5 Domain"), ("ITILV5KPICatalog", "column", "Maturity"), ("ITILV5KPICatalog", "column", "Needed Next Data")]),
    },
]


DRILLTHROUGH_PAGES = [
    {
        "name": "DT Incident Detail",
        "summary": "Drillthrough fuer einzelne Incidents, Status, Prioritaet, Kategorie, Zieltermin und Ownership.",
        "cards": [("Incident Count", "Incident Count"), ("Open Backlog", "Open Incident Count"), ("Lifecycle", "Incident Lifecycle Completeness"), ("Triage", "Triage Quality Score")],
        "bar": ("Incidents nach Status", "FactIncident", "Status", "Incident Count"),
        "line": ("Incident Trend", "Incident Count"),
        "table": ("Incident Detail", [("FactIncident", "column", "IncidentNumber"), ("FactIncident", "column", "Status"), ("FactIncident", "column", "Priority"), ("FactIncident", "column", "Category"), ("FactIncident", "column", "OperatorGroup")]),
        "type": "Drillthrough",
    },
    {
        "name": "DT SLA Breach Detail",
        "summary": "Drillthrough fuer SLA-Risiko, fehlende Zieltermine, Service Commitments und Experience-Friction.",
        "cards": [("Missing Targets", "Missing Target Date Count"), ("SLA Stewardship", "SLA Stewardship Score"), ("Experience Risk", "ITIL Experience Risk %"), ("Commitment Coverage", "Service Commitment Coverage %")],
        "bar": ("SLA-Risiko nach Prioritaet", "FactIncident", "Priority", "Missing Target Date Count"),
        "line": ("SLA Stewardship Trend", "SLA Stewardship Score"),
        "table": ("SLA Findings", [("SLAFinding", "column", "incident"), ("SLAFinding", "column", "severity"), ("SLAFinding", "column", "finding"), ("SLAFinding", "column", "action")]),
        "type": "Drillthrough",
    },
    {
        "name": "DT Data Quality Detail",
        "summary": "Drillthrough fuer fehlende Felder, Datenvertrag, Data Foundation und Automatisierungsrisiko.",
        "cards": [("Data Foundation", "Data Foundation Score"), ("Quality Load", "Improvement Backlog Items"), ("Structured Coverage", "Structured Data Coverage %"), ("AI Window", "AI Safe Automation Window")],
        "bar": ("Findings nach Severity", "DataQualityFindings", "severity", "Improvement Backlog Items"),
        "line": ("Data Foundation Trend", "Data Foundation Score"),
        "table": ("Data Quality Findings", [("DataQualityFindings", "column", "entity"), ("DataQualityFindings", "column", "field"), ("DataQualityFindings", "column", "severity"), ("DataQualityFindings", "column", "details")]),
        "type": "Drillthrough",
    },
    {
        "name": "DT PII Compliance Detail",
        "summary": "Drillthrough fuer PII-Findings, Governance, Reporting Confidence und Publish-Blocker.",
        "cards": [("PII Exposure", "AI Governance Risk %"), ("Publish Blockers", "Publish Blocker Count"), ("AI Gov Risk", "AI Governance Risk %"), ("Governance", "Governed Reporting Confidence")],
        "bar": ("PII nach Severity", "PIIFinding", "severity", "Publish Blocker Count"),
        "line": ("Governance Trend", "Governed Reporting Confidence"),
        "table": ("PII Findings", [("PIIFinding", "column", "entity"), ("PIIFinding", "column", "field"), ("PIIFinding", "column", "severity"), ("PIIFinding", "column", "recommendation")]),
        "type": "Drillthrough",
    },
    {
        "name": "DT Operator Group Detail",
        "summary": "Drillthrough fuer Queue-/Team-Performance, Routing, Swarming und Backlog-Containment.",
        "cards": [("Routing", "Routing Coverage %"), ("Swarming", "Swarming Readiness Score"), ("Backlog Containment", "Backlog Containment Score"), ("Open Backlog", "Open Incident Count")],
        "bar": ("Backlog nach Gruppe", "DimOperatorGroup", "OperatorGroup", "Open Incident Count"),
        "line": ("Flow Trend", "Flow Efficiency Proxy"),
        "table": ("Operator Groups", [("DimOperatorGroup", "column", "OperatorGroup"), ("DimOperatorGroup", "column", "Branch"), ("DimOperatorGroup", "column", "FirstLine"), ("DimOperatorGroup", "column", "SecondLine")]),
        "type": "Drillthrough",
    },
    {
        "name": "DT Service Category Detail",
        "summary": "Drillthrough fuer Service Portfolio, Kategorien, Nachfrage, Knowledge und Problem Control.",
        "cards": [("Demand", "Demand Structuring Score"), ("Portfolio Signal", "Service Portfolio Signal Score"), ("Knowledge", "Knowledge Practice Readiness"), ("Problem Control", "Problem Control Score")],
        "bar": ("Incidents nach Kategorie", "FactIncident", "Category", "Incident Count"),
        "line": ("Portfolio Signal Trend", "Service Portfolio Signal Score"),
        "table": ("Category Detail", [("FactIncident", "column", "Category"), ("FactIncident", "column", "Subcategory"), ("FactIncident", "column", "Priority"), ("FactIncident", "column", "Status")]),
        "type": "Drillthrough",
    },
]


TOOLTIP_PAGES = [
    ("TT Executive KPI", "Executive KPI tooltip mit Health, Risk, Value und Operating Model.", [("Health", "Executive Health Index"), ("Risk", "Executive Risk Index"), ("Value", "Value Realization Score"), ("Operating", "ITIL V5 Operating Model Score")]),
    ("TT SLA Risk", "SLA tooltip mit Stewardship, Experience, Missing Targets und Commitment.", [("Stewardship", "SLA Stewardship Score"), ("Experience", "ITIL Experience Health Score"), ("Missing", "Missing Target Date Count"), ("Commitment", "Service Commitment Coverage %")]),
    ("TT Data Quality", "Data-quality tooltip mit Foundation, Coverage, Findings und AI Window.", [("Foundation", "Data Foundation Score"), ("Coverage", "Structured Data Coverage %"), ("Finding Load", "Improvement Backlog Items"), ("AI Window", "AI Safe Automation Window")]),
    ("TT AI Governance", "AI governance tooltip mit Readiness, Risk, PII und Confidence.", [("Readiness", "AI Readiness Score"), ("AI Risk", "AI Governance Risk %"), ("Blockers", "Publish Blocker Count"), ("Confidence", "Governed Reporting Confidence")]),
    ("TT ITIL Practice", "ITIL practice tooltip mit Knowledge, Problem, Change und Supplier.", [("Knowledge", "Knowledge Practice Readiness"), ("Problem", "Problem Control Score"), ("Change", "Change Enablement Readiness"), ("Supplier", "Supplier Accountability Score")]),
    ("TT Production", "Production tooltip mit readiness, controls, ops and security.", [("Production", "Production Readiness Score"), ("Controls", "Control Framework Coverage"), ("Ops", "Operationalization Coverage"), ("Security", "Security Design Coverage")]),
]


def build_page(page: dict, ordinal: int) -> tuple[str, dict, dict[str, dict]]:
    page_id = f"ReportSection{ordinal:02d}{slug(page['name'], 18)}"
    visuals: dict[str, dict] = {}
    z = 1
    visuals[f"Title{ordinal:02d}"] = textbox(f"Title{ordinal:02d}", 24, 16, 1232, 64, z, page["name"], page["summary"])
    z += 1
    x_positions = [24, 332, 640, 948]
    for idx, (title, measure_name) in enumerate(page["cards"], start=1):
        visual_id = f"Kpi{ordinal:02d}{idx:02d}"
        visuals[visual_id] = card(visual_id, x_positions[idx - 1], 100, title, measure_name)
        visuals[visual_id]["position"]["z"] = z
        visuals[visual_id]["position"]["tabOrder"] = z
        z += 1
    bar_title, cat_table, cat_col, bar_measure = page["bar"]
    visuals[f"Bar{ordinal:02d}"] = bar(f"Bar{ordinal:02d}", 24, 230, 584, 300, bar_title, cat_table, cat_col, bar_measure)
    visuals[f"Bar{ordinal:02d}"]["position"]["z"] = z
    visuals[f"Bar{ordinal:02d}"]["position"]["tabOrder"] = z
    z += 1
    line_title, line_measure = page["line"]
    visuals[f"Line{ordinal:02d}"] = line(f"Line{ordinal:02d}", 640, 230, 616, 300, line_title, line_measure)
    visuals[f"Line{ordinal:02d}"]["position"]["z"] = z
    visuals[f"Line{ordinal:02d}"]["position"]["tabOrder"] = z
    z += 1
    table_title, fields = page["table"]
    visuals[f"Table{ordinal:02d}"] = table(f"Table{ordinal:02d}", 24, 548, 1232, 152, table_title, fields)
    visuals[f"Table{ordinal:02d}"]["position"]["z"] = z
    visuals[f"Table{ordinal:02d}"]["position"]["tabOrder"] = z
    z += 1
    visuals.update(standard_support_visuals(page, ordinal, z))
    z += 3
    visuals.update(advanced_visuals(page, ordinal, z))

    page_json = {
        "$schema": PAGE_SCHEMA,
        "name": page_id,
        "displayName": page["name"],
        "displayOption": "FitToPage",
        "height": 1660,
        "width": 1280,
        "annotations": [
            {"name": "ordinal", "value": str(ordinal)},
            {"name": "purpose", "value": page["summary"]},
        ],
    }
    return page_id, page_json, visuals


def build_tooltip_page(page: tuple[str, str, list[tuple[str, str]]], ordinal: int) -> tuple[str, dict, dict[str, dict]]:
    name, summary, cards = page
    page_id = f"ReportSection{ordinal:02d}{slug(name, 18)}"
    visuals: dict[str, dict] = {}
    visuals[f"Title{ordinal:02d}"] = textbox(f"Title{ordinal:02d}", 12, 8, 456, 52, 1, name, summary)
    x_positions = [12, 244, 12, 244]
    y_positions = [72, 72, 190, 190]
    for idx, (title, measure_name) in enumerate(cards, start=1):
        visual_id = f"TtKpi{ordinal:02d}{idx:02d}"
        visuals[visual_id] = card(visual_id, x_positions[idx - 1], y_positions[idx - 1], title, measure_name)
        visuals[visual_id]["position"]["width"] = 224
        visuals[visual_id]["position"]["height"] = 104
        visuals[visual_id]["position"]["z"] = idx + 1
        visuals[visual_id]["position"]["tabOrder"] = idx + 1
    table_id = f"TtTable{ordinal:02d}"
    visuals[table_id] = table(
        table_id,
        12,
        308,
        456,
        104,
        "Threshold",
        [("KPIThreshold", "column", "KPI"), ("KPIThreshold", "column", "Green"), ("KPIThreshold", "column", "Red")],
    )
    visuals[table_id]["position"]["z"] = 6
    visuals[table_id]["position"]["tabOrder"] = 6
    page_json = {
        "$schema": PAGE_SCHEMA,
        "name": page_id,
        "displayName": name,
        "displayOption": "ActualSize",
        "height": 430,
        "width": 480,
        "annotations": [{"name": "purpose", "value": summary}],
    }
    return page_id, page_json, visuals


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantic-model", type=Path, required=True, help="Existing .SemanticModel folder containing definition/*.tmdl")
    parser.add_argument("--out", type=Path, required=True, help="Output PBIP project folder")
    parser.add_argument("--project-name", default="topdeskdemo")
    args = parser.parse_args()

    semantic_src = args.semantic_model.resolve()
    if not (semantic_src / "definition" / "database.tmdl").exists():
        raise SystemExit(f"Missing TMDL database.tmdl under {semantic_src}")

    out = args.out.resolve()
    temp_semantic_src = None
    try:
        semantic_src.relative_to(out)
        temp_semantic_src = Path(tempfile.mkdtemp(prefix="topdesk-semantic-model-")) / semantic_src.name
        shutil.copytree(semantic_src, temp_semantic_src)
        semantic_src = temp_semantic_src
    except ValueError:
        pass

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    project_name = args.project_name
    semantic_dst = out / f"{project_name}.SemanticModel"
    report_dst = out / f"{project_name}.Report"
    shutil.copytree(semantic_src, semantic_dst)
    if temp_semantic_src:
        shutil.rmtree(temp_semantic_src.parent, ignore_errors=True)

    write_json(
        semantic_dst / "definition.pbism",
        {
            "$schema": PBISM_SCHEMA,
            "version": "4.0",
            "settings": {},
        },
    )
    write_json(
        out / f"{project_name}.pbip",
        {
            "version": "1.0",
            "artifacts": [{"report": {"path": f"{project_name}.Report"}}],
            "settings": {"enableAutoRecovery": True},
        },
    )
    (out / ".gitignore").write_text("**/.pbi/localSettings.json\n**/.pbi/cache.abf\n", encoding="utf-8")

    write_json(
        report_dst / "definition.pbir",
        {
            "$schema": PBIR_SCHEMA,
            "version": "4.0",
            "datasetReference": {"byPath": {"path": f"../{project_name}.SemanticModel"}},
        },
    )
    definition = report_dst / "definition"
    write_json(
        definition / "report.json",
        {
            "$schema": REPORT_SCHEMA,
            "themeCollection": {
                "baseTheme": {
                    "name": "CY26SU04",
                    "type": "SharedResources",
                    "reportVersionAtImport": {
                        "visual": "2.8.0",
                        "report": "3.2.0",
                        "page": "2.3.1",
                    },
                }
            },
            "objects": {
                "section": [
                    {
                        "properties": {
                            "verticalAlignment": text_literal("Top"),
                        }
                    }
                ]
            },
            "resourcePackages": [
                {
                    "name": "SharedResources",
                    "type": "SharedResources",
                    "items": [
                        {
                            "name": "CY26SU04",
                            "path": "BaseThemes/CY26SU04.json",
                            "type": "BaseTheme",
                        }
                    ],
                }
            ],
            "settings": {
                "useStylableVisualContainerHeader": True,
                "exportDataMode": "AllowSummarized",
                "defaultDrillFilterOtherVisuals": True,
                "allowChangeFilterTypes": True,
                "useEnhancedTooltips": True,
                "useDefaultAggregateDisplayName": True,
            },
            "annotations": [
                {"name": "defaultPage", "value": "ReportSection01ExecutiveOverview"},
                {"name": "generatedBy", "value": "topdesk-pbir-generator"},
            ],
        },
    )
    write_json(
        definition / "version.json",
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
            "version": "2.0.0",
        },
    )
    page_refs = []
    all_pages = list(PAGES) + list(DRILLTHROUGH_PAGES)
    ordinal = 0
    for ordinal, page in enumerate(all_pages, start=1):
        page_id, page_json, visuals = build_page(page, ordinal)
        page_refs.append({"name": page_id, "displayName": page["name"]})
        page_dir = definition / "pages" / page_id
        write_json(page_dir / "page.json", page_json)
        for visual_id, visual in visuals.items():
            write_json(page_dir / "visuals" / visual_id / "visual.json", visual)
    for tooltip_index, tooltip_page in enumerate(TOOLTIP_PAGES, start=ordinal + 1):
        page_id, page_json, visuals = build_tooltip_page(tooltip_page, tooltip_index)
        page_refs.append({"name": page_id, "displayName": tooltip_page[0]})
        page_dir = definition / "pages" / page_id
        write_json(page_dir / "page.json", page_json)
        for visual_id, visual in visuals.items():
            write_json(page_dir / "visuals" / visual_id / "visual.json", visual)
    write_json(
        definition / "pages" / "pages.json",
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": [page["name"] for page in page_refs],
            "activePageName": page_refs[0]["name"],
        },
    )
    visual_count = len(list((definition / "pages").rglob("visual.json")))

    manifest = {
        "project": str(out),
        "pbip": str(out / f"{project_name}.pbip"),
        "pbir": str(report_dst / "definition.pbir"),
        "pages": len(page_refs),
        "visuals": visual_count,
        "standardPages": len(PAGES),
        "drillthroughPages": len(DRILLTHROUGH_PAGES),
        "tooltipPages": len(TOOLTIP_PAGES),
        "semanticModel": str(semantic_dst),
    }
    write_json(out / "topdesk-pbir-manifest.json", manifest)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
