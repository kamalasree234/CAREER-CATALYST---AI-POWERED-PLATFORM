

// Fetch top news
async function fetchNews() {
    try {
        const query = "career OR job OR skills OR technology OR learning OR education OR training";
        const response = await fetch(`${baseUrl}/search?q=${encodeURIComponent(query)}&token=${apiKey}&lang=en`);
        const data = await response.json();

        if (!data.articles || data.articles.length === 0) {
            document.getElementById("newsContainer").innerHTML = "<p>No news articles found.</p>";
            return;
        }

        displayNews(data.articles);
    } catch (error) {
        console.error("Error fetching news:", error);
        document.getElementById("newsContainer").innerHTML = "<p>Failed to load news. Try again later.</p>";
    }
}

// Display news articles
function displayNews(articles) {
    const newsContainer = document.getElementById("newsContainer");
    newsContainer.innerHTML = "";

    articles.forEach(article => {
        const newsItem = document.createElement("div");
        newsItem.classList.add("news-article");

        newsItem.innerHTML = `
            <img src="${article.image}" alt="News Image">
            <h3><a href="${article.url}" target="_blank">${article.title}</a></h3>
            <p>${article.description}</p>
        `;

        newsContainer.appendChild(newsItem);
    });
}

// Search news based on user input
async function searchNews() {
    const searchQuery = document.getElementById("searchBar").value.trim();

    if (searchQuery === "") {
        fetchNews(); // Show all news if search is empty
        return;
    }

    try {
        const response = await fetch(`${baseUrl}/search?q=${searchQuery}&token=${apiKey}&lang=en`);
        const data = await response.json();

        if (!data.articles || data.articles.length === 0) {
            document.getElementById("newsContainer").innerHTML = "<p>No news found for this topic.</p>";
            return;
        }

        displayNews(data.articles);
    } catch (error) {
        console.error("Error fetching search results:", error);
        document.getElementById("newsContainer").innerHTML = "<p>Failed to search news. Try again later.</p>";
    }
}

// Load all news initially
fetchNews();

