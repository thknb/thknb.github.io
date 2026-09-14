"""Қарапайым Markdown → HTML.

Қолдайтыны:
    ## Тақырып        ### Кіші тақырып
    - тізім
    > дәйексөз
    **қалың**  *көлбеу*  `код`
    [мәтін](сілтеме)   ![сипаттама](images/сурет.jpg)
    ```  код блогы  ```
"""
import html
import re


def _inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" rel="noopener">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def to_html(source):
    lines = (source or "").replace("\r\n", "\n").split("\n")
    out, buffer, mode = [], [], None

    def flush():
        nonlocal buffer, mode
        if not buffer:
            mode = None
            return
        if mode == "p":
            out.append("<p>" + _inline(" ".join(buffer)) + "</p>")
        elif mode == "ul":
            items = "".join("<li>" + _inline(item) + "</li>" for item in buffer)
            out.append("<ul>" + items + "</ul>")
        elif mode == "quote":
            out.append("<blockquote>" + _inline(" ".join(buffer)) + "</blockquote>")
        elif mode == "code":
            out.append("<pre><code>" + html.escape("\n".join(buffer)) + "</code></pre>")
        buffer, mode = [], None

    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            if in_code:
                flush()
                in_code = False
            else:
                flush()
                in_code, mode = True, "code"
            continue

        if in_code:
            buffer.append(line)
            continue

        stripped = line.strip()

        if not stripped:
            flush()
        elif stripped.startswith("### "):
            flush()
            out.append("<h4>" + _inline(stripped[4:]) + "</h4>")
        elif stripped.startswith("## "):
            flush()
            out.append("<h3>" + _inline(stripped[3:]) + "</h3>")
        elif stripped.startswith("- "):
            if mode != "ul":
                flush()
                mode = "ul"
            buffer.append(stripped[2:])
        elif stripped.startswith("> "):
            if mode != "quote":
                flush()
                mode = "quote"
            buffer.append(stripped[2:])
        else:
            if mode != "p":
                flush()
                mode = "p"
            buffer.append(stripped)

    flush()
    return "".join(out)
