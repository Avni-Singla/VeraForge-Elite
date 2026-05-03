from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="VeraForge Elite",
    version="7.0",
    description="AI Merchant Growth Decision Engine"
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
        margin:0;
        font-family:Arial;
        text-align:center;
        background:linear-gradient(135deg,#001233,#003566,#001d3d);
        color:white;
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

memory = {}
loop_memory = {}

@app.post("/v1/context")
def context(req: ContextRequest):
    memory[req.context_id] = req.payload
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for trig in req.available_triggers:
        if trig == "sales_dip":
            body = "Orders dipped this week nearby. Launch a limited-time combo campaign tonight to recover momentum."
            cta = "Boost Orders"
        elif trig == "festival_push":
            body = "Festival demand is rising nearby. Promote festive specials and family-value bundles today."
            cta = "Run Festival Push"
        elif trig == "competitor_spike":
            body = "Nearby competitors are trending. Win repeat customers back with loyalty rewards today."
            cta = "Win Customers Back"
        elif trig == "rain_alert":
            body = "Rain expected today. Push delivery bundles and convenience offers for higher order volume."
            cta = "Boost Delivery"
        elif trig == "regulation_change":
            body = "A compliance update may impact local businesses. Review operations and customer notices today."
            cta = "Stay Compliant"
        else:
            body = "A new local growth opportunity is available today. Activate a quick campaign now."
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

def repeated_loop(conversation_id: str, msg: str):
    prev = loop_memory.get(conversation_id)
    if prev == msg:
        return True
    loop_memory[conversation_id] = msg
    return False

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    stop_words = [
        "stop", "unsubscribe", "spam",
        "leave me alone", "annoying",
        "don't message", "stop messaging"
    ]
    if any(x in msg for x in stop_words):
        return {
            "action": "end",
            "body": "Understood. Promotional messages have been stopped. Reach out anytime if you'd like help again."
        }
    if repeated_loop(req.conversation_id, msg):
        return {
            "action": "end",
            "body": "We'll pause here for now. Reach out anytime when you'd like fresh growth ideas."
        }
    if req.from_role == "customer":
        if any(x in msg for x in ["book", "reserve", "table", "appointment"]):
            return {
                "action": "send",
                "body": "Thanks! Your booking request has been shared with the merchant. You'll receive confirmation shortly."
            }
        if any(x in msg for x in ["order", "buy", "delivery", "pizza", "food"]):
            return {
                "action": "send",
                "body": "Thanks! Your order request has been shared with the merchant team for quick assistance."
            }
        if any(x in msg for x in ["timing", "hours", "open", "close"]):
            return {
                "action": "send",
                "body": "Thanks for checking in. The merchant will confirm operating hours shortly."
            }
        if any(x in msg for x in ["price", "cost", "menu", "charges"]):
            return {
                "action": "send",
                "body": "Thanks! The merchant team will share pricing details shortly."
            }
        return {
            "action": "send",
            "body": "Thanks for contacting the merchant. Your message has been forwarded for assistance."
        }
    else:
        if any(x in msg for x in [
            "clinic", "patient", "doctor",
            "x-ray", "hospital", "scan", "dentist"
        ]):
            return {
                "action": "send",
                "body": "Increase patient bookings using local search visibility, appointment reminders, review growth, and follow-up campaigns."
            }
        if any(x in msg for x in [
            "restaurant", "cafe", "pizza",
            "food", "orders", "table"
        ]):
            return {
                "action": "send",
                "body": "Grow orders using combo meals, delivery promotions, repeat-customer offers, and local map visibility."
            }
        if any(x in msg for x in [
            "salon", "spa", "beauty", "hair"
        ]):
            return {
                "action": "send",
                "body": "Increase bookings using makeover packages, referral offers, review growth, and appointment reminders."
            }
        if any(x in msg for x in [
            "gym", "fitness", "trainer", "workout"
        ]):
            return {
                "action": "send",
                "body": "Grow memberships using trial passes, referral rewards, transformation stories, and retention campaigns."
            }
        if any(x in msg for x in [
            "tuition", "coaching", "academy", "school"
        ]):
            return {
                "action": "send",
                "body": "Increase enrollments using demo classes, parent trust campaigns, local visibility, and referral programs."
            }
        if any(x in msg for x in [
            "sales", "dropping", "down", "decline"
        ]):
            return {
                "action": "send",
                "body": "Recover sales with combo offers, local ads, festive promotions, and reactivation campaigns for past customers."
            }
        if any(x in msg for x in [
            "repeat", "retention", "loyal"
        ]):
            return {
                "action": "send",
                "body": "Increase repeat customers using loyalty rewards, review follow-ups, referral offers, and personalized comeback campaigns."
            }
        if any(x in msg for x in [
            "growth", "customer", "acquire", "help"
        ]):
            return {
                "action": "send",
                "body": "Acquire new customers using first-order offers, referral incentives, social proof, and hyperlocal targeting."
            }
        return {
            "action": "send",
            "body": "I can help improve growth, retention, promotions, visibility, and overall merchant performance."
        }