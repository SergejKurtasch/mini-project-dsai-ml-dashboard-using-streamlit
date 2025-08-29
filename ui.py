import matplotlib.pyplot as plt
from backend import get_store_sales, get_store_sales_postgree

def plot_store_sales(store_ids):
    sales = get_store_sales_postgree()
    fig, ax = plt.subplots(figsize=(10, 6))

    for sid in store_ids:
        df = sales[sales["store_id"] == sid]
        ax.plot(df["rental_day"], df["revenue"], label=f"Store {sid}")

    ax.set_title("Daily Revenue")
    ax.set_xlabel("Rental Day")
    ax.set_ylabel("Revenue")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    return fig

