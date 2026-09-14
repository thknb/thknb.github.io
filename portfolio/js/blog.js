/* =========================================================
   Блог беттерінің логикасы (blog.html және post.html).
   Мәтіндер data/articles.js файлынан келеді.
   ========================================================= */

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatDate(iso) {
  const date = new Date(iso + "T00:00:00");
  if (isNaN(date)) return iso;
  return date.toLocaleDateString("kk-KZ", { year: "numeric", month: "long", day: "numeric" });
}

function allArticles() {
  return Array.isArray(window.ARTICLES) ? window.ARTICLES : [];
}

/* ---------- тізім беті ---------- */
function renderList() {
  const box = document.getElementById("post-list");
  if (!box) return;

  const list = allArticles();

  if (list.length === 0) {
    box.innerHTML = '<p class="sec-note">Жазбалар әзірге жоқ.</p>';
    return;
  }

  box.innerHTML = list.map(function (article) {
    const url = "post.html?slug=" + encodeURIComponent(article.slug);
    const cover = article.cover
      ? '<div class="post-cover"><img src="' + escapeHtml(article.cover) + '" alt=""></div>'
      : "";

    return "" +
      '<a class="post-item" href="' + url + '">' +
        cover +
        '<div class="post-item-text">' +
          '<time class="post-date">' + escapeHtml(formatDate(article.date)) + "</time>" +
          "<h2>" + escapeHtml(article.title) + "</h2>" +
          "<p>" + escapeHtml(article.summary) + "</p>" +
          '<span class="plink">Оқу →</span>' +
        "</div>" +
      "</a>";
  }).join("");
}

/* ---------- жазба беті ---------- */
function renderPost() {
  const box = document.getElementById("post");
  if (!box) return;

  const slug = new URLSearchParams(window.location.search).get("slug");
  const article = allArticles().find(function (a) { return a.slug === slug; });

  if (!article) {
    box.innerHTML = '<p class="sec-note">Мұндай жазба табылмады.</p>';
    return;
  }

  document.title = article.title;

  const cover = article.cover
    ? '<div class="post-cover wide"><img src="' + escapeHtml(article.cover) + '" alt=""></div>'
    : "";

  // article.html — Django арқылы Markdown-нан жасалған HTML.
  box.innerHTML =
    '<time class="post-date">' + escapeHtml(formatDate(article.date)) + "</time>" +
    '<h1 class="page-title">' + escapeHtml(article.title) + "</h1>" +
    cover +
    '<div class="article-body">' + article.html + "</div>";
}

renderList();
renderPost();
