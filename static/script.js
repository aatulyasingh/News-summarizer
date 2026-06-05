async function getNews() {
    const btn = document.getElementById("fetchBtn");
    const loader = document.getElementById("loader");
    const summaryBox = document.getElementById("summary-box");
    const headlinesBox = document.getElementById("headlines-box");

    btn.disabled = true;
    btn.textContent = "Fetching...";
    loader.classList.remove("hidden");
    summaryBox.classList.add("hidden");
    headlinesBox.classList.add("hidden");

    try {
        const response = await fetch("/get-news");
        const data = await response.json();

        document.getElementById("summary-text").textContent = data.summary;

        const headlinesList = document.getElementById("headlines-list");
        headlinesList.innerHTML = "";
        data.headlines.forEach(headline => {
            headlinesList.innerHTML += `
                <div class="headline-card">
                    <a href="${headline.url}" target="_blank">${headline.title}</a>
                    <p class="source">${headline.source}</p>
                </div>
            `;
        });

        summaryBox.classList.remove("hidden");
        headlinesBox.classList.remove("hidden");

    } catch (error) {
        alert("Something went wrong! Please try again.");
    } finally {
        loader.classList.add("hidden");
        btn.disabled = false;
        btn.textContent = "Get Today's News";
    }
}