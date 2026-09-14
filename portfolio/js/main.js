/* =========================================================
   Басты беттің логикасы: жобалар, соңғы жазбалар, форма.
   ========================================================= */

/* ---------------------------------------------------------
   БАПТАУЛАР

   API_URL — бэкендтің адресі.
   Бос ("") болса, форма пошта қолданбаңды ашады. GitHub Pages
   үшін осы керек, себебі онда сервер жұмыс істемейді.

   Бэкендті Render-ге шығарсаң, адресін осында жаз:
   const API_URL = "https://менің-сайтым.onrender.com/api/messages/";
   --------------------------------------------------------- */
const API_URL = "";
const CONTACT_EMAIL = "nursultan@example.com";

/* ---------- көмекші ---------- */
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

/* ---------- жобалар ---------- */
function renderProjects() {
  const box = document.getElementById("projects-list");
  if (!box) return;

  const list = Array.isArray(window.PROJECTS) ? window.PROJECTS : [];

  if (list.length === 0) {
    box.innerHTML = '<p class="sec-note">Жобалар әзірге қосылмаған.</p>';
    return;
  }

  box.innerHTML = list.map(function (project) {
    const tags = (project.tags || [])
      .map(function (tag) { return "<span>" + escapeHtml(tag) + "</span>"; })
      .join("");

    const link = project.link
      ? '<a class="plink" href="' + escapeHtml(project.link) +
        '" target="_blank" rel="noopener">Кодын көру</a>'
      : "";

    return "" +
      '<article class="project">' +
        '<div class="project-media">' +
          '<img src="' + escapeHtml(project.image) + '" alt="' + escapeHtml(project.title) + '">' +
        "</div>" +
        '<div class="project-body">' +
          "<h3>" + escapeHtml(project.title) + "</h3>" +
          '<span class="status">' + escapeHtml(project.status) + "</span>" +
          "<p>" + escapeHtml(project.description) + "</p>" +
          '<div class="tags">' + tags + "</div>" +
          link +
        "</div>" +
      "</article>";
  }).join("");
}

/* ---------- соңғы жазбалар ---------- */
function renderLatestPosts() {
  const box = document.getElementById("latest-posts");
  if (!box) return;

  const list = (Array.isArray(window.ARTICLES) ? window.ARTICLES : []).slice(0, 3);

  if (list.length === 0) {
    box.innerHTML = '<p class="sec-note">Жазбалар әзірге жоқ.</p>';
    return;
  }

  box.innerHTML = list.map(function (article) {
    return "" +
      '<a class="post-row" href="post.html?slug=' + encodeURIComponent(article.slug) + '">' +
        '<time class="post-date">' + escapeHtml(formatDate(article.date)) + "</time>" +
        "<h3>" + escapeHtml(article.title) + "</h3>" +
        "<p>" + escapeHtml(article.summary) + "</p>" +
      "</a>";
  }).join("");
}

renderProjects();
renderLatestPosts();

/* ---------- байланыс формасы ---------- */
const form = document.getElementById("contact-form");
const formStatus = document.getElementById("form-status");

function setStatus(text, type) {
  formStatus.textContent = text;
  formStatus.className = "form-status" + (type ? " " + type : "");
}

if (form) {
  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      message: form.message.value.trim()
    };

    if (!data.name || !data.message) {
      setStatus("Атыңыз бен хабарламаны толтырыңыз.", "err");
      return;
    }

    // Сервер қосылмаған болса — пошта қолданбасын ашамыз.
    if (!API_URL) {
      const subject = encodeURIComponent("Сайттан хабарлама: " + data.name);
      const body = encodeURIComponent(
        data.message + "\n\n—\n" + data.name + (data.email ? " · " + data.email : "")
      );
      window.location.href = "mailto:" + CONTACT_EMAIL + "?subject=" + subject + "&body=" + body;
      setStatus("Пошта қолданбаңыз ашылды.", "ok");
      return;
    }

    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    setStatus("Жіберілуде…");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error("bad status");
      form.reset();
      setStatus("Хабарламаңыз сақталды. Рақмет!", "ok");
    } catch (error) {
      setStatus("Жіберу мүмкін болмады. Серверді тексеріңіз.", "err");
    } finally {
      button.disabled = false;
    }
  });
}
