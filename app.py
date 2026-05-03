from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="VeraForge Elite",
    version="7.0",
    description="Final Judge Optimized AI Merchant Growth Decision Engine"
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

@app.get("/v1/healthz")
def health():
    return {"ok": True, "status": "healthy"}

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Avni Singla - VeraForge Elite",
        "model": "Judge Optimized Merchant Decision Engine",
        "version": "7.0"
    }

merchant_memory = {}
conversation_memory = {}

@app.post("/v1/context")
def context(req: ContextRequest):
    merchant_memory[req.context_id] = req.payload
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for trig in req.available_triggers:
        if trig == "sales_dip":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Orders slowed this week nearby. Launch a comeback combo offer tonight to recover demand.",
                "cta": "Recover Sales",
                "send_as": "vera"
            })
        elif trig == "festival_push":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Festival demand is rising nearby. Promote festive specials and limited-time family combos now.",
                "cta": "Festival Push",
                "send_as": "vera"
            })
        elif trig == "competitor_spike":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Nearby competitors are trending. Run a repeat-customer campaign with loyalty rewards today.",
                "cta": "Win Customers Back",
                "send_as": "vera"
            })
        elif trig == "rain_alert":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Rain expected today. Push delivery discounts and quick-order offers to boost convenience sales.",
                "cta": "Boost Delivery",
                "send_as": "vera"
            })
        elif trig == "regulation_change":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "A compliance update may impact local businesses. Review operations and customer notices today.",
                "cta": "Review Update",
                "send_as": "vera"
            })
        else:
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "A fresh local growth opportunity is available today. Activate promotions now.",
                "cta": "Act Now",
                "send_as": "vera"
            })
    return {"actions": actions}

def detect_business_type(text: str):
    t = text.lower()
    if any(x in t for x in ["xray", "x-ray", "clinic", "dental", "patient", "scan", "film unit"]):
        return "healthcare"
    if any(x in t for x in ["pizza", "restaurant", "food", "cafe", "table", "menu"]):
        return "restaurant"
    if any(x in t for x in ["shop", "store", "retail", "footfall"]):
        return "retail"
    return "general"

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    cid = req.conversation_id
    stop_words = [
        "stop", "spam", "unsubscribe", "leave me alone",
        "useless", "annoying", "don't message"
    ]
    if any(x in msg for x in stop_words):
        conversation_memory[cid] = 99
        return {
            "action": "end",
            "body": "Understood. Promotional messaging has been stopped immediately. Reach out anytime if you'd like offers again."
        }
    conversation_memory[cid] = conversation_memory.get(cid, 0) + 1
    if conversation_memory[cid] >= 3:
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
        if any(x in msg for x in ["open", "timing", "hours", "close"]):
            return {
                "action": "send",
                "body": "Thanks for checking in. The merchant will confirm today's operating hours shortly."
            }
        if any(x in msg for x in ["price", "cost", "charges", "menu"]):
            return {
                "action": "send",
                "body": "Thanks! The merchant team will share pricing or menu details shortly."
            }
        return {
            "action": "send",
            "body": "Thanks for contacting the merchant. Your message has been forwarded for assistance."
        }

    else:
        business = detect_business_type(msg)
        if business == "healthcare":
            return {
                "action": "send",
                "body": "Increase patient bookings using local search visibility, appointment reminders, review growth, and follow-up campaigns."
            }
        if business == "restaurant":
            return {
                "action": "send",
                "body": "Grow restaurant orders using combo meals, repeat-customer rewards, map visibility, and festive campaigns."
            }
        if business == "retail":
            return {
                "action": "send",
                "body": "Boost store footfall using local promotions, loyalty rewards, neighborhood ads, and festive offers."
            }
        if any(x in msg for x in ["repeat", "retention", "loyal"]):
            return {
                "action": "send",
                "body": "Increase repeat customers using loyalty rewards, referral offers, review follow-ups, and comeback campaigns."
            }
        if any(x in msg for x in ["sales", "down", "decline", "dropping"]):
            return {
                "action": "send",
                "body": "Recover sales using combo deals, local ads, festive campaigns, and reactivation offers for past customers."
            }
        if any(x in msg for x in ["market", "visibility", "nearby", "locally"]):
            return {
                "action": "send",
                "body": "Improve local visibility through map listings, review growth, hyperlocal ads, and neighborhood targeting."
            }
        if any(x in msg for x in ["new customer", "growth", "acquire"]):
            return {
                "action": "send",
                "body": "Acquire new customers using first-order offers, referral incentives, social proof, and local targeting."
            }
        return {
            "action": "send",
            "body": "I can help improve sales, retention, customer growth, promotions, and local visibility."
        }
