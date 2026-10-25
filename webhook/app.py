
from flask import Flask, request, jsonify
import logging
import subprocess
import threading
from pathlib import Path

app = Flask(__name__)

PROJECT_DIR = Path(__file__).resolve().parent.parent
PLAYBOOK = PROJECT_DIR / "ansible" / "recover_nginx.yml"
ANSIBLE = "/opt/homebrew/bin/ansible-playbook"

logging.basicConfig(
    filename=str(PROJECT_DIR / "logs" / "recovery.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Prevent duplicate recovery runs for the same outage.
recovery_lock = threading.Lock()
outage_handled = False

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/alert", methods=["POST"])
def receive_alert():
    global outage_handled

    payload = request.get_json(silent=True) or {}
    results = []

    for alert in payload.get("alerts", []):
        name = alert.get("labels", {}).get("alertname", "unknown")
        status = alert.get("status", payload.get("status", "unknown"))

        logging.info("Received alert: name=%s status=%s", name, status)
        print(f"Received alert: {name}, status={status}", flush=True)

        if name != "NginxDown":
            continue

        if status == "resolved":
            with recovery_lock:
                outage_handled = False
            logging.info("NginxDown resolved; recovery safeguard reset")
            results.append({"alert": name, "recovery": "reset"})
            continue

        if status != "firing":
            continue

        with recovery_lock:
            if outage_handled:
                logging.info("Duplicate NginxDown ignored")
                results.append({"alert": name, "recovery": "already_handled"})
                continue

            # Reserve this outage before starting Ansible.
            outage_handled = True

        try:
            result = subprocess.run(
                [
                    ANSIBLE,
                    "-i", "localhost,",
                    "-c", "local",
                    str(PLAYBOOK)
                ],
                cwd=str(PROJECT_DIR),
                capture_output=True,
                text=True,
                timeout=120,
                check=False
            )

            if result.returncode == 0:
                logging.info("Ansible recovery succeeded: %s", result.stdout)
                print("Ansible recovery succeeded", flush=True)
                results.append({"alert": name, "recovery": "succeeded"})
            else:
                logging.error("Ansible recovery failed: %s", result.stderr)
                print("Ansible recovery failed", flush=True)
                with recovery_lock:
                    outage_handled = False
                results.append({"alert": name, "recovery": "failed"})

        except subprocess.TimeoutExpired:
            logging.error("Ansible recovery timed out")
            with recovery_lock:
                outage_handled = False
            results.append({"alert": name, "recovery": "timeout"})

        except Exception:
            logging.exception("Could not run Ansible recovery")
            with recovery_lock:
                outage_handled = False
            results.append({"alert": name, "recovery": "error"})

    return jsonify({"received": True, "results": results}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
