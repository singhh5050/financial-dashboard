# 🚀 KV Board Deck Parser - MVP

A 30-minute proof-of-concept for extracting financial metrics from board deck PDFs using AI.

## 🎯 What This Does

Upload a board deck PDF → AI extracts Revenue, Gross Margin %, EBITDA, Burn Rate, and Cash Balance → Display as interactive charts → Manual override capability.

This is Part B of the KV portfolio management platform gameplan - a working demo you can run tonight!

## 🚀 Quick Start

### 1. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get OpenAI API Key
- Go to [OpenAI Platform](https://platform.openai.com/api-keys)
- Create a new API key
- Copy it for the next step

### 3. Set your API key (choose one method):

**Option A: Environment variable**
```bash
export OPENAI_API_KEY=sk-your-api-key-here
```

**Option B: .env file**
```bash
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

**Option C: Enter in the app**
- Leave the environment variable empty
- Enter your API key in the sidebar when the app starts

### 4. Run the app
```bash
streamlit run kv_mvp.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Features

### Core Functionality
- **PDF Upload**: Drag & drop board deck PDFs
- **AI Extraction**: GPT-4o-mini extracts financial metrics
- **Interactive Charts**: Plotly visualizations with trends
- **Manual Override**: Edit any incorrect values
- **JSON Export**: Download extracted data

### Supported Metrics
- **Revenue** (ARR, MRR, total revenue, sales)
- **Gross Margin %** (GM%, gross margin percentage)
- **EBITDA** (earnings before interest, taxes, depreciation, amortization)
- **Burn Rate** (monthly burn, cash burn)
- **Cash Balance** (cash on hand, available cash)

## 🏗️ Architecture

```
streamlit run kv_mvp.py
├── PDF Upload (pdfplumber)
├── Text Extraction
├── OpenAI GPT-4o-mini Analysis
├── JSON Structured Output
├── Plotly Dashboard
└── Manual Override (st.data_editor)
```

## 🎥 Demo Flow

1. **Upload PDF**: Click "Upload board deck PDF" and select a file
2. **View Extraction**: See text preview and character count
3. **AI Analysis**: Watch as GPT-4o-mini processes the financial data
4. **Interactive Dashboard**: Explore the multi-metric dashboard
5. **Individual Charts**: Detailed view of each metric trend
6. **Manual Override**: Edit any incorrect values in the data tables
7. **Export**: Download the final JSON for integration

## 🔧 Technical Details

- **Framework**: Streamlit for rapid prototyping
- **PDF Processing**: pdfplumber for reliable text extraction
- **AI Model**: OpenAI GPT-4o-mini with JSON mode
- **Visualization**: Plotly for interactive charts
- **Data**: Pandas DataFrames with editable tables

## 🚀 Next Steps (V1 Roadmap)

This MVP proves the concept. The full platform will include:

1. **Database Integration**: PostgreSQL + TimescaleDB
2. **Authentication**: Google OAuth SSO
3. **Real-time Sync**: Harmonic API integration
4. **Alert System**: Slack/email notifications
5. **Natural Language Queries**: "How much runway does Company X have?"

## 🛠️ Troubleshooting

### Common Issues

**"No OpenAI API key found"**
- Set the `OPENAI_API_KEY` environment variable
- Or enter it in the app sidebar

**"Error extracting text from PDF"**
- Try a different PDF file
- Ensure the PDF contains readable text (not just images)

**"No financial metrics found"**
- The PDF might not contain recognizable financial data
- Try a board deck with clear financial tables/charts

### Performance Notes
- Large PDFs (>50 pages) may take longer to process
- First run downloads required NLTK data
- API calls to OpenAI may take 5-15 seconds

## 💡 Usage Tips

1. **Best PDF Types**: Board decks with clear financial tables work best
2. **Date Formats**: The AI recognizes YYYY-Q# and YYYY-MM formats
3. **Manual Override**: Always review and correct the extracted data
4. **Multiple Metrics**: The dashboard shows all available metrics in one view

## 📝 Example Output

```json
{
  "Revenue": [
    {"date": "2023-Q1", "value": 1200000, "unit": "USD"},
    {"date": "2023-Q2", "value": 1450000, "unit": "USD"}
  ],
  "GrossMargin": [
    {"date": "2023-Q1", "value": 75.5, "unit": "%"},
    {"date": "2023-Q2", "value": 78.2, "unit": "%"}
  ]
}
```

## 🎯 This is Just the Beginning

This MVP demonstrates the core value proposition of the KV portfolio platform:
- **AI-powered extraction** from unstructured documents
- **Real-time visualization** of key metrics
- **Manual override** for accuracy
- **Structured data export** for integration

The full platform will scale this to handle multiple portfolio companies, real-time data sync, and natural language querying.

---

**Built for KV - Internal Portfolio Management Platform MVP** 