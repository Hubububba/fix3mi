# **Media Intelligence Dashboard with Streamlit**

This is an interactive web application built with Streamlit that allows you to upload media engagement data from a CSV file and visualize it through a series of charts and actionable insights.

## **Features**

* **Easy CSV Upload:** Upload your media data directly in the app.  
* **Automated Data Cleaning:** The app handles common data issues like missing values and inconsistent formats.  
* **Interactive Visualizations:** All charts are created with Plotly, allowing you to hover, zoom, and explore your data.  
* **Automated Insights:** Key takeaways and recommendations are generated automatically for each chart.  
* **Responsive Layout:** The dashboard is designed to look great on any screen size.

## **Prerequisites**

* Python 3.7+  
* pip for installing packages

## **How to Run the Dashboard Locally**

1. Create a Project Directory:  
   Create a new folder for your project and place the following files inside it:  
   * app.py  
   * requirements.txt  
   * sample\_data.csv (optional, for testing)  
2. Create a Virtual Environment (Recommended):  
   Open your terminal or command prompt, navigate to your project directory, and run:  
   \# Create the virtual environment  
   python \-m venv venv

   \# Activate it  
   \# On Windows:  
   venv\\Scripts\\activate  
   \# On macOS/Linux:  
   source venv/bin/activate

3. Install Dependencies:  
   With your virtual environment active, install the required libraries:  
   pip install \-r requirements.txt

4. Run the Streamlit App:  
   Now, you can start the application by running:  
   streamlit run app.py

   Your web browser should automatically open with the dashboard running.

## **CSV File Format**

To use your own data, make sure your CSV file has the following columns. The names should be on the first line of the file.

* Date: The date of the media mention (e.g., 2023-10-25).  
* Platform: The social media or news platform (e.g., Twitter, Facebook).  
* Sentiment: The sentiment of the mention (e.g., Positive, Neutral, Negative).  
* Location: The geographical location of the mention (e.g., USA, UK).  
* Engagements: The number of engagements (likes, shares, comments).  
* Media Type: The format of the content (e.g., Article, Video, Tweet).

You can use the included sample\_data.csv as a template.