from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="VeraForge Elite",
    version="7.0",
    description="Final AI Merchant Growth Decision Engine"
)

class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: str

class TickRequest(BaseModel):
    now: str
    available_triggers: List[str]

class ReplyRequest(BaseModel):
    conversation_id: str
    merchant_id: str
    from_role: str
    message: str
    received_at: str
    turn_number: int

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
    <title>VeraForge Elite</title>
    <style>
    body{
        background:linear-gradient(135deg,#001233,#003566,#001d3d);
        color:white;
        text-align:center;
        font-family:Arial;
        padding-top:90px;
    }
    h1{font-size:72px;color:#46b3ff;}
    p{font-size:28px;}
    a{
        text-decoration:none;
        background:#1e90ff;
        color:white;
        padding:16px 28px;
        border-radius:10px;
        margin:12px;
        display:inline-block;
        font-size:22px;
    }
    </style>
    </head>
    <body>
        <h1>VeraForge Elite</h1>
        <p>AI Merchant Growth Decision Engine</p>
        <a href='/docs'>API Docs</a>
        <a href='/v1/healthz'>Health</a>
    </body>
    </html>
    """

memory = {}
conversation_memory = {}

@app.get("/v1/healthz")
def health():
    return {"ok": True, "status": "healthy"}

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Avni Singla - VeraForge Elite",
        "model": "Adaptive Merchant Decision Engine",
        "version": "7.0"
    }

@app.post("/v1/context")
def context(req: ContextRequest):
    memory[req.context_id] = req.payload
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for trig in req.available_triggers:
        if trig == "sales_dip":
            body = "Orders slowed this week nearby. Launch a comeback combo offer tonight to recover demand."
            cta = "Recover Sales"
        elif trig == "festival_push":
            body = "Festival demand is rising nearby. Promote festive specials and limited-time family combos now."
            cta = "Festival Push"
        elif trig == "competitor_spike":
            body = "Nearby competitors are trending. Run a repeat-customer campaign with loyalty rewards today."
            cta = "Win Customers Back"
        elif trig == "rain_alert":
            body = "Rain expected today. Push delivery bundles and convenience offers for higher order volume."
            cta = "Boost Delivery"
        elif trig == "regulation_change":
            body = "A compliance update may impact local businesses. Review operations and customer notices today."
            cta = "Review Update"
        else:
            body = "A fresh growth opportunity is available today. Activate outreach campaigns now."
            cta = "Act Now"
        actions.append({
            "trigger_id": trig,
            "merchant_id": "m1",
            "customer_id": None,
            "body": body,
            "cta": cta,
            "send_as": "vera"
        })
    return {"actions": actions}

def has_any(msg, words):
    return any(w in msg for w in words)

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    cid = req.conversation_id
    stop_words = [
        "stop", "unsubscribe", "spam", "leave me alone",
        "annoying", "don't message", "remove me"
    ]
    if has_any(msg, stop_words):
        return {
            "action": "end",
            "body": "Understood. Promotional messaging has been stopped immediately. Reach out anytime if you'd like offers again."
        }
    if cid not in conversation_memory:
        conversation_memory[cid] = 0
    conversation_memory[cid] += 1
    if conversation_memory[cid] >= 2 and req.from_role == "merchant":
        return {
            "action": "end",
            "body": "We'll pause here for now. Reach out anytime when you'd like fresh growth ideas."
        }
    if req.from_role == "customer":
        if has_any(msg, ["book", "booking", "reserve", "table", "appointment"]):
            return {
                "action": "send",
                "body": "Thanks! Your booking request has been shared with the merchant. You'll receive confirmation shortly."
            }
        if has_any(msg, ["order", "buy", "delivery", "pizza", "food", "menu"]):
            return {
                "action": "send",
                "body": "Thanks! Your order request has been forwarded to the merchant team for quick assistance."
            }
        if has_any(msg, ["open", "timing", "hours", "close"]):
            return {
                "action": "send",
                "body": "The merchant will confirm operating hours shortly. Thanks for checking in."
            }
        if has_any(msg, ["price", "cost", "charges", "rate"]):
            return {
                "action": "send",
                "body": "The merchant team will share pricing details shortly."
            }
        return {
            "action": "send",
            "body": "Thanks for contacting the merchant. Your message has been shared for assistance."
        }
    if has_any(msg, ["x-ray", "patient", "clinic", "doctor", "audit", "medical"]):
        return {
            "action": "send",
            "body": "Increase patient bookings using local search visibility, appointment reminders, review growth, and follow-up campaigns."
        }
    if has_any(msg, [
        "sales", "slow", "down", "decline", "falling",
        "less customers", "low revenue", "business slow"
    ]):
        return {
            "action": "send",
            "body": "Recover sales using combo deals, local ads, festive campaigns, and reactivation offers for past customers."
        }
    if has_any(msg, ["repeat", "loyal", "retention", "customers back"]):
        return {
            "action": "send",
            "body": "Increase repeat customers using loyalty rewards, referral offers, review follow-ups, and comeback campaigns."
        }
    if has_any(msg, ["market", "visibility", "nearby", "footfall", "walk-ins"]):
        return {
            "action": "send",
            "body": "Improve local visibility through map listings, hyperlocal ads, review growth, and neighborhood targeting."
        }
    if has_any(msg, ["growth", "grow", "new customer", "acquire", "help"]):
        return {
            "action": "send",
            "body": "Acquire new customers using first-order offers, referral incentives, social proof, and local targeting."
        }
    return {
        "action": "send",
        "body": "I can help improve sales, visibility, retention, promotions, and customer growth."
    }