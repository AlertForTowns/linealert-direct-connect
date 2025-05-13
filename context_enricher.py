import re

def generate_context(alert_line):
    if "[DRIFT]" in alert_line:
        values = extract_values(alert_line)
        if values and sorted(values) == values:
            return "↳ Gradual increase detected. May indicate heat, load, or loop lag."
        elif values and sorted(values, reverse=True) == values:
            return "↳ Gradual decrease detected. Possible flow restriction or cooling issue."
        return "↳ Drift detected. Check for signal fluctuation or external influence."

    if "[STABLE]" in alert_line:
        return "↳ Values consistent. No significant system change observed."

    return ""

def extract_values(alert_line):
    match = re.search(r"\[([0-9,\s]+)\]", alert_line)
    if match:
        return [int(x.strip()) for x in match.group(1).split(",")]
    return []
