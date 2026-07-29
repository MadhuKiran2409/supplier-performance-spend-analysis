"""Generate supplier transactions and produce a weighted scorecard."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; OUT=ROOT/"output"
DATA.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(2410)
suppliers=pd.DataFrame({"supplier_id":[f"SUP-{i:02d}" for i in range(1,16)],
 "supplier_name":[f"Supplier {c}" for c in "ABCDEFGHIJKLMNO"],
 "region":rng.choice(["East","Central","South","West"],15),
 "contract_lead_days":rng.integers(5,25,15)})
rows=[]
for i in range(600):
    s=suppliers.iloc[int(rng.integers(0,len(suppliers)))]
    order=pd.Timestamp("2025-01-01")+pd.Timedelta(days=int(rng.integers(0,365)))
    promised=order+pd.Timedelta(days=int(s.contract_lead_days))
    tier=int(s.supplier_id[-2:])%5
    delay=int(rng.choice([-2,-1,0,1,2,3],p=[.08,.12,.58,.12,.07,.03])) + (1 if tier==4 and rng.random()<.35 else 0)
    actual=promised+pd.Timedelta(days=delay)
    qty=int(rng.integers(10,400)); unit=float(rng.uniform(3,160))
    rows.append((f"PO-{i+1:04d}",s.supplier_id,order.date(),promised.date(),actual.date(),qty,round(unit,2),int(rng.binomial(qty,.008+tier*.003))))
po=pd.DataFrame(rows,columns=["po_id","supplier_id","order_date","promised_date","actual_date","quantity","unit_price","defect_qty"])
po["spend"]=po.quantity*po.unit_price; po["on_time"]=(pd.to_datetime(po.actual_date)<=pd.to_datetime(po.promised_date)).astype(int)
po["defect_rate"]=po.defect_qty/po.quantity
score=po.groupby("supplier_id").agg(total_spend=("spend","sum"),orders=("po_id","count"),on_time_delivery=("on_time","mean"),defect_rate=("defect_rate","mean"),avg_unit_price=("unit_price","mean")).reset_index()
score=score.merge(suppliers,on="supplier_id")
score["cost_score"]=100*(1-(score.avg_unit_price-score.avg_unit_price.min())/(score.avg_unit_price.max()-score.avg_unit_price.min()))
score["delivery_score"]=100*score.on_time_delivery; score["quality_score"]=100*(1-score.defect_rate)
score["weighted_score"]=(.35*score.cost_score+.40*score.delivery_score+.25*score.quality_score).round(1)
score["risk_tier"]=pd.cut(score.weighted_score,[0,70,82,100],labels=["High","Watch","Preferred"],include_lowest=True)
po.to_csv(DATA/"purchase_orders.csv",index=False); suppliers.to_csv(DATA/"suppliers.csv",index=False)
score.sort_values("weighted_score",ascending=False).to_csv(OUT/"supplier_scorecard.csv",index=False)
summary=pd.DataFrame({"metric":["Total spend","Suppliers assessed","Overall on-time delivery","Overall defect rate","High-risk suppliers"],"value":[f"${po.spend.sum():,.0f}",len(suppliers),f"{po.on_time.mean():.1%}",f"{po.defect_rate.mean():.2%}",int((score.risk_tier=="High").sum())]})
summary.to_csv(OUT/"executive_summary.csv",index=False)
fig,ax=plt.subplots(figsize=(10,5)); top=score.sort_values("weighted_score")
ax.barh(top.supplier_name,top.weighted_score,color=np.where(top.weighted_score>=88,"#0b6b5b","#efb366")); ax.axvline(75,color="#cf5c5c",ls="--"); ax.set(xlabel="Weighted score",title="Supplier Performance Scorecard")
fig.tight_layout();fig.savefig(OUT/"supplier_scorecard.png",dpi=160);plt.close(fig)
print(summary.to_string(index=False))
