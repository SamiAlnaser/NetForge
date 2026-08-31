def build_markdown_report(summary):
    lines = [
        "# NetForge Performance Report",
        "",
        f'**Overall Status:** {summary["overall_status"]}',
        "",
        "| Metric | Baseline | Current | Change | Threshold | Status |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for result in summary["results"]:
        change = result["change_percent"]

        if change is None:
            change_text = "N/A"
        else:
            change_text = f"{change:+.2f}%"

        lines.append(
            f'| {result["metric"]} '
            f'| {result["baseline"]} '
            f'| {result["current"]} '
            f'| {change_text} '
            f'| {result["threshold_percent"]}% '
            f'| {result["status"]} |'
        )

    return "\n".join(lines)
