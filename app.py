from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import socket
import ssl

app = Flask(__name__)

def analyze_url(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname

    if not domain:
        return {"error": "Invalid URL"}

    score = 0
    reasons = []

    if parsed.scheme != "https":
        score += 20
        reasons.append("Website does not use HTTPS")

    if "@" in parsed.netloc:
        score += 25
        reasons.append("Suspicious @ symbol detected")

    suspicious_words = [
        "login", "verify", "password",
        "bank", "free", "gift", "secure"
    ]

    for word in suspicious_words:
        if word in url.lower():
            score += 5
            reasons.append("Suspicious word: " + word)

    if domain.count("-") >= 3:
        score += 10
        reasons.append("Unusual domain structure")

    score = min(score, 100)

    if score >= 50:
        result = "High Risk"
    elif score >= 20:
        result = "Needs Caution"
    else:
        result = "Lower Risk"

    tls_status = "Not checked"

    if parsed.scheme == "https":
        try:
            context = ssl.create_default_context()

            with socket.create_connection(
                (domain, parsed.port or 443), timeout=3
            ) as sock:

                with context.wrap_socket(
                    sock, server_hostname=domain
                ):
                    tls_status = "Certificate verified"

        except Exception:
            tls_status = "Certificate verification unavailable"

    if not reasons:
        reasons.append("No obvious suspicious patterns detected")

    return {
        "url": url,
        "domain": domain,
        "score": score,
        "result": result,
        "reasons": reasons,
        "tls": tls_status
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def scan():

    data = request.get_json()
    url = data.get("url", "")

    if not url.strip():
        return jsonify({"error": "Please enter a URL"}), 400

    result = analyze_url(url)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)