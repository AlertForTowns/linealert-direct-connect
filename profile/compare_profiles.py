# profile/compare_profiles.py
import json

def load_profile(path):
    with open(path, "r") as f:
        return json.load(f)

def compare_profiles(old, new, register_threshold=0.1, interval_threshold_ms=150):
    alerts = []

    # Check register drift
    old_regs = set(old["registers_accessed"].keys())
    new_regs = set(new["registers_accessed"].keys())
    new_registers = new_regs - old_regs
    lost_registers = old_regs - new_regs

    if new_registers:
        alerts.append(f"🆕 New registers accessed: {sorted(new_registers)}")
    if lost_registers:
        alerts.append(f"⚠️ Registers no longer accessed: {sorted(lost_registers)}")

    # Check polling frequency drift
    old_mean = old["polling_interval_ms"]["mean"]
    new_mean = new["polling_interval_ms"]["mean"]
    drift = abs(new_mean - old_mean)

    if drift > interval_threshold_ms:
        alerts.append(f"⏱ Polling interval drift: {old_mean}ms → {new_mean}ms (Δ {drift:.2f}ms)")

    # Check for burstiness or quietness
    old_total = old["summary"]["total_packets"]
    new_total = new["summary"]["total_packets"]

    if new_total < old_total * (1 - register_threshold):
        alerts.append(f"📉 Total packets dropped: {old_total} → {new_total}")
    elif new_total > old_total * (1 + register_threshold):
        alerts.append(f"📈 Total packets increased: {old_total} → {new_total}")

    return alerts or ["✅ No significant behavioral drift detected."]

# Example usage
if __name__ == "__main__":
    old_profile = load_profile("profiles/baseline_profile.json")
    new_profile = load_profile("profiles/new_snapshot_profile.json")

    results = compare_profiles(old_profile, new_profile)
    print("\n".join(results))
