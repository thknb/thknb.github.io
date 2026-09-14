# Сайтты интернетке шығару — нақты қадамдар

Нәтижесі: сайт `https://thknb.github.io` адресінде ашылады. Тегін, мерзімсіз.

---

## Дайындық (шығарар алдында)

**1. Өз деректеріңді қой.**

`index.html` ішінен тауып, ауыстыр:

| Не | Қайда | Қазір |
|---|---|---|
| Telegram | `https://t.me/username` | `username` — өз аккаунтың |
| Instagram | `https://instagram.com/username` | `username` — өз аккаунтың |
| LinkedIn | `https://linkedin.com/in/username` | `username` — өз аккаунтың |

`js/main.js` ішінен:
```js
const CONTACT_EMAIL = "nursultan@example.com";   ← өз поштаң
```

**2. Суретіңді қой.** `images/photo.jpg` файлын сал, сосын `index.html` ішіндегі `images/photo-placeholder.svg` жолын `images/photo.jpg` деп ауыстыр.

**3. Үлгі мазмұнды тазала.** Админкаға кіріп, дайын тұрған үлгі жазбаны және жобаларды өзіңдікіне ауыстыр. Сосын:
```bash
cd backend
python manage.py export_site
```

---

## 1-қадам. Git орнатылғанын тексер

Терминалда:
```bash
git --version
```

Нұсқа шықса — бәрі дұрыс. «command not found» десе, https://git-scm.com/downloads сайтынан орнат.

Алғаш рет қолданып отырсаң, өзіңді таныстыр:
```bash
git config --global user.name "Нұрсұлтан"
git config --global user.email "senin@poshtan.com"
```

---

## 2-қадам. GitHub-та репозиторий жаса

1. github.com сайтына кір (аккаунт: `thknb`)
2. Оң жоғарыдағы **+** → **New repository**
3. **Repository name** өрісіне дәл былай жаз: `thknb.github.io`
4. **Public** таңда
5. «Add a README file» деген жерге **белгі қойма**
6. **Create repository** бас

Репозиторийдің аты дәл `сенің-логинің.github.io` болуы керек — сонда ғана сайт негізгі адресте ашылады.

---

## 3-қадам. Файлдарды жүкте

Терминалда `portfolio` папкасына кір:
```bash
cd portfolio
```

Сосын кезекпен:
```bash
git init
git branch -M main
git add .
git commit -m "Портфолио сайты"
git remote add origin https://github.com/thknb/thknb.github.io.git
git push -u origin main
```

**Пароль сұраса:** GitHub енді қарапайым парольді қабылдамайды, оның орнына токен керек:

1. github.com → оң жоғарыдағы суретің → **Settings**
2. Ең төменде **Developer settings**
3. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
4. **Note**: кез келген ат. **Expiration**: 90 days. **repo** деген жерге белгі қой
5. **Generate token** бас, шыққан мәтінді көшір

Терминал пароль сұрағанда сол токенді қой (username — `thknb`).

Токенді бір рет қана көресің, сақтап қой.

---

## 4-қадам. Күт те, аш

1–3 минут өтеді. Сосын браузерде аш:

```
https://thknb.github.io
```

Ашылмаса: репозиторийде **Settings** → сол жақтан **Pages** → **Source** бөлімінде `Deploy from a branch`, branch `main`, папка `/ (root)` тұрғанын тексер.

---

## 5-қадам. Кейін жаңарту

Жаңа жазба немесе жоба қосқан сайын:

```bash
cd backend
python manage.py export_site
cd ..

git add .
git commit -m "Жаңа жазба"
git push
```

Бір минуттан кейін сайтта көрінеді.

---

## Жиі кездесетін қателер

**`fatal: not a git repository`** — `portfolio` папкасының ішінде тұрған жоқсың. `cd portfolio` жаса.

**`remote origin already exists`** — сілтеме бұрын қосылған. Ауыстыр:
```bash
git remote set-url origin https://github.com/thknb/thknb.github.io.git
```

**`rejected` деген қате push кезінде** — GitHub-та файл бар. Алдымен тарт:
```bash
git pull origin main --allow-unrelated-histories
git push
```

**Сайт ашылды, бірақ дизайн жоқ** — `css` папкасы жүктелмеген. `git status` жаса, `git add .` қайтала.

**Суреттер көрінбейді** — файл аты дәл сәйкес келуі керек. `Photo.JPG` мен `photo.jpg` — GitHub үшін екі бөлек файл.

---

## Есіңде болсын

Бэкенд (Django, админка, дерекқор) **интернетке шықпайды** — ол сенің компьютеріңде қалады. GitHub Pages тек дайын файлдарды көрсетеді. Дерекқор файлы `.gitignore`-да тұр, GitHub-қа түспейді.

Яғни: жазбаны үйде админкада жазасың → `export_site` → `git push` → сайтта шығады.
