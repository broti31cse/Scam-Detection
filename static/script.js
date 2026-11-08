async function scanWebsite() {

    const url = document.getElementById("url").value.trim();

    const result = document.getElementById("result");

    if (!url) {
        result.innerHTML = "Please enter a website URL.";
        return;
    }

    result.innerHTML = "Analyzing website...";

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({ url: url })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed");
        }

        result.innerHTML = `
            <h3>Security Analysis Result</h3>

            <p><b>Website:</b> ${escapeHTML(data.domain)}</p>

            <p><b>Risk Score:</b> ${data.score}/100</p>

            <p><b>Status:</b> ${data.result}</p>

            <p><b>HTTPS:</b> ${escapeHTML(data.tls)}</p>

            <h4>Detected Signals:</h4>

            <ul>
                ${data.reasons.map(
                    item => `<li>${escapeHTML(item)}</li>`
                ).join("")}
            </ul>

            <small>
                Educational prototype. A low risk score
                does not guarantee that a website is safe.
            </small>
        `;

    } catch (error) {

        result.innerHTML = escapeHTML(error.message);

    }
}

function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}