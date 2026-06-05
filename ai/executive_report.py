from pathlib import Path

script_dir = Path(__file__).resolve().parent
report_path = script_dir / "executive_report.md"

if not report_path.exists():
    raise FileNotFoundError(
        "executive_report.md not found. Run generate_insights.py first."
    )

print(report_path.read_text(encoding="utf-8"))
