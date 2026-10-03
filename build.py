#!/usr/bin/env python3
"""Build the Hidden Payouts static site from the lab's settlements.json.
Reads ../lab/lab14-hidden-payouts-watch/settlements.json, writes index.html.
Deploy: git add -A && git commit -m ... && git push origin main
"""
import json, os, datetime, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'lab', 'lab14-hidden-payouts-watch', 'settlements.json')
OUT = os.path.join(HERE, 'index.html')
today = datetime.date(2026, 10, 2)

items = json.load(open(DATA))
verified = [i for i in items if i.get('status') == 'open']
leads = [i for i in items if i.get('status') != 'open']

def days_left(d):
    try:
        y, m, dd = map(int, d.split('-'))
        return (datetime.date(y, m, dd) - today).days
    except Exception:
        return None

def fmt_deadline(d):
    n = days_left(d)
    if n is None or not d:
        return '<span class="dl unknown">Deadline: check official site</span>'
    try:
        y, m, dd = map(int, d.split('-'))
        label = datetime.date(y, m, dd).strftime('%b %d, %Y')
    except Exception:
        label = d
    cls = 'urgent' if n <= 30 else 'soon' if n <= 60 else 'ok'
    extra = f' — <b>{n} days left</b>' if n >= 0 else ' — <b>deadline may have passed, verify</b>'
    return f'<span class="dl {cls}">File by {label}{extra}</span>'

def card(i):
    return f"""
    <article class="card">
      <h3>{html.escape(i.get('title',''))}</h3>
      <p class="payout">{html.escape(i.get('payout',''))}</p>
      <p class="who"><b>Who qualifies:</b> {html.escape(i.get('who',''))}</p>
      <p>{fmt_deadline(i.get('claim_deadline',''))}</p>
      <p class="links">
        <a class="btn" href="{html.escape(i.get('claim_url',''), quote=True)}" rel="noopener">File a claim (official site)</a>
        <a class="src" href="{html.escape(i.get('source_url',''), quote=True)}" rel="noopener">Source: {html.escape(i.get('source',''))}</a>
      </p>
      <p class="verified">Verified {html.escape(i.get('verified',''))}</p>
    </article>"""

def lead_row(i):
    return (f'<li><a href="{html.escape(i.get("claim_url") or i.get("source_url",""), quote=True)}" rel="noopener">'
            f'{html.escape(i.get("title",""))}</a> '
            f'<span class="tag">via {html.escape(i.get("source",""))} — details being verified</span></li>')

