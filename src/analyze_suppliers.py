"""Generate supplier transactions and produce a weighted scorecard."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]; DATA=ROOT/"data"; OUT=ROOT/"output"
DATA.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(2410)
N_SUPPLIERS=75
suppliers=pd.DataFrame({"supplier_id":[f"SUP-{i:03d}" for i in range(1,N_SUPPLIERS+1)],
 "supplier_name":[f"Industrial Partner {i:03d}" for i in range(1,N_SUPPLIERS+1)],
 "category":rng.choice(["Electrical","Safety","MRO","Packaging","HVAC","Plumbing"],N_SUPPLIERS),
 "region":rng.choice(["East","Central","South","West"],N_SUPPLIERS),
 "contract_lead_days":rng.integers(5,31,N_SUPPLIERS)})
rows=[]
for i in range(50000):
    s=suppliers.iloc[int(rng.integers(0,len(suppliers)))]
    order=pd.Timestamp("2025-01-01")+pd.Timedelta(days=int(rng.integers(0,365)))
    promised=order+pd.Timedelta(days=int(s.contract_lead_days))
    tier=int(s.supplier_id[-3:])%5
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
monthly=po.assign(month=pd.to_datetime(po.order_date).dt.to_period("M").astype(str)).groupby("month").spend.sum()
pareto=score.sort_values("total_spend",ascending=False).copy(); pareto["cum_spend_pct"]=pareto.total_spend.cumsum()/pareto.total_spend.sum()*100
pareto[["supplier_id","supplier_name","total_spend","cum_spend_pct"]].to_csv(OUT/"spend_pareto.csv",index=False)
fig,axes=plt.subplots(2,2,figsize=(15,10))
monthly.plot(ax=axes[0,0],marker="o",color="#0b6b5b",title="Monthly Procurement Spend"); axes[0,0].set_ylabel("$")
axes[0,1].scatter(score.delivery_score,score.quality_score,s=score.total_spend/score.total_spend.max()*900+30,c=score.weighted_score,cmap="RdYlGn"); axes[0,1].set(title="Supplier Risk Matrix",xlabel="Delivery score",ylabel="Quality score")
top=pareto.head(20); axes[1,0].bar(range(len(top)),top.total_spend,color="#6c8ebf"); ax2=axes[1,0].twinx(); ax2.plot(range(len(top)),top.cum_spend_pct,color="#cf5c5c",marker="o"); axes[1,0].set_title("Supplier Spend Pareto — Top 20"); axes[1,0].set_xlabel("Suppliers ranked by spend"); ax2.set_ylabel("Cumulative spend %")
score.risk_tier.value_counts().reindex(["Preferred","Watch","High"]).plot(kind="bar",ax=axes[1,1],color=["#0b6b5b","#efb366","#cf5c5c"],title="Supplier Risk Tiers"); axes[1,1].set_xlabel("")
fig.suptitle("Supplier Performance Executive Dashboard",fontsize=18,fontweight="bold");fig.tight_layout();fig.savefig(OUT/"executive_dashboard.png",dpi=170);plt.close(fig)
print(summary.to_string(index=False))
