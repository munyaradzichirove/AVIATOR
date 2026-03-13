from django.shortcuts import render
from events.kafka_config import send_event
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import GameID
import time

def aviator_game(request):
    return render(request, "game/index.html")

@csrf_exempt
def bet(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")
        amount = data.get("amount")
        game_id = data.get("game_id", "unknown")  # optional if available

        # Fire event to Kafka
        event = {
            "event_type": "BET_PLACED",
            "game_id": game_id,
            "player": user_id,
            "bet_amount": amount,
            "timestamp": time.time(),
            "status": "active"
        }
        send_event(topic="placed_bets", key=user_id, event_data=event)

        print(f"[EVENT] {user_id} placed BET: {amount}")
        return JsonResponse({"status": "ok", "user": user_id, "bet": amount})
@csrf_exempt
def plane_crash(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_id = data.get("game_id")
        crash_point = data.get("crash_point")
        event = {
            "event_type": "PLANE_CRASH",
            "game_id": game_id,
            "crash_point": crash_point,
            "timestamp": time.time(),
            "status": "finished"
        }
        send_event(topic="plane_crash", key=game_id, event_data=event)
        print(f"[EVENT] Game {game_id} - PLANE CRASHED at {crash_point}x")
        return JsonResponse({"status": "ok", "game_id": game_id, "crash_point": crash_point})

@csrf_exempt
def request_game_id(request):
    game_tracker, _ = GameID.objects.get_or_create(id=1)
    game_tracker.current_id += 1
    game_tracker.save()
    print(f"[EVENT] GAME ID REQUESTED -> {game_tracker.current_id}")
    return JsonResponse({"game_id": game_tracker.current_id})

@csrf_exempt
def run_game(request):
    if request.method == "POST":
        data = json.loads(request.body)
        game_id = data.get("game_id")
        event = {
            "event_type": "GAME_START",
            "game_id": game_id,
            "timestamp": time.time(),
            "status": "in_progress"
        }
        send_event(topic="game_launch", key=game_id, event_data=event)
        print(f"[EVENT] GAME STARTED -> {game_id}")
        return JsonResponse({"status": "ok"})
    
@csrf_exempt
def cashout(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")
    game_id = data.get("game_id")
    multiplier = data.get("multiplier")

    if not user_id or not game_id:
        return JsonResponse({"status": "error", "message": "Missing user_id or game_id"}, status=400)

    bet_amount = data.get("bet_amount", 0)

    event = {
        "event_type": "CASHOUT",
        "user_id": user_id,
        "game_id": game_id,
        "bet_amount": bet_amount,
        "multiplier": multiplier,
        "timestamp": time.time(),
        "status": "completed"
    }

    send_event(topic="cash_out", key=str(user_id), event_data=event)

    print(f"[KAFKA] Cashout event sent for user {user_id}, game {game_id}")
    print(f"[EVENT] USER {user_id} cashed out at {multiplier}x")

    return JsonResponse({
        "status": "ok",
        "multiplier": multiplier
    })