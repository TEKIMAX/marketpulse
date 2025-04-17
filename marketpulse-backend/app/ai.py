import subprocess
import json

def run_codex(prompt: str) -> str:
    """
    Run the Codex CLI with the given prompt and return the analysis result.
    Requires 'codex' binary to be installed and authenticated.
    """
    payload = {"prompt": prompt}
    # Invoke codex CLI in JSON mode
    proc = subprocess.run(
        ["codex", "run", "--json", json.dumps(payload)],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Codex CLI error: {proc.stderr.strip()}")

    output = proc.stdout.strip()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid JSON from Codex CLI: {output}")

    # Expect 'result' field in output
    if "result" not in data:
        raise RuntimeError(f"Unexpected response structure: {data}")

    return data["result"]