# Kidney Disease Prediction

A machine learning-powered web application for assessing kidney disease risk and providing clinical insights.

## Project Overview

This project implements a comprehensive kidney disease prediction system using machine learning models trained on clinical patient data. The application provides:

- **Risk Assessment**: Predicts likelihood of chronic kidney disease (CKD) based on medical parameters
- **Interactive Interface**: User-friendly Streamlit web application for clinicians and patients
- **Data Analysis**: Exploratory data analysis and model development in Jupyter Notebook
- **Clinical Insights**: Visual analytics and PDF report generation

## Project Structure

```
Kidney Disease Prediction/
├── app.py                      # Main Streamlit web application
├── code_project.ipynb         # Jupyter notebook with EDA and model development
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Features

- **Patient Data Input**: Enter medical metrics for kidney disease risk assessment
- **Real-time Predictions**: Machine learning model provides immediate risk predictions
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Report Generation**: PDF reports for patient records
- **Responsive Design**: Modern clinical theme with optimized UI/UX

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. Clone or download this project:
```bash
cd "Kidney Diesease Prediction"
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Running the Notebook

Open and run the Jupyter notebook for data analysis:
```bash
jupyter notebook code_project.ipynb
```

## Dataset

The project uses the Chronic Kidney Disease dataset from Kaggle. Key features include:

- Age, Blood Pressure, Specific Gravity
- Albumin, Sugar levels
- Red Blood Cells, Pus Cells, Bacteria count
- Blood Glucose, Blood Urea, Serum Creatinine
- Electrolytes (Sodium, Potassium)
- Haemoglobin, Packed Cell Volume
- White Blood Cell Count, Red Blood Cell Count
- Medical conditions: Hypertension, Diabetes, Coronary Artery Disease
- Appetite, Pedal Edema

## Model Development

The notebook includes:
- Data loading and exploration
- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- Feature engineering
- Model training and evaluation
- Model persistence for the web application

## Technologies Used

- **Python 3**: Core language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning models
- **Matplotlib & Seaborn**: Static visualizations
- **Plotly**: Interactive visualizations
- **ReportLab**: PDF generation
- **Jupyter**: Interactive notebook environment

## File Descriptions

### app.py
The main Streamlit application providing:
- Modern clinical UI theme
- Patient input forms
- Risk prediction interface
- Visual analytics
- PDF report generation

### code_project.ipynb
Jupyter notebook containing:
- Dataset exploration and analysis
- Data preprocessing and cleaning
- Exploratory Data Analysis (EDA)
- Model training and hyperparameter tuning
- Model evaluation and validation

## Configuration

The Streamlit app includes custom styling for:
- Clinical color scheme (slate and sky blue)
- Optimized input fields and buttons
- Professional layout with proper text hierarchy
- Responsive design for different screen sizes

## Future Enhancements

- Integration with medical databases
- Multi-model ensemble predictions
- Patient history tracking
- API endpoint for external integrations
- Mobile application version

## License

This project is for educational and research purposes.

## Support

For issues or questions, please check the notebook for detailed analysis steps and model information.

---

**Note**: This application is designed to assist in kidney disease risk assessment and should not replace professional medical diagnosis and treatment.
