import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Message

MAX_BODY = 20_000


@csrf_exempt
def create_message(request):
    """Формадан келген хабарламаны дерекқорға жазады."""
    if request.method == "OPTIONS":
        return JsonResponse({"ok": True})

    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "method_not_allowed"}, status=405)

    if len(request.body) > MAX_BODY:
        return JsonResponse({"ok": False, "error": "too_large"}, status=413)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    name = str(data.get("name", "")).strip()[:120]
    email = str(data.get("email", "")).strip()[:200]
    text = str(data.get("message", "")).strip()[:5000]

    if not name or not text:
        return JsonResponse({"ok": False, "error": "missing_fields"}, status=400)

    message = Message.objects.create(name=name, email=email, text=text)
    return JsonResponse({"ok": True, "id": message.id}, status=201)
