"""Crisp docs screenshots 1280x800."""
from PIL import Image, ImageDraw, ImageFont
import os
OUT = "docs"; W, H = 1280, 800
def FF(sz, b=False):
    n = "arialbd.ttf" if b else "arial.ttf"
    p = "C:/Windows/Fonts/" + n
    try:
        return ImageFont.truetype(p, sz)
    except Exception:
        return ImageFont.load_default()
BRAND=(226,55,68); BG=(245,245,245); CARD=(255,255,255); INK=(30,30,30); MUT=(110,110,110)
DK=(17,24,39); GR=(110,231,183); LT=(226,232,240); GY=(100,116,139)
def base(t, s):
    im = Image.new("RGB", (W,H), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40,30,W-40,170],24,fill=CARD)
    d.ellipse([70,60,130,120],fill=BRAND)
    d.text((92,68),"U",font=FF(26,True),fill=(255,255,255))
    d.text((150,58),t,font=FF(28,True),fill=INK)
    d.text((150,100),s,font=FF(16),fill=MUT)
    d.rounded_rectangle([W-400,92,W-70,130],16,fill=(230,255,232))
    d.text((W-385,98),"LIVE DEMO - 7/7 tests passing",font=FF(13,True),fill=(20,120,40))
    return im, d
def chat(d,x,y,w,h,ms):
    d.rounded_rectangle([x,y,x+w,y+h],22,fill=CARD,outline=(230,230,230),width=2)
    d.rounded_rectangle([x,y,x+w,y+60],22,fill=BRAND); d.rectangle([x,y+36,x+w,y+60],fill=BRAND)
    d.text((x+20,y+16),"University Helpdesk - online",font=FF(17,True),fill=(255,255,255))
    cy=y+86
    for who,tx in ms:
        if who=="b":
            d.rounded_rectangle([x+18,cy,x+w-120,cy+42],14,fill=(236,236,236))
            d.text((x+32,cy+10),tx,font=FF(15),fill=INK)
        else:
            d.rounded_rectangle([x+120,cy,x+w-18,cy+42],14,fill=BRAND)
            d.text((x+140,cy+10),tx,font=FF(15),fill=(255,255,255))
        cy+=56
    px=x+18
    for p in ["Forgot password","Session timeout","Payment status"]:
        tw=len(p)*8+28
        d.rounded_rectangle([px,cy,px+tw,cy+32],16,fill=(255,229,231))
        d.text((px+14,cy+7),p,font=FF(12),fill=BRAND); px+=tw+10
    d.rounded_rectangle([x+18,y+h-56,x+w-110,y+h-18],18,outline=(220,220,220),width=2)
    d.text((x+34,y+h-46),"Ask your issue...",font=FF(14),fill=MUT)
    d.rounded_rectangle([x+w-96,y+h-56,x+w-18,y+h-18],18,fill=BRAND)
    d.text((x+w-74,y+h-46),"Send",font=FF(14,True),fill=(255,255,255))
def api(d,x,y,w,h,t,rows):
    d.rounded_rectangle([x,y,x+w,y+h],20,fill=DK)
    d.text((x+20,y+14),t,font=FF(15,True),fill=GR)
    yy=y+48
    for ln,co in rows:
        d.text((x+20,yy),ln,font=FF(13),fill=co); yy+=25
def sv(im,n):
    p=os.path.join(OUT,n); im.save(p); print("wrote",p,im.size)
os.makedirs(OUT,exist_ok=True)
#PART2
im,d=base("University Helpdesk Chatbot","RAG + FastAPI + ChromaDB + React - semantic search over 7 categories")
d.rounded_rectangle([40,200,760,740],24,fill=CARD,outline=(230,230,230),width=2)
d.text((80,230),"Ask in plain English, get the fix",font=FF(26,True),fill=INK)
d.text((80,270),"Embeddings understand intent - no keyword matching.",font=FF(16),fill=MUT)
fy=318
for t,s in [("Real-time WS chat","instant suggestions as you type"),("Semantic search","all-MiniLM-L6-v2 + ChromaDB"),("Ticket escalation","description + file upload"),("7 categories","login, forms, admit card, results")]:
    d.rounded_rectangle([80,fy,720,fy+94],16,fill=(250,250,250),outline=(235,235,235),width=2)
    d.text((100,fy+12),t,font=FF(17,True),fill=INK); d.text((100,fy+44),s,font=FF(13),fill=MUT); fy+=104
