from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# --- Page view ---
def aviator_game(request):
    # Just renders your template
    return render(request, "game/index.html")


# --- API endpoints ---
@csrf_exempt
def bet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get("user")
        amount = data.get("amount")
        print(f"[EVENT] {user} placed BET: {amount}")
        return JsonResponse({"status": "ok", "user": user, "bet": amount})

@csrf_exempt
def cashout(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get("user")
        multiplier = data.get("multiplier")
        print(f"[EVENT] {user} cashed out at {multiplier}x")
        return JsonResponse({"status": "ok", "user": user, "multiplier": multiplier})

@csrf_exempt
def plane_crash(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_id = data.get("game_id")
        crash_point = data.get("crash_point")
        print(f"[EVENT] Game {game_id} - PLANE CRASHED at {crash_point}x")
        return JsonResponse({"status": "ok", "game_id": game_id, "crash_point": crash_point})

@csrf_exempt
def new_game(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_id = data.get("game_id")
        print(f"[EVENT] NEW GAME STARTED - ID: {game_id}")
        return JsonResponse({"status": "ok", "game_id": game_id})

@csrf_exempt
def start_game(request):
    if request.method == "POST":
        # For demo, just increment a simple counter or random ID
        game_id = getattr(request, "last_game_id", 1)
        request.last_game_id = game_id + 1  # store in memory for now
        print(f"[EVENT] NEW GAME STARTED - ID: {game_id}")
        return JsonResponse({"status": "ok", "game_id": game_id})