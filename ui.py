import matplotlib.pyplot as plt
from backend import get_store_sales_postgree, get_total_store_sales

def plot_daily_store_sales(store_ids):
    sales = get_store_sales_postgree()
    fig, ax = plt.subplots(figsize=(8, 4))

    for sid in store_ids:
        df = sales[sales["store_id"] == sid]
        ax.plot(df["rental_day"], df["revenue"], label=f"Store {sid}")

    # ax.set_title("Daily Revenue")
    ax.set_xlabel("Rental Day")
    ax.set_ylabel("Revenue")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    return fig

def plot_total_store_sales():
    sales = get_total_store_sales()
    fig, ax = plt.subplots(figsize=(8, 4))
    
    bars = ax.bar(sales["store_id"], sales["revenue"], color=['lightblue', 'orange'])
    
    #ax.set_title("Total benefit by Store")
    ax.set_xlabel("Store ID")
    ax.set_ylabel("Total Revenue")
    ax.set_xticks(sales["store_id"])
    ax.set_xticklabels([f"Store {sid}" for sid in sales["store_id"]])
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2, 
            height,
            f"{height:,.2f}", 
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )
    
    plt.tight_layout()
    return fig


    
def format_top5(df, sid):
    df_display = (
        df[df["store_id"] == sid]
        .drop(columns=["store_id"])
        .reset_index(drop=True)
    )
    df_display.index = df_display.index + 1
    df_display.index.name = "#"
    return df_display