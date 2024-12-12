GradeBoost
------------
------------
GradeBoost is a Python project that collects data through a questionnaire and analyzes this data in order to predict grades for 15-18 year old students.
The project uses data from an already existing dataset as a reference to predict the students grade based on the input in the questionnaire. 
GradeBoost integrates Machine Learning (a Random Forest Model) to analyze responses and provide data-driven grade forecasts.

Prerequisites
------------
- Required libraries: listed in the file requirements.txt
- GitHub API-Key: required for certain functionalities

Setup Instructions
-----------
1. Clone the GradeBoost GitHub Repository:
  git clone https://github.com/levmueller/Gradeboost.git
  cd Gradeboost
2. Install the required elements:
  pip install -r requirements.txt
3. Configure a GitHub API-Key:
  Generate a personal access token for GitHub in order to be able to access all functions of our code.

Usage
------------
1. Run and fill out the questionnaire. Data from the responses will be saved for analysis.
2. Analysis and grade prediction.
  - The project uses both the collected responses and a pre-existing dataset (dataset_final.csv) to train and test the model.
  - Predictions are powered by a pre-trained Random Forest model.
3. Visualize Results.
  - Outputs, including insights on how you compare to other user's data and the predicted grade itself, are displayed through diagrams.
  - This data visualization includes a radar chart (for comparison) and pie chart (for the possibility of the predicted grade(s)).
4. Save your report by letting GradeBoost send you an email.
  - To remember the predicted grade and track progress over time, an email can be sent to your personal mail address.
  - In order for this to work, the SendGrid API is used.
  - You don't need an API key, as this is already safely stored in Streamlit Cloud.

Additional Information
------------
- The questionnaire is the primary method for collecting the user's data.
- The data set is used to train the Machine Learning model and improve the grade predictions.
- For more details about the analysis and Machine Learning model, navigate to report.py.