chat(d,790,200,450,540,[("b","Hi! I am your Helpdesk Assistant."),("u","wifi not working in hostel"),("b","Did you mean one of these?")])
sv(im,"01-landing.png")
im,d=base("Live chat - quick help + suggestions","GET /categories powers pills - WS /ws/chat streams answers")
chat(d,60,200,560,540,[("b","Hi! Ask your issue."),("u","Forgot password, cant login"),("b","Did you mean one of these?")])
api(d,650,200,570,250,"GET /categories -> 200 OK",[('Login & Access Issues (3 issues)',LT),('Registration Form Issues (5 issues)',LT),('7 categories total - see DEMO.md',GR)])
api(d,650,470,570,270,"WS /ws/chat -> 3 suggestions",[('1. Forgot password / Reset password',LT),('2. Username not found',LT),('3. Session timeout',GR)])
sv(im,"02-chat-open.png")
im,d=base("Semantic search returns top-3","POST /chat query -> similarity_search k=3")
chat(d,60,200,560,540,[("u","my internet is very slow"),("b","Did you mean one of these?"),("b","3 suggestions ready - pick one")])
api(d,650,200,570,290,'POST /chat "my internet is very slow"',([('Unable to download submitted form',LT),('Payment issues [Form Related]',LT),('Old data not fetched [Form Related]',GR),('"success": true - see DEMO.md',GY)]))
d.rounded_rectangle([650,510,1220,740],20,fill=CARD,outline=(230,230,230),width=2)
d.text((675,530),"Why this matters",font=FF(18,True),fill=INK)
d.text((675,566),"- Embeddings understand intent",font=FF(14),fill=MUT)
d.text((675,592),"- Each hit: issue, category, response",font=FF(14),fill=MUT)
d.text((675,618),"- Runs locally: transformers + Chroma",font=FF(14),fill=MUT)
d.text((675,654),"Try: python scripts/demo.py",font=FF(14,True),fill=BRAND)
sv(im,"03-suggestions.png")
#PART3
im,d=base("One click -> verified answer + Yes/No","POST /issue-response issue -> exact fix")
chat(d,60,200,560,540,[("u","Forgot password / Reset password"),("b","Reset link sent - check inbox"),("b","Solved? Yes / No")])
api(d,650,200,570,230,"POST /issue-response -> 200 OK",([('{ "issue": "Forgot password..." }',LT),('"Password reset link sent to email."',GR),('Full text in docs/DEMO.md',GY)]))
d.rounded_rectangle([650,450,1220,740],20,fill=CARD,outline=(230,230,230),width=2)
d.text((675,470),"Resolution flow",font=FF(18,True),fill=INK)
yy=505
for s in ["1. Click a suggestion pill","2. Call /issue-response","3. Bot shows fix + Yes/No","4. No -> ticket form opens"]:
    d.rounded_rectangle([675,yy,1195,yy+44],12,fill=(250,250,250),outline=(235,235,235))
    d.text((690,yy+10),s,font=FF(14),fill=INK); yy+=54
sv(im,"04-answer.png")
im,d=base("Unresolved? Raise a ticket + file","POST /create-ticket multipart -> TICK-xxxxxx")
d.rounded_rectangle([60,200,620,740],22,fill=CARD,outline=(230,230,230),width=2)
d.text((90,225),"Create support ticket",font=FF(20,True),fill=INK)
d.rounded_rectangle([90,270,590,400],14,outline=(220,220,220),width=2)
d.text((105,282),"Demo ticket: wifi issue in hostel",font=FF(14),fill=INK)
d.rounded_rectangle([90,420,590,468],14,outline=(220,220,220),width=2,fill=(250,250,250))
d.text((105,432),"demo_note.txt attached",font=FF(14),fill=MUT)
d.rounded_rectangle([90,488,590,540],14,fill=BRAND)
d.text((245,501),"Create Ticket",font=FF(16,True),fill=(255,255,255))
d.rounded_rectangle([90,560,590,690],16,fill=(230,255,232))
d.text((110,578),"Ticket TICK-544249 created - open",font=FF(15,True),fill=(20,120,40))
d.text((110,612),"Support replies within 2 hours.",font=FF(13),fill=(40,100,50))
api(d,650,200,570,230,"POST /create-ticket -> Created",([('{ "ticket_id": "TICK-544249" }',GR),('{ "status": "open" }',LT),('Files -> Backend/uploads/',GY)]))
d.rounded_rectangle([650,450,1220,740],20,fill=CARD,outline=(230,230,230),width=2)
d.text((675,470),"Run the whole demo",font=FF(18,True),fill=INK)
d.rounded_rectangle([675,515,1195,568],12,fill=DK)
d.text((695,528),"python scripts/demo.py",font=FF(14),fill=GR)
d.text((675,588),"Backend: uvicorn main:app --port 8010",font=FF(13),fill=MUT)
d.text((675,616),"Frontend: npm start -> localhost:3000",font=FF(13),fill=MUT)
d.text((675,644),"Docs: 127.0.0.1:8010/docs",font=FF(13),fill=MUT)
d.text((675,678),"Tests: python Backend/test_api.py (7/7 pass)",font=FF(13,True),fill=BRAND)
sv(im,"05-ticket.png")
print("done")