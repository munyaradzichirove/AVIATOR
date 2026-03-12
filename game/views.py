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
        user = data.get("user_id")
        amount = data.get("amount")
        print(f"[EVENT] {user} placed BET: {amount}")
        return JsonResponse({"status": "ok", "user": user, "bet": amount})

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

         # Fire directly to Kafka
        event = {
            "event_type": "GAME_START",
            "game_id": game_id,
            "timestamp": time.time(),
            "status": "in_progress"
        }
        send_event(topic="game_launch", key=game_id, event_data=event)


        print(f"[EVENT] GAME STARTED -> {game_id}")
        return JsonResponse({"status": "ok"})

DUMMY_BETS = {}          # { (user_id, game_id): {"amount": 10, "cashed_out": False} }
DUMMY_MULTIPLIERS = {}   # { game_id: 2.5 }

def get_user_bet(user_id, game_id):
    key = (user_id, game_id)
    if key not in DUMMY_BETS:
        # Create a fake bet for testing
        DUMMY_BETS[key] = {"amount": 10, "cashed_out": False, "payout": 0}
    return DUMMY_BETS[key]

def get_current_multiplier(game_id):
    # Use stored multiplier or fake one
    return DUMMY_MULTIPLIERS.get(game_id, 2.0)

def add_money_to_user_account(user_id, amount):
    # Just print for now
    print(f"[WALLET] Added {amount} to user {user_id}")

@csrf_exempt
def cashout(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST required"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")
    game_id = data.get("game_id")

    if not user_id or not game_id:
        return JsonResponse({"status": "error", "message": "Missing user_id or game_id"}, status=400)

    # 1. Get user's bet
    bet = get_user_bet(user_id, game_id)
    if bet["cashed_out"]:
        return JsonResponse({"status": "error", "message": "Already cashed out"}, status=400)

    # 2. Get real multiplier
    multiplier = get_current_multiplier(game_id)

    # 3. Calculate payout
    payout = round(bet["amount"] * multiplier, 2)

    # 4. Update dummy storage
    bet["cashed_out"] = True
    bet["payout"] = payout
    DUMMY_BETS[(user_id, game_id)] = bet
    add_money_to_user_account(user_id, payout)  # just print for now

    print(f"[EVENT] USER {user_id} cashed out at {multiplier}x, payout: {payout}")

    return JsonResponse({"status": "ok", "payout": payout, "multiplier": multiplier})