cards = '\n'.join(card(i) for i in verified)
lead_list = '\n'.join(lead_row(i) for i in leads[:24])

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hidden Payouts — open settlements & unclaimed money</title>
<meta name="description" content="Currently-open class-action settlements with filing deadlines, plus where to check for unclaimed money in your name. Updated hourly.">
<style>
:root {{--ink:#1a2b1f; --green:#1e7a3c; --bg:#f4f7f4; --card:#fff; --urgent:#b3261e;}}
* {{box-sizing:border-box}}
body {{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; margin:0; background:var(--bg); color:var(--ink); line-height:1.55}}
header {{background:#12351f; color:#fff; padding:2.2rem 1.2rem; text-align:center}}
header h1 {{margin:0 0 .4rem; font-size:1.9rem}}
header p {{margin:.2rem 0; opacity:.92}}
main {{max-width:960px; margin:0 auto; padding:1.4rem 1rem 3rem}}
h2 {{color:#12351f; border-bottom:3px solid var(--green); padding-bottom:.3rem; margin-top:2.4rem}}
.card {{background:var(--card); border:1px solid #dfe7df; border-left:6px solid var(--green); border-radius:10px; padding:1.1rem 1.2rem; margin:1rem 0; box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.card h3 {{margin:.1rem 0 .5rem; font-size:1.15rem}}
.payout {{font-weight:700; color:var(--green); margin:.3rem 0}}
.who {{margin:.3rem 0}}
.dl {{display:inline-block; padding:.25rem .6rem; border-radius:6px; font-size:.92rem; margin:.4rem 0}}
.dl.urgent {{background:#fdecea; color:var(--urgent); font-weight:700}}
.dl.soon {{background:#fff4e0; color:#8a5a00; font-weight:600}}
.dl.ok {{background:#e6f4ea; color:#14632e}}
.dl.unknown {{background:#eee; color:#555}}
.links {{margin:.7rem 0 .2rem}}
.btn {{display:inline-block; background:var(--green); color:#fff; text-decoration:none; padding:.55rem 1.1rem; border-radius:8px; font-weight:700; margin-right:.7rem}}
.btn:hover {{background:#155c2d}}
.src {{font-size:.88rem; color:#555}}
.verified {{font-size:.78rem; color:#888; margin:.4rem 0 0}}
ul.leads {{padding-left:1.2rem}}
ul.leads li {{margin:.35rem 0}}
.tag {{font-size:.8rem; color:#8a5a00; background:#fff4e0; padding:.1rem .45rem; border-radius:5px}}
.checklist {{background:#fff; border:1px solid #dfe7df; border-radius:10px; padding:1.1rem 1.3rem}}
.checklist li {{margin:.6rem 0}}
footer {{text-align:center; color:#666; font-size:.85rem; padding:2rem 1rem; border-top:1px solid #dfe7df}}
.disclaimer {{background:#fff8e1; border:1px solid #f0d060; border-radius:8px; padding:.9rem 1.1rem; font-size:.9rem; margin-top:2rem}}
</style>
</head>
<body>
<header>
  <h1>💰 Hidden Payouts</h1>
  <p>Open class-action settlements you can still file for — with deadlines, who qualifies, and the official claim links.</p>
  <p>Updated hourly by an automated watch · Last check: Oct 2, 2026</p>
</header>
<main>
  <h2>Open settlements — file before the deadline</h2>
  {cards}

  <h2>🔎 Check for money in your name (free, official)</h2>
  <div class="checklist"><ul>
    <li><b>Michigan unclaimed property</b> — search your name for forgotten bank accounts, deposits, insurance payouts:
      <a href="https://unclaimedproperty.michigan.gov/" rel="noopener">unclaimedproperty.michigan.gov</a></li>
    <li><b>MissingMoney.com</b> — NAUPA's national search across participating states:
      <a href="https://www.missingmoney.com/" rel="noopener">missingmoney.com</a></li>
    <li><b>IRS unclaimed refunds</b> — if you didn't file a return, you have 3 years to claim a refund:
      <a href="https://www.irs.gov/refunds" rel="noopener">irs.gov/refunds</a></li>
    <li><b>FTC refunds</b> — the FTC sends money back after enforcement cases; see if a case names you:
      <a href="https://www.ftc.gov/enforcement/refunds" rel="noopener">ftc.gov/enforcement/refunds</a></li>
  </ul></div>

  <h2>🕵️ New leads being verified</h2>
  <p>Fresh settlement links spotted by the watch — details not yet confirmed. Always verify on the official site before filing.</p>
  <ul class="leads">{lead_list}</ul>

  <div class="disclaimer">
    <b>Please read:</b> this page is informational, not legal advice. Never pay anyone to file a claim —
    legitimate settlements are always free to file. Always confirm deadlines and eligibility on the
    <b>official</b> settlement website (linked above) before submitting anything. Filing a claim is a sworn
    statement — only file if you genuinely qualify.
  </div>
</main>
<footer>Hidden Payouts · automated hourly watch · not affiliated with any settlement administrator</footer>
</body>
</html>"""

open(OUT, 'w').write(page)
open(os.path.join(HERE, '.nojekyll'), 'w').write('')
print(f"wrote {OUT} ({len(page)} bytes), {len(verified)} verified cards, {len(leads)} leads")
