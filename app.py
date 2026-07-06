import streamlit as st
import pandas as pd

from scrapers.bigbasket_scraper import BigBasketScraper
from utils.csv_writer import save_prices


st.set_page_config(
    page_title="Grocery Price Intelligence",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Grocery Price Intelligence")
st.write("Search live product prices from BigBasket")

# Search box
product = st.text_input(
    "Enter Product Name",
    value="Tomato"
)

# Search button
if st.button("Search"):

    with st.spinner("Fetching prices from BigBasket..."):

        scraper = BigBasketScraper()

        products = scraper.fetch_prices(product)

    if not products:
        st.error("No products found.")
        st.stop()

    df = pd.DataFrame(products)

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Products", len(df))
    col2.metric("Lowest Price", f"₹{df['price'].min()}")
    col3.metric("Highest Price", f"₹{df['price'].max()}")

    st.divider()

    st.subheader("Products")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "image": st.column_config.ImageColumn(
                "Image"
            ),
            "url": st.column_config.LinkColumn(
                "Product Link"
            ),
            "price": st.column_config.NumberColumn(
                "Price",
                format="₹%.2f"
            ),
            "mrp": st.column_config.NumberColumn(
                "MRP",
                format="₹%.2f"
            ),
        },
    )

    st.divider()

    st.subheader("Price Comparison")

    chart_df = (
        df.sort_values("price")
          .set_index("name")
    )

    st.bar_chart(chart_df["price"])

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=f"{product.lower()}_prices.csv",
        mime="text/csv",
    )