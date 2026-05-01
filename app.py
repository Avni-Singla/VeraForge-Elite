from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="VeraForge Elite",
    version="6.0",
    description="Ultimate AI Merchant Growth Decision Engine"
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
        "model": "Adaptive Merchant Decision Engine",
        "version": "6.0"
    }

memory = {}

@app.post("/v1/context")
def context(req: ContextRequest):
    memory[req.context_id] = req.payload
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
                "body": "Orders slowed recently in your area. Launch a comeback combo offer today.",
                "cta": "Recover Sales",
                "send_as": "vera"
            })
        elif trig == "festival_push":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Festival demand is rising nearby. Promote festive specials and limited-time deals now.",
                "cta": "Run Festival Push",
                "send_as": "vera"
            })
        elif trig == "competitor_spike":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Nearby competitors are trending. Run a smart retention campaign immediately.",
                "cta": "Win Customers Back",
                "send_as": "vera"
            })
        elif trig == "rain_alert":
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "Rain expected today. Push delivery-focused offers to increase convenience orders.",
                "cta": "Boost Delivery",
                "send_as": "vera"
            })
        else:
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": "A fresh growth opportunity is available today.",
                "cta": "Act Now",
                "send_as": "vera"
            })
    return {"actions": actions}

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    stop_words = [
        "stop", "spam", "unsubscribe", "leave me alone",
        "useless", "annoying", "don't message"
    ]
    if any(x in msg for x in stop_words):
        return {
            "action": "end",
            "body": "Understood. Promotional messaging has been stopped immediately. Reach out anytime if you'd like offers again."
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
                "body": "Thanks for reaching out. Your order request has been shared with the merchant team for quick assistance."
            }
        if any(x in msg for x in ["open", "timing", "hours", "close"]):
            return {
                "action": "send",
                "body": "The merchant will confirm operating hours shortly. Thanks for checking in."
            }
        if any(x in msg for x in ["price", "cost", "charges", "menu"]):
            return {
                "action": "send",
                "body": "The merchant team will share pricing details shortly."
            }
        return {
            "action": "send",
            "body": "Thanks for contacting the merchant. Your message has been forwarded for assistance."
        }
    else:
        if any(x in msg for x in ["repeat", "retention", "loyal"]):
            return {
                "action": "send",
                "body": "Increase repeat customers using loyalty rewards, referral offers, review follow-ups, and personalized comeback campaigns."
            }
        if any(x in msg for x in ["sales dropping", "sales", "down", "decline"]):
            return {
                "action": "send",
                "body": "Recover sales with combo deals, local ads, festive campaigns, and reactivation offers for past customers."
            }
        if any(x in msg for x in ["market", "visibility", "locally", "nearby"]):
            return {
                "action": "send",
                "body": "Improve local visibility through map listings, hyperlocal ads, review growth, and neighborhood targeting."
            }
        if any(x in msg for x in ["new customer", "acquire", "growth"]):
            return {
                "action": "send",
                "body": "Acquire new customers using first-order offers, referral incentives, local targeting, and social proof campaigns."
            }
        return {
            "action": "send",
            "body": "I can help with growth strategy, retention, promotions, visibility, and merchant performance optimization."
        }
    