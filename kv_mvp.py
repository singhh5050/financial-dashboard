import streamlit as st
import pdfplumber
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY') or st.secrets.get('OPENAI_API_KEY')
    if not api_key:
        st.error("Please set your OPENAI_API_KEY in .env file or Streamlit secrets")
        st.stop()
    return OpenAI(api_key=api_key)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {i+1} ---\n{page_text}\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_financial_metrics(text, client):
    """Use OpenAI to extract financial metrics from text"""
    prompt = f"""
    You are a precise financial data extractor. Analyze the following board deck text and extract financial metrics.
    
    Look for:
    - Revenue (ARR, MRR, total revenue, sales, etc.)
    - Gross Margin % (gross margin, GM%, etc.)
    - EBITDA (earnings before interest, taxes, depreciation, and amortization)
    - Burn Rate (monthly burn, cash burn, etc.)
    - Cash Balance (cash on hand, available cash, etc.)
    
    Return ONLY a valid JSON object in this exact format:
    {{
        "Revenue": [
            {{"date": "2023-Q1", "value": 1200000, "unit": "USD"}},
            {{"date": "2023-Q2", "value": 1450000, "unit": "USD"}}
        ],
        "GrossMargin": [
            {{"date": "2023-Q1", "value": 75.5, "unit": "%"}},
            {{"date": "2023-Q2", "value": 78.2, "unit": "%"}}
        ],
        "EBITDA": [
            {{"date": "2023-Q1", "value": -200000, "unit": "USD"}},
            {{"date": "2023-Q2", "value": -150000, "unit": "USD"}}
        ],
        "BurnRate": [
            {{"date": "2023-Q1", "value": 300000, "unit": "USD"}},
            {{"date": "2023-Q2", "value": 280000, "unit": "USD"}}
        ],
        "CashBalance": [
            {{"date": "2023-Q1", "value": 5000000, "unit": "USD"}},
            {{"date": "2023-Q2", "value": 4500000, "unit": "USD"}}
        ]
    }}
    
    If no data is found for a metric, return an empty array [].
    Extract dates in YYYY-Q# format when possible, or YYYY-MM format for monthly data.
    
    Text to analyze:
    {text[:15000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        st.error(f"Error extracting metrics: {str(e)}")
        return None

def create_metric_chart(data, metric_name, color):
    """Create a plotly chart for a specific metric"""
    if not data:
        return None
    
    df = pd.DataFrame(data)
    if df.empty:
        return None
    
    fig = px.line(
        df, 
        x="date", 
        y="value",
        title=f"{metric_name} Trend",
        color_discrete_sequence=[color]
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{metric_name} ({df['unit'].iloc[0] if 'unit' in df.columns else ''})",
        height=300,
        showlegend=False
    )
    
    return fig

def create_dashboard(metrics_data):
    """Create a comprehensive dashboard with multiple metrics"""
    if not metrics_data:
        return None
    
    # Filter out empty metrics
    available_metrics = {k: v for k, v in metrics_data.items() if v}
    
    if not available_metrics:
        st.warning("No financial metrics found in the uploaded document.")
        return None
    
    # Create subplots
    num_metrics = len(available_metrics)
    if num_metrics == 1:
        rows, cols = 1, 1
    elif num_metrics == 2:
        rows, cols = 1, 2
    elif num_metrics <= 4:
        rows, cols = 2, 2
    else:
        rows, cols = 3, 2
    
    fig = make_subplots(
        rows=rows, 
        cols=cols,
        subplot_titles=list(available_metrics.keys()),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (metric_name, data) in enumerate(available_metrics.items()):
        if not data:
            continue
            
        df = pd.DataFrame(data)
        row = (i // cols) + 1
        col = (i % cols) + 1
        
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['value'],
                mode='lines+markers',
                name=metric_name,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8)
            ),
            row=row, col=col
        )
    
    fig.update_layout(
        height=600,
        title_text="Financial Metrics Dashboard",
        showlegend=False
    )
    
    return fig

# Streamlit App
def main():
    st.set_page_config(
        page_title="KV Board Deck Parser",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 KV Board Deck Parser")
    st.markdown("*30-minute financial metrics extraction from board decks*")
    
    # Sidebar for API key input
    with st.sidebar:
        st.header("Configuration")
        api_key_input = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
        )
        
        if api_key_input:
            os.environ['OPENAI_API_KEY'] = api_key_input
    
    # Initialize OpenAI client
    try:
        client = get_openai_client()
    except:
        st.stop()
    
    # File uploader
    st.header("📄 Upload Board Deck")
    pdf_file = st.file_uploader(
        "Upload board deck PDF", 
        type="pdf",
        help="Upload a PDF containing financial metrics and board deck information"
    )
    
    if pdf_file is not None:
        # Extract text
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(pdf_file)
        
        if text:
            st.success(f"✅ Extracted text from PDF ({len(text):,} characters)")
            
            # Show text preview
            with st.expander("📖 Text Preview"):
                st.text_area("Extracted Text (first 2000 chars)", text[:2000], height=200)
            
            # Extract metrics
            with st.spinner("🤖 Analyzing financial metrics with AI..."):
                metrics_data = extract_financial_metrics(text, client)
            
            if metrics_data:
                st.success("✅ Financial metrics extracted successfully!")
                
                # Create dashboard
                dashboard_fig = create_dashboard(metrics_data)
                if dashboard_fig:
                    st.plotly_chart(dashboard_fig, use_container_width=True)
                
                # Individual metric charts
                col1, col2 = st.columns(2)
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                
                for i, (metric_name, data) in enumerate(metrics_data.items()):
                    if data:  # Only show metrics with data
                        with col1 if i % 2 == 0 else col2:
                            fig = create_metric_chart(data, metric_name, colors[i % len(colors)])
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                
                # Manual override section
                st.header("✏️ Manual Override")
                st.markdown("Edit the extracted data if needed:")
                
                # Convert to editable format
                for metric_name, data in metrics_data.items():
                    if data:
                        df = pd.DataFrame(data)
                        st.subheader(f"{metric_name}")
                        edited_df = st.data_editor(
                            df,
                            key=f"edit_{metric_name}",
                            num_rows="dynamic",
                            use_container_width=True
                        )
                        metrics_data[metric_name] = edited_df.to_dict('records')
                
                # Raw JSON output
                st.header("📊 Raw Data")
                with st.expander("View Raw JSON"):
                    st.json(metrics_data)
                
                # Download option
                st.download_button(
                    label="💾 Download Metrics as JSON",
                    data=json.dumps(metrics_data, indent=2),
                    file_name=f"financial_metrics_{pdf_file.name.replace('.pdf', '')}.json",
                    mime="application/json"
                )
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.markdown("""
        1. **Upload a PDF**: Click the file uploader and select a board deck PDF
        2. **AI Analysis**: The system will extract text and analyze it for financial metrics
        3. **View Results**: Charts and data tables will appear showing trends
        4. **Manual Override**: Edit any incorrect values in the data editor
        5. **Download**: Export the extracted metrics as JSON
        
        **Supported Metrics:**
        - Revenue (ARR, MRR, total revenue)
        - Gross Margin %
        - EBITDA
        - Burn Rate
        - Cash Balance
        """)

if __name__ == "__main__":
    main() 