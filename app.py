from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

app = FastAPI(title="VeraForge Elite")

contexts = {
    "category": {},
    "merchant": {},
    "trigger": {},
    "customer": {}
}

auto_reply_counter = {}

class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: Optional[str] = None

class TickRequest(BaseModel):
    now: str
    available_triggers: List[str]

class ReplyRequest(BaseModel):
    conversation_id: str
    merchant_id: str
    customer_id: Optional[str] = None
    from_role: str
    message: str
    received_at: str
    turn_number: int

def merchant_name(m):
    return m.get("identity", {}).get("name", "Your Business")

def owner_name(m):
    return m.get("identity", {}).get("owner_first_name", "there")

def locality(m):
    return m.get("identity", {}).get("locality", "your area")

def active_offer(m):
    offers = m.get("offers", [])
    for o in offers:
        if o.get("status") == "active":
            return o.get("title", "")
    return ""

def category_slug(m):
    return m.get("category_slug", "general")

def perf_views(m):
    return m.get("performance", {}).get("views", 100)

def perf_ctr(m):
    return m.get("performance", {}).get("ctr", 2.0)

def is_hostile(msg):
    msg = msg.lower()
    words = ["stop messaging", "spam", "useless", "annoying", "leave me"]
    return any(w in msg for w in words)

def is_commitment(msg):
    msg = msg.lower()
    words = ["lets do it", "let's do it", "do it", "launch", "yes proceed", "what next"]
    return any(w in msg for w in words)

def is_auto_reply(msg):
    msg = msg.lower()
    patterns = [
        "thank you for contacting us",
        "our team will respond shortly",
        "we will get back",
        "away right now"
    ]
    return any(p in msg for p in patterns)

def compose_action(trigger_id: str):
    trigger = contexts["trigger"].get(trigger_id, {
        "kind": trigger_id,
        "payload": {},
        "merchant_id": "m1"
    })
    merchant_id = trigger.get("merchant_id", "m1")
    merchant = contexts["merchant"].get(merchant_id, {})

    if not merchant:
        return None
    slug = category_slug(merchant)
    owner = owner_name(merchant)
    mname = merchant_name(merchant)
    area = locality(merchant)
    offer = active_offer(merchant)
    views = perf_views(merchant)
    ctr = perf_ctr(merchant)
    repeat_users = max(18, int(views * 0.22))
    hot_searches = max(25, int(views * 0.30))
    lost_users = max(12, int(views * 0.15))
    kind = trigger.get("kind", trigger_id)
    if slug == "restaurant":
        if "sales_dip" in kind:
            body = (
                f"{owner}, lunch demand dipped today. "
                f"{repeat_users} nearby diners in {area} haven’t ordered recently. "
                f"Should I send them {offer or 'a lunch combo'} for 1–3 PM now?"
            )
        elif "search_spike" in kind:
            body = (
                f"{owner}, food searches in {area} are rising now. "
                f"{hot_searches} people are browsing nearby options. "
                f"Should I boost {mname} with {offer or 'your bestseller'} today?"
            )
        else:
            body = (
                f"{owner}, {lost_users} repeat diners from {area} look inactive. "
                f"Want me to win them back using {offer or 'a comeback offer'} today?"
            )
    elif slug == "dentist":
        body = (
            f"Dr. {owner}, check-up searches rose in {area}. "
            f"Should I help fill 2 consultation slots this evening?"
        )
    elif slug == "salon":
        body = (
            f"{owner}, beauty bookings are picking up in {area}. "
            f"{hot_searches} nearby people are exploring salons today. "
            f"Should I promote premium services now?"
        )
    elif slug == "gym":
        body = (
            f"{owner}, {lost_users} members haven’t visited lately. "
            f"Want me to launch a 7-day comeback challenge today?"
        )
    elif slug == "pharmacy":
        body = (
            f"{owner}, refill demand may be due soon in {area}. "
            f"Should I send reorder reminders today?"
        )
    else:
        body = (
            f"{owner}, demand in {area} looks active today. "
            f"Should I promote {mname} now?"
        )
    return {
        "trigger_id": trigger_id,
        "merchant_id": merchant_id,
        "customer_id": None,
        "body": body,
        "cta": "Yes, launch it",
        "send_as": "vera"
    }

@app.get("/v1/healthz")
def healthz():
    return {
        "ok": True,
        "status": "healthy"
    }

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Avni Singla - VeraForge Elite",
        "model": "Deterministic Contextual Decision Engine",
        "version": "3.0"
    }

@app.post("/v1/context")
def push_context(req: ContextRequest):
    if req.scope not in contexts:
        return {"accepted": False}
    contexts[req.scope][req.context_id] = req.payload
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for trig_id in req.available_triggers[:3]:
        action = compose_action(trig_id)
        if action:
            actions.append(action)
    return {"actions": actions}

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message
    cid = req.conversation_id
    if is_hostile(msg):
        return {
            "action": "end",
            "body": "Understood. I’ll stop here and only reach out when genuinely useful."
        }
    if is_auto_reply(msg):
        auto_reply_counter[cid] = auto_reply_counter.get(cid, 0) + 1
        if auto_reply_counter[cid] >= 2:
            return {
                "action": "end",
                "body": ""
            }
        return {
            "action": "wait",
            "wait_seconds": 60
        }
    if is_commitment(msg):
        return {
            "action": "send",
            "body": "Done — campaign draft is ready for today. Confirm and I’ll launch it now."
        }
    if "price" in msg.lower() or "cost" in msg.lower():
        return {
            "action": "send",
            "body": "We can start small and only scale what performs. Want a low-budget test first?"
        }
    return {
        "action": "send",
        "body": "Got it. I’ll monitor performance and share the next best growth opportunity."
    }