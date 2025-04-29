# LineAlert: Direct-Connect Edition

This is the minimal, field-ready version of LineAlert designed for use with industrial PLCs connected directly to a Raspberry Pi via serial (RS232 or USB-serial).

No switches. No VLANs. Just real-time passive analysis over a direct wire.

---

## 🔧 Features (MVP Scope)

- Passive serial traffic capture
- Snapshot writer (`.lasnap` format)
- Basic behavior profiling (registers, frequency)
- Drift detection (recursive + timing instability model)
- Ready for small industrial environments or lab setups

---

## 🧪 Target Use Case

- Field techs working with isolated or legacy PLCs
- Small facilities without managed switches
- Testing drift or behavioral anomalies in connected equipment

---

## 📦 Project Structure

linealert-direct-connect/ ├── capture/serial_capture.py ├── snapshot/snapshot_writer.py ├── profile/auto_profiler.py ├── drift/afib_detector.py ├── test_data/example_serial_log.txt

yaml
Copy
Edit

---

## ⚙️ Quick Start

```bash
pip install -r requirements.txt
python capture/serial_capture.py --port /dev/ttyUSB0
🔒 License
Apache 2.0 (see LICENSE)
