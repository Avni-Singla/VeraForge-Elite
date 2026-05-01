from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import random
import re

app = FastAPI(
    title="VeraForge Elite",
    version="2.0",
    description="Version - Contextual Merchant AI Engine"
)

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
                background:linear-gradient(135deg,#08111f,#12284a,#0a1322);
                color:white;
                text-align:center;
                padding-top:120px;
            }
            .box{
                width:760px;
                margin:auto;
                padding:50px;
                background:rgba(255,255,255,0.08);
                border-radius:24px;
                box-shadow:0 0 40px rgba(0,0,0,0.4);
            }
            h1{
                font-size:58px;
                color:#44c2ff;
            }
            p{
                font-size:24px;
                color:#ddd;
            }
            a{
                display:inline-block;
                margin:15px;
                padding:16px 28px;
                border-radius:14px;
                color:white;
                text-decoration:none;
                font-weight:bold;
            }
            .b1{background:#18c964;}
            .b2{background:#3b82f6;}
            .b3{background:#9333ea;}
        </style>
    </head>
    <body>
        <div class='box'>
            <h1> VeraForge Elite</h1>
            <p>Winning AI Merchant Engagement Engine</p>
            <a class='b1' href='/docs'>API Docs</a>
            <a class='b2' href='/v1/healthz'>Health</a>
            <a class='b3' href='https://github.com/Avni-Singla/VeraForge-Elite'>GitHub</a>
            <p style='font-size:18px;margin-top:30px;'>Built by Avni Singla • Version 2.0</p>
        </div>
    </body>
    </html>
    """

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

def detect_category(mid):
    if mid in merchant_memory:
        return merchant_memory[mid].get("category_slug", "business")
    return "business"

def detect_name(mid):
    if mid in merchant_memory:
        return merchant_memory[mid]["name"]
    return "Merchant"

@app.get("/v1/healthz")
def health():
    return {"ok": True, "status": "healthy"}

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "Avni Singla - VeraForge Elite",
        "model": "Adaptive Merchant Decision Engine",
        "version": "2.0"
    }

@app.post("/v1/context")
def context(req: ContextRequest):
    merchant_memory[req.context_id] = {
        "name": req.payload["identity"]["name"],
        "locality": req.payload["identity"]["locality"],
        "category_slug": req.payload.get("category_slug", "business")
    }
    return {"accepted": True}

@app.post("/v1/tick")
def tick(req: TickRequest):
    actions = []
    for mid, info in merchant_memory.items():
        category = info["category_slug"]
        name = info["name"]
        locality = info["locality"]
        for trig in req.available_triggers:
            if trig == "sales_dip":
                body = f"{name} orders dipped in {locality}. Launch a comeback offer today."
                cta = "Recover Sales"
            elif trig == "festival_push":
                body = f"Festive demand is rising near {locality}. Promote a limited-time special."
                cta = "Run Festival Campaign"
            elif trig == "competitor_spike":
                body = f"Nearby competitors are gaining attention. Counter with a smart promo now."
                cta = "Win Customers Back"
            elif trig == "rainy_day":
                body = f"Rainy weather detected. Push delivery-first offers today."
                cta = "Push Delivery Offer"
            else:
                body = f"New opportunity detected for {name}."
                cta = "Act Now"
            actions.append({
                "trigger_id": trig,
                "merchant_id": mid,
                "customer_id": None,
                "body": body,
                "cta": cta,
                "send_as": "vera"
            })
    return {"actions": actions[:3]}

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    msg = req.message.lower()
    if "stop" in msg or "spam" in msg or "useless" in msg:
        return {
            "action": "end",
            "body": "Understood. Messaging has been stopped immediately."
        }
    if req.from_role == "customer":
        if "book" in msg or "appointment" in msg:
            return {
                "action": "send",
                "body": "Your booking request has been shared with the merchant. Confirmation will follow shortly."
            }
        if "price" in msg or "cost" in msg:
            return {
                "action": "send",
                "body": "Thanks for your interest. The merchant will share pricing details shortly."
            }
        if "time" in msg or "open" in msg:
            return {
                "action": "send",
                "body": "Your query has been forwarded. The merchant will confirm timings soon."
            }
        return {
            "action": "send",
            "body": "Thanks for reaching out. The merchant has received your message."
        }
    if req.from_role == "merchant":
        if "repeat" in msg:
            return {
                "action": "send",
                "body": "To increase repeat customers: run loyalty rewards, comeback offers, and review follow-ups."
            }
        if "sales" in msg:
            return {
                "action": "send",
                "body": "I recommend urgent recovery campaigns, festive offers, and local visibility boosts."
            }
        if "help" in msg:
            return {
                "action": "send",
                "body": "I can help with growth campaigns, retention strategy, customer acquisition, and local demand generation."
            }
        return {
            "action": "send",
            "body": "I’m ready to help optimize your growth and customer engagement."
        }
    return {
        "action": "send",
        "body": "Message received."
    }
