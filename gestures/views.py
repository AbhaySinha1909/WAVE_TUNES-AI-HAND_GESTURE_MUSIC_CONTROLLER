from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Store the latest gesture globally
current_gesture = None


@csrf_exempt
def update_gesture(request):
    """
    Frontend sends gesture updates here.
    Example payload:
    { "gesture": "play" }
    """
    global current_gesture

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
        gesture = data.get("gesture")

        if gesture:
            current_gesture = gesture
            return JsonResponse({"status": "updated", "gesture": gesture})

        return JsonResponse({"error": "Gesture not provided"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def get_gesture(request):
    """
    Music page polls this endpoint to get the latest gesture.
    """
    global current_gesture

    if current_gesture is None:
        return JsonResponse({"gesture": "none"})

    return JsonResponse({"gesture": current_gesture})
