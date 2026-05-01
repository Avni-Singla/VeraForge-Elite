from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import re

app = FastAPI(
    title="VeraForge Elite",
    version="5.0",
    description="Adaptive Merchant Decision Engine"
)

merchant_memory = {}

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
        background:linear-gradient(135deg,#07111f,#142b4d,#07111f);
        color:white;
        font-family:Arial;
        text-align:center;
        padding-top:120px;
    }
    h1{font-size:58px;margin-bottom:10px;color:#4fc3ff;}
    p{font-size:24px;color:#d0d0d0;}
    .btn{
        display:inline-block;
        margin:15px;
        padding:16px 28px;
        border-radius:12px;
        text-decoration:none;
        color:white;
        font-weight:bold;
        background:#1f8fff;
    }
    </style>
    </head>
    <body>
        <h1>VeraForge Elite</h1>
        <p>AI Merchant Growth Decision Engine</p>
        <a class='btn' href='/docs'>API Docs</a>
        <a class='btn' href='/v1/healthz'>Health</a>
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
        "version": "5.0"
    }

@app.post("/v1/context")
def context(req: ContextRequest):
    merchant_memory[req.context_id] = req.payload
    return {"accepted": True}

def get_info(mid):
    data = merchant_memory.get(mid, {})
    identity = data.get("identity", {})
    return {
        "name": identity.get("name", "Your Business"),
        "locality": identity.get("locality", "your area"),
        "category": data.get("category_slug", "business")
    }

def restaurant_trigger(name, locality, trig):
    if trig == "sales_dip":
        return {
            "trigger_id": trig,
            "merchant_id": "m1",
            "customer_id": None,
            "body": f"{name} orders in {locality} slowed recently. Launch a Buy 1 Get 1 weekday combo to recover traffic fast.",
            "cta": "Recover Sales",
            "send_as": "vera"
        }
    if trig == "festival_push":
        return {
            "trigger_id": trig,
            "merchant_id": "m1",
            "customer_id": None,
            "body": f"Festive demand is rising near {locality}. Promote a limited-time family meal combo this weekend.",
            "cta": "Launch Festival Offer",
            "send_as": "vera"
        }
    if trig == "competitor_spike":
        return {
            "trigger_id": trig,
            "merchant_id": "m1",
            "customer_id": None,
            "body": f"Nearby competitors are gaining attention in {locality}. Run a 20% first-order promo today.",
            "cta": "Win Customers Back",
            "send_as": "vera"
        }
    return {
        "trigger_id": trig,
        "merchant_id": "m1",
        "customer_id": None,
        "body": f"Opportunity detected for {name}. Take action now.",
        "cta": "Grow Now",
        "send_as": "vera"
    }

@app.post("/v1/tick")
def tick(req: TickRequest):
    info = get_info("m1")
    name = info["name"]
    locality = info["locality"]
    category = info["category"]
    actions = []
    for trig in req.available_triggers:
        if category == "restaurant":
            actions.append(restaurant_trigger(name, locality, trig))
        else:
            actions.append({
                "trigger_id": trig,
                "merchant_id": "m1",
                "customer_id": None,
                "body": f"{name} has a growth opportunity in {locality}.",
                "cta": "Act Now",
                "send_as": "vera"
            })
    return {"actions": actions}

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    info = get_info(req.merchant_id)
    name = info["name"]
    locality = info["locality"]
    msg = req.message.lower()
    if any(x in msg for x in [
        "stop", "spam", "shut up", "useless", "don't message",
        "do not message", "leave me", "annoying"
    ]):
        return {
            "action": "end",
            "body": "Understood. Promotional messaging has been stopped immediately. Reach out anytime if you'd like offers again."
        }
    if req.from_role == "customer":
        if any(x in msg for x in [
            "book", "table", "reserve", "reservation"
        ]):
            return {
                "action": "send",
                "body": f"Thanks! Your booking request has been shared with {name}. You’ll receive confirmation shortly."
            }
        if any(x in msg for x in [
            "order", "menu", "delivery", "food"
        ]):
            return {
                "action": "send",
                "body": f"Thanks for reaching out to {name}. Your request has been shared and the team will assist shortly."
            }
        if any(x in msg for x in [
            "open", "timing", "hours", "close"
        ]):
            return {
                "action": "send",
                "body": f"{name} will confirm operating hours shortly. Thanks for checking in."
            }
        return {
            "action": "send",
            "body": f"Thanks for contacting {name}. Your message has been shared with the team."
        }
    if req.from_role == "merchant":
        if any(x in msg for x in [
            "sales", "dropping", "low sales", "decline"
        ]):
            return {
                "action": "send",
                "body": f"To recover {name}'s sales in {locality}: run combo offers, boost local ads, and activate repeat-customer campaigns."
            }
        if any(x in msg for x in [
            "repeat", "loyal", "customers"
        ]):
            return {
                "action": "send",
                "body": "Increase repeat customers using loyalty rewards, review follow-ups, referral offers, and personalized comeback deals."
            }
        if any(x in msg for x in [
            "marketing", "grow", "promotion"
        ]):
            return {
                "action": "send",
                "body": f"Recommended growth plan for {name}: festive promos, Google review drive, local awareness ads, and retention offers."
            }
        return {
            "action": "send",
            "body": "I can help with growth strategy, customer retention, promotions, and visibility improvement."
        }
    return {
        "action": "send",
        "body": "Message received successfully."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
