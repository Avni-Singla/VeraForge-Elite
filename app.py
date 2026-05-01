from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
import os

app = FastAPI(
    title="VeraForge Elite",
    version="2.0"
)

MEMORY = {}
class ContextRequest(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: dict
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
        background:linear-gradient(135deg,#07152d,#11284f);
        font-family:Arial;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;
    }
    .card{
        background:rgba(255,255,255,0.08);
        padding:50px;
        border-radius:20px;
        text-align:center;
        width:700px;
    }
    a{
        display:inline-block;
        margin:10px;
        padding:14px 24px;
        border-radius:10px;
        text-decoration:none;
        color:white;
        font-weight:bold;
    }
    .g{background:#22c55e;}
    .b{background:#3b82f6;}
    .p{background:#9333ea;}
    </style>
    </head>
    <body>
        <div class="card">
            <h1> VeraForge Elite 2.0</h1>
            <h2>Winning Merchant AI Engine</h2>
            <p>Smart Triggering • Contextual Replies • High Conversion Actions</p>
            <a class='g' href='/docs'>API Docs</a>
            <a class='b' href='/v1/healthz'>Health</a>
            <a class='p' href='/v1/metadata'>Metadata</a>
        </div>
    </body>
    </html>
    """

@app.get("/v1/healthz")
def health():
    return {"ok": True, "status": "healthy"}

@app.get("/v1/metadata")
def metadata():
    return {
        "name": "VeraForge Elite",
        "version": "2.0.0",
        "creator": "Avni Singla",
        "mode": "Winning Edition"
    }

@app.post("/v1/context")
def push_context(req: ContextRequest):
    MEMORY[req.context_id] = req.payload
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for merchant_id, data in MEMORY.items():
        name = data["identity"]["name"]
        locality = data["identity"]["locality"]
        category = data["category_slug"]
        for trig in req.available_triggers:
            body = compose_trigger_message(
                trig, name, locality, category
            )
            actions.append({
                "trigger_id": trig,
                "merchant_id": merchant_id,
                "customer_id": None,
                "body": body,
                "cta": "Yes, launch it",
                "send_as": "vera"
            })
    return {"actions": actions}

def compose_trigger_message(trigger, name, locality, category):
    if trigger == "sales_dip":
        return f"{name}: Orders in {locality} dipped recently. Launch a comeback offer today?"
    elif trigger == "dormant_users":
        return f"{name}: Repeat customers have gone inactive. Send a loyalty reward to bring them back?"
    elif trigger == "festival_push":
        return f"{name}: Local festive demand is rising in {locality}. Promote a limited-time special?"
    elif trigger == "regulation_change":
        return f"{name}: Customers now prefer compliant and modern {category} businesses. Promote your trust factor?"
    elif trigger == "competitor_spike":
        return f"{name}: Nearby competitors are gaining attention. Run a smart counter-offer now?"
    elif trigger == "weather_opportunity":
        return f"{name}: Weather shift in {locality} can increase demand today. Push a timely campaign?"
    return f"{name}: Opportunity detected. Promote your business now?"

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    stop_words = ["stop", "unsubscribe", "spam", "useless", "don't message"]
    if any(x in msg for x in stop_words):
        return {
            "action": "end",
            "body": "Understood. Messaging has been stopped. We’ll only reconnect if requested."
        }
    if req.from_role == "customer":
        if "book" in msg or "appointment" in msg:
            return {
                "action": "send",
                "body": "Your booking request has been shared with the merchant. They’ll confirm shortly."
            }
        if "price" in msg or "cost" in msg:
            return {
                "action": "send",
                "body": "Thanks for your interest. The merchant will share pricing details soon."
            }
        return {
            "action": "send",
            "body": "Thanks for reaching out. Your message has been forwarded to the merchant."
        }

    if req.from_role == "merchant":
        if "x-ray" in msg or "audit" in msg:
            return {
                "action": "send",
                "body": "I recommend promoting upgraded diagnostic quality and patient safety to attract new customers."
            }
        if "help" in msg or "growth" in msg:
            return {
                "action": "send",
                "body": "I can help boost repeat customers, local visibility, and campaign conversions."
            }
        return {
            "action": "send",
            "body": "Understood. I’ll optimize the next growth opportunity for your business."
        }
    return {
        "action": "send",
        "body": "Message received."
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)