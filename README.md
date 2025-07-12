# XLRI Schedule Helper

A Streamlit web application for managing and organizing your academic schedule with priority-based filtering and date-specific views.

## 🚀 Features

- **Add New Entries**: User-friendly form interface to add schedule entries
- **Legacy Method**: Bulk entry system for multiple entries at once
- **Priority Filtering**: Filter entries by priority levels (ABCD, B, ABC, ABCDE)
- **Date Filtering**: View today's and tomorrow's schedule entries
- **Automatic Sorting**: Entries are automatically sorted by date and time
- **Real-time Updates**: Changes reflect immediately in all tables
- **CSV Storage**: Data is stored in a CSV file for persistence

## 📋 Prerequisites

- Python 3.7+
- Streamlit
- Pandas

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bajju360/XLRI_schedule_helper.git
   cd XLRI_schedule_helper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run stream_app/todohemanth.py
   ```

## 📖 Usage

### Adding New Entries

#### Method 1: Form Interface
1. Select date from the dropdown
2. Choose time (15-minute intervals)
3. Set time required (0-300 minutes)
4. Select topic (Assignment, Gym, Other)
5. Click "Add Entry"

#### Method 2: Legacy Text Area
1. Enter entries in the format: `DD-MM-YY HH.MM AM/PM (PRIORITY);TOPIC;PROFESSOR;LECTURE_HALL`
2. Example: `15-08-25 02.45 PM (ABCD);MSTBJ24-4;Indrajit Mukherjee;LC2/L.H. 16`
3. Click "Add Entries"

### Viewing Schedule

- **Today & Tomorrow's Schedule**: Shows entries for current and next day with ABCD, B, ABC, and ABCDE priorities
- **All Values**: Displays all entries from the CSV file with the same priority filtering
- **Summary Statistics**: Shows total entries and unique topics

## 📁 File Structure

```
XLRI_schedule_helper/
├── README.md
├── requirements.txt
├── stream_app/
│   ├── todohemanth.py
│   └── schedule_hemanth.csv
└── venv/
```

## 🔧 Configuration

### Priority Levels
- **ABCD**: High priority (90 minutes required)
- **B**: Medium priority (90 minutes required)
- **ABC**: Standard priority (0 minutes required)
- **ABCDE**: Default priority for new entries (0 minutes required)

### Data Format
Entries are stored in CSV format with the structure:
```
DD-MM-YY HH.MM AM/PM (PRIORITY);TOPIC;PROFESSOR;LECTURE_HALL
```

## 🚀 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the app

### Local Network
```bash
streamlit run stream_app/todohemanth.py --server.address=0.0.0.0 --server.port=8501
```

## 🐛 Troubleshooting

### Common Issues
1. **CSV file not found**: Ensure `schedule_hemanth.csv` exists in the `stream_app/` directory
2. **Entries not appearing**: Check that entries have proper priority format (ABCD, B, ABC, ABCDE)
3. **Date format issues**: Ensure dates are in DD-MM-YY format

### Data Validation
- Dates must be in DD-MM-YY format
- Times must be in HH.MM AM/PM format
- Priorities must be one of: ABCD, B, ABC, ABCDE
- Entries are automatically sorted by date and time

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Bajju360** - [GitHub Profile](https://github.com/Bajju360)

---

**Note**: This application is designed specifically for XLRI schedule management and may require modifications for other use cases. 