from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List
from fastapi.responses import HTMLResponse
import re

app = FastAPI(
    title="VeraForge Elite",
    version="8.1",
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

merchant_memory = {}
loop_memory = {}

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
        "version": "8.1",
        "engine": "AI Merchant Growth Decision Engine"
    }

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return " ".join(text.split()[:6])

def detect_category(merchant_id):
    ctx = merchant_memory.get(merchant_id, {})
    payload = ctx.get("payload", {})
    return payload.get("category_slug", "").lower()

def merchant_name(merchant_id):
    ctx = merchant_memory.get(merchant_id, {})
    payload = ctx.get("payload", {})
    identity = payload.get("identity", {})
    return identity.get("name", "your business")

def repeated_loop(cid, msg):
    norm = normalize(msg)
    arr = loop_memory.get(cid, [])
    arr.append(norm)
    loop_memory[cid] = arr[-4:]
    if len(arr) >= 3:
        if arr[-1] == arr[-2]:
            return True
        if len(set(arr[-3:])) == 1:
            return True
    return False

@app.post("/v1/context")
def context(req: ContextRequest):
    merchant_memory[req.context_id] = req.dict()
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for trig in req.available_triggers:
        if trig == "sales_dip":
            body = "Orders slowed nearby this week. Launch a dinner combo + comeback SMS campaign tonight."
            cta = "Recover Sales"
        elif trig == "festival_push":
            body = "Festival demand is rising nearby. Promote festive specials and family bundles today."
            cta = "Run Festival Push"
        elif trig == "competitor_spike":
            body = "Nearby competitors are trending. Win repeat customers back with loyalty rewards now."
            cta = "Win Customers Back"
        elif trig == "rain_alert":
            body = "Rain expected today. Push delivery bundles and priority convenience offers."
            cta = "Boost Delivery"
        elif trig == "regulation_change":
            body = "Compliance update released. Review operations, pricing notices, and customer messaging today."
            cta = "Review Update"
        else:
            body = "Fresh local demand signal detected. Launch a quick campaign today."
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

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    category = detect_category(req.merchant_id)
    name = merchant_name(req.merchant_id)
    stop_words = [
        "stop", "unsubscribe", "spam",
        "leave me alone", "dont message",
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
                "body": f"Thanks! Your booking request has been sent to {name}. You'll receive confirmation shortly."
            }
        if any(x in msg for x in ["price", "cost", "menu", "charges"]):
            return {
                "action": "send",
                "body": f"Thanks! {name} will share pricing details with you shortly."
            }
        if any(x in msg for x in ["timing", "hours", "open", "close"]):
            return {
                "action": "send",
                "body": f"Thanks for checking in. {name} will confirm opening hours shortly."
            }
        if any(x in msg for x in ["order", "buy", "delivery"]):
            return {
                "action": "send",
                "body": f"Thanks! Your order request has been sent to {name} for quick assistance."
            }
        return {
            "action": "send",
            "body": f"Thanks for contacting {name}. Your message has been shared with the merchant."
        }
    if category in ["clinic", "healthcare"] or any(
        x in msg for x in ["clinic", "doctor", "x-ray", "patient", "scan", "dentist", "hospital"]
    ):
        return {
            "action": "send",
            "body": "Increase patient bookings using Google Maps visibility, recall reminders, same-day diagnostics, doctor referrals, and review growth."
        }
    if category == "salon" or any(
        x in msg for x in ["salon", "spa", "beauty", "hair"]
    ):
        return {
            "action": "send",
            "body": "Increase bookings using bridal packages, rebooking reminders, referral rewards, makeover reels, and festive beauty offers."
        }
    if category == "gym" or any(
        x in msg for x in ["gym", "fitness", "trainer", "workout"]
    ):
        return {
            "action": "send",
            "body": "Grow memberships using free trials, referral rewards, body-transformation stories, retention plans, and class upsells."
        }
    if category in ["education", "academy"] or any(
        x in msg for x in ["tuition", "academy", "coaching", "school"]
    ):
        return {
            "action": "send",
            "body": "Increase enrollments using demo classes, topper success stories, parent trust campaigns, referrals, and exam-season offers."
        }
    if category == "restaurant" or any(
        x in msg for x in ["pizza", "food", "restaurant", "cafe", "orders", "table"]
    ):
        return {
            "action": "send",
            "body": "Grow orders using lunch combos, Google review boosts, delivery promos, repeat-diner rewards, and weekend family offers."
        }
    if any(x in msg for x in ["sales", "dropping", "decline", "down"]):
        return {
            "action": "send",
            "body": "Recover sales using limited-time bundles, reactivation offers, local ads, referral pushes, and repeat-customer rewards."
        }
    if any(x in msg for x in ["growth", "help", "customer", "acquire"]):
        return {
            "action": "send",
            "body": "Acquire new customers using first-order offers, strong reviews, referral incentives, WhatsApp follow-ups, and local targeting."
        }
    return {
        "action": "send",
        "body": "I can help improve customer acquisition, repeat sales, promotions, visibility, and business growth."
    }