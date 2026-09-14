"""Дерекқордағы жобалар мен блог жазбаларын сайт оқитын файлдарға шығарады.

Қолданылуы:
    python manage.py export_site

Нәтижесі:
    ../data/projects.js
    ../data/articles.js
"""
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from blog.models import Article
from projects.models import Project

WARNING = (
    "/* БҰЛ ФАЙЛ АВТОМАТТЫ ТҮРДЕ ЖАСАЛҒАН — қолмен түзетпе.\n"
    "   Жаңарту: backend папкасында `python manage.py export_site` */\n\n"
)


class Command(BaseCommand):
    help = "Жобалар мен жазбаларды data/ папкасына шығарады"

    def handle(self, *args, **options):
        data_dir = settings.BASE_DIR.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)

        projects = [p.as_dict() for p in Project.objects.filter(is_published=True)]
        self._write(data_dir / "projects.js", "window.PROJECTS", projects)

        articles = [a.as_dict() for a in Article.objects.filter(is_published=True)]
        self._write(data_dir / "articles.js", "window.ARTICLES", articles)

        self.stdout.write(self.style.SUCCESS(
            f"{len(projects)} жоба және {len(articles)} жазба жазылды → {data_dir}"
        ))

    def _write(self, path, variable, items):
        body = json.dumps(items, ensure_ascii=False, indent=2)
        path.write_text(WARNING + variable + " = " + body + ";\n", encoding="utf-8")
