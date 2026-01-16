document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add patient message
        addMessage("Patient", message);
        userInput.value = "";

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            // Add physician reply
            addMessage("Physician", data.physician_reply);

            // Update UI sections
            updateSummary(data.summary);
            updateSentiment(data.sentiment);
            updateSOAP(data.soap_note);
        })
        .catch(err => console.error("Error:", err));
    }

    function addMessage(role, text) {
        const msg = document.createElement("div");
        msg.classList.add("chat-message", role.toLowerCase());

        const label = document.createElement("div");
        label.className = "label";
        label.textContent = role;

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.textContent = text;

        msg.append(label, bubble);
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // -------------------------------
    // Medical Summary Rendering
    // -------------------------------
    function updateSummary(summary) {
        const summaryText = document.getElementById("summaryText");

        if (!summary || typeof summary !== "object") {
            summaryText.textContent = "No summary available.";
            return;
        }

        summaryText.textContent = `
Patient Name:
${summary.Patient_Name || "Unknown"}

Symptoms:
- ${summary.Symptoms?.join("\n- ") || "Not mentioned"}

Diagnosis:
${summary.Diagnosis || "Not mentioned"}

Treatment:
- ${summary.Treatment?.join("\n- ") || "Not mentioned"}

Current Status:
${summary.Current_Status || "Not specified"}

Prognosis:
${summary.Prognosis || "Not specified"}
        `.trim();
    }

    // -------------------------------
    // Sentiment Rendering
    // -------------------------------
    function updateSentiment(sentiment) {
        const label = document.getElementById("sentimentLabel");
        label.className = "sentiment";

        if (sentiment === "Anxious") label.classList.add("anxious");
        else if (sentiment === "Reassured") label.classList.add("reassured");
        else label.classList.add("neutral");

        label.textContent = sentiment;
    }

    // -------------------------------
    // SOAP Note Rendering (Formatted)
    // -------------------------------
    function updateSOAP(soap) {
        if (!soap) return;

        document.getElementById("soapSubjective").textContent =
            formatSection(soap.Subjective);

        document.getElementById("soapObjective").textContent =
            formatSection(soap.Objective);

        document.getElementById("soapAssessment").textContent =
            formatSection(soap.Assessment);

        document.getElementById("soapPlan").textContent =
            formatSection(soap.Plan);
    }

    function formatSection(section) {
        if (!section || typeof section !== "object") {
            return "Not documented.";
        }

        return Object.entries(section)
            .map(([key, value]) => `${key.replaceAll("_", " ")}: ${value}`)
            .join("\n");
    }
});