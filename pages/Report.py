import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load
import requests
import os

#(API Reference/Configuration - Streamlit Docs)
st.set_page_config(page_title="Report", layout="wide")

#(API Reference/Text elements - Streamlit Docs)
st.title("Analysis of Results")
st.markdown("---")

#This API was selected for its free, reliable, and user-friendly access to current date and time across various time zones, including UTC.
#It provides data in a straightforward JSON format and requires no authentication.
#ChatGPT assisted in evaluating and implementing this API.
#The API is useful for displaying the current date, which helps the student track the progress of predicted grades throughout the semester.
url = "http://worldtimeapi.org/api/timezone/Etc/UTC"

#The requests library sends an HTTP-request to the URL in order to extract the actual date. If the request isn't successful, an error message is displayed.
#(supported by ChatGPT)
try:
    response = requests.get(url)
    response.raise_for_status()  #Raise an HTTPError if the request isn't successful
    data = response.json()
    today_date = data.get("datetime", "").split("T")[0]

except requests.RequestException as e:
    print(f"An error occurred while fetching the date: {e}")
except ValueError:
    print("Error decoding JSON response. Please check the API response format.")

#The session state for 'responses' is initialized.
#(API Reference/Caching and state - Streamlit Docs)
if 'responses' not in st.session_state:
    st.session_state.responses = None  #Default to None if not filled out yet.

#If statement to display report section only if responses from the questionnaire are available.
#(API Reference/Caching and state - Streamlit Docs)
if st.session_state.responses:
    try:
        #Retrieve saved responses of the following questions from session state, which were collected through the questionnaire.
        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

        #Title of the report that will be displayed. Today's date will be extracted through the aforementioned API.
        #(API Reference/Text elements/Write and magic - Streamlit Docs)
        st.subheader(f"Report of {today_date}")
        st.write("Below is a comparison of your inputs against the overall average (see Figure 1) and your predicted grade based on your inputs (see Figure 2).")
        st.write("") #Each st.write("") creates a blank line in the app.
        st.write("")
        st.markdown("<h5 style='font-size: 20px;'>Deviation From Averages</h5>", unsafe_allow_html=True) #The code displays a styled header for "Deviation From Averages" using HTML (supported by ChatGPT)

        #The code generates a table with 2 columns
        #See later in line xy and line xy, where specific elements are placed
        #(API Reference/Layouts and containters - Streamlit Docs)
        col1, col2 = st.columns(2)

        with col1:
            #Corresponding title for Figure 1 in the first column
            #(API Reference/Write and magic - Streamlit Docs)
            st.write("Figure 1: Inputs vs. overall average")

            #The code checks if responses exists in session state (from the questionnaire).
            #(API Reference/Caching and state - Streamlit Docs)
            if 'responses' not in st.session_state:
                st.session_state.responses = None  #Default to None if not filled out yet, indicating no inputs have been provided yet.

            #(API Reference/Caching and state - Streamlit Docs)
            try:
                if st.session_state.responses:
                    try:
                        #Retrieve responses from session state
                        #The code contains a sequence of instructions that only need to be controlled and stopped in the event of an error.
                        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses
                    except ValueError:
                        #The error is handled if unpacking fails (for example if the list doesn't have 12 elements)
                        #(API Reference/Status elements - Streamlit Docs)
                        st.error("Error: Incorrect number of responses or malformed data.")
                        st.stop()  #Stop execution if the responses are malformed (API Reference/Execution flow - Streamlit Docs)

                    #The individual user inputs are combined into a list for further analysis.
                    #This organized structure makes it easier to compare the user's data against averages.
                    user_values = [age, parental_degree_numeric, average_time, absences, support_numeric, tutoring_numeric, performance, sports, music, volunteering, extracurricular]

                    #Defined categories (these are based on the questions in the questionnaire).
                    categories = [
                        "Age", 
                        "Parental Education", 
                        "Weekly Study Time", 
                        "Absences", 
                        "Parental Support",
                        "Tutoring",
                        "GPA",
                        "Sports",
                        "Music",
                        "Volunteering",
                        "Extracurricular Activities"
                    ]

                    #Defined min and max values for each category.
                    #These min values are derived from the dataset and represent the lowest possible valid inputs for each category.
                    #They act as lower boundaries to ensure that user inputs fall within the correct range, based on the dataset.
                    #While users can select values between these boundaries, the min values help validate inputs and normalize data for visualization purposes.
                    min_values = {
                        "Age": 15, 
                        "Parental Education": 0, 
                        "Weekly Study Time": 0, 
                        "Absences": 0, 
                        "Parental Support": 0,
                        "Tutoring": 0,
                        "GPA": 1,
                        "Sports": 0,
                        "Music": 0,
                        "Volunteering": 0,
                        "Extracurricular Activities": 0
                    }
                    #These max values are derived from the dataset and represent the highest possible valid inputs for each category.
                    #They act as upper boundaries to ensure that user inputs fall within the correct range, based on the dataset.
                    #While users can select values between these boundaries, the max values help validate inputs and normalize data for visualization purposes.
                    max_values = {
                        "Age": 18, 
                        "Parental Education": 4, 
                        "Weekly Study Time": 25, 
                        "Absences": 30, 
                        "Parental Support": 4,
                        "Tutoring": 1,
                        "GPA": 6,
                        "Sports": 1,
                        "Music": 1,
                        "Volunteering": 1,
                        "Extracurricular Activities": 1
                    }

                    #Average values for comparison (based on our dataset).
                    #These values were derived from the dataset. All data was exported to an Excelsheet, where averages were calculated for each category.
                    #These averages serve as a baseline to compare the user's inputs against the overall trends in the dataset.
                    average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122074, 0.301421, 4, 0.303512, 0.196906, 0.157191, 0.383361]

                    #We created a function to normalize the input values from the student's questionnaire responses for comparison with the average values from the dataset. 
                    #For this, we chose to apply Min-Max normalization, which scales the values to a range between 0 and 1. This ensures that the student's inputs can be easily compared to the average values.
                    #We used ChatGPT to assist in the process of normalizing the values.
                    def normalize(value, category):
                        return (value - min_values[category]) / (max_values[category] - min_values[category])

                    #Here we applied normalization for 'Your Input' values and 'Average' values to ensure comparability across categories.
                    #This allows all categories, regardless of their original range, to be visualized uniformly in the radar chart (Supported by ChatGPT).
                    normalized_user_values = [normalize(value, category) for value, category in zip(user_values, categories)]
                    normalized_average_values = [normalize(value, category) for value, category in zip(average_values, categories)]

                    #Add the first category to the end of the list to ensure the radar chart forms a closed shape (Supported by ChatGPT).
                    categories += [categories[0]]
                    normalized_user_values += [normalized_user_values[0]] #Add the first normalized user value to the end of the list to close shape of the user's data in the radar chart.
                    normalized_average_values += [normalized_average_values[0]] #Add the first normalized average value to the end of the list to close shape of the average data in the radar chart.

                    #Create DataFrames for both user inputs and average values to safe the traces in the radar chart for later on.
                    #We used df_user = pd.DataFrame to do achieve this (Geeksforgeeks/Supported by ChatGPT)
                    df_user = pd.DataFrame({
                        'Category': categories, #Categories for the radar chart.
                        'Value': normalized_user_values, #Normalized user values.
                        'Type': ['Your Inputs'] * len(categories) #Label the data as 'Your Inputs'.
                    })

                    df_average = pd.DataFrame({
                        'Category': categories, #Categories for the radar chart.
                        'Value': normalized_average_values, #Normalized average values.
                        'Type': ['Average'] * len(categories) #Label the data as 'Average'.
                    })

                    #The code combines both DataFrames into a single DataFrame.
                    #This allows Plotly to plot both user inputs and average values on the same radar chart, distinguished by 'Type' for the color coding.
                    df_combined = pd.concat([df_average, df_user])

                    #Plot radar chart using Plotly Bib. With the help of ChatGPT, the Plotly library was discovered and the Radar Chart was coded.
                    #We have used a radar chart to visualize the user's responses compared to the dataset averages.
                    #This type of chart is chosen because it provides an intuitive and user-friendly way to display multiple factors at once.
                    #Users (especially younger audiences) can easily understand where their inputs differ from the average (which was calculated based on the dataset).
                    #Additionally, we included a table next to the radar chart to provide precise numerical details.
                    #This allows users to see the specific differences from the average in a clear and structured format.

                    #We used px.line_polar from Plotly Bib for the radar chart.
                    #(Plotly Bib/Scientific Charts/Radar Charts)
                    fig = px.line_polar(
                        df_combined, 
                        r='Value', #Here it defines the radial values, determining the distance of points from the center and the normalized values ensure comparability across categories (Supported by ChatGPT).
                        theta='Category', #This defines the angular positions for our categories, plotted around the circle (like "Age" or "GPA").
                        color='Type', #For differentiating 'Your input' and 'Average'.
                        line_close=True 
                    )

                    #fic.update_layout from Plotly Bib allowed us to customize our radar chart, making it more visually appealing and user friendly.
                    #(Plotly Bib/Scientific Charts/Radar Charts)
                    fig.update_layout(
                        polar=dict(
                            bgcolor="white",  
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1] #This ensures that radial values from 0-1 are properly scaled and displayed (Supported by ChatGPT).
                            ),
                            angularaxis=dict(
                                visible=True #To make it easier to interpret, we have visible axes to help users quickly interpret categories and their values.
                            )
                        ),
                    )

                    #We used fig.update_traces from Plotly Bib to customize the appearance of the 'Average' data series in the radar chart.
                    #Generally, it allows to set fill colors, transparency and line colors to visually distinguish 'Your Inputs' from 'Average'.
                    #Thanks to ChatGPT we found W3Schools RGBA Colors to customize our Colors for the Radar Chart.
                    #(Plotly Bib/Scientific Charts/ Radar Charts)
                    fig.update_traces(
                        fill='toself',
                        fillcolor="rgba(180, 180, 180, 0.4)", #Here we used W3Schools RGBA Colors to pick and create the colors that we wanted.
                        line_color="gray",  
                        selector=dict(name="Average") #This applies updates only to the trace named 'Average', avoiding changes to other traces (Supported by ChatGPT).
                    )
                    
                    #Here we did the same for the 'Your Inputs' data series.
                    #(Plotly Bib/Scientific Charts/Radar Charts)
                    fig.update_traces(
                        fill='toself',
                        fillcolor="rgba(225, 130, 180, 0.4)",  
                        line_color="red",  
                        selector=dict(name="Your Inputs") #This applies updates only to the trace named 'Your Inputs', avoiding changes to other traces (Supported by ChatGPT).
                    )

                    #We use st.plotly_chart to show our Radar Chart and with fig, use_container_width is True, it sets the width of the figure to match the width of the parent container.
                    #(API Reference/Chart elements/Status elements - Streamlit Docs)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please fill out the questionnaire first.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

        with col2:

            #The code inserts the average values from the dataset in a list, that were previously calculated in the Excelsheet.
            average_values = [
                16.46864548,  # Age
                1.746237458,  # Parental Education
                9.771991919,  # Weekly Study Time
                14.54138796,  # Absences
                2.122074,     # Parental Support
                0.301421,     # Tutoring
                4,            # GPA
                0.303512,     # Sports
                0.196906,     # Music
                0.157191,     # Volunteering
                0.383361      # Extracurricular Activities
            ]

            #This list contains the categories corresponding to the average values.
            #These categories are the labels for the rows in the output table.
            categories = [
                "Age", 
                "Parental Education", 
                "Weekly Study Time", 
                "Absences", 
                "Parental Support",
                "Tutoring",
                "GPA",
                "Sports",
                "Music",
                "Volunteering",
                "Extracurricular Activities"
            ]

            #This list collects the user’s inputs for the same categories defined in average_values and categories.
            #The input values are obtained from the questionnaire. 
            user_input_values = [
                age,  #Age
                parental_degree_numeric,  #Parental Education
                average_time,  #Weekly Study Time
                absences,  #Absences
                support_numeric,  #Parental Support
                tutoring_numeric,  #Tutoring
                performance,  #GPA
                sports,  #Sports
                music,  #Music
                volunteering,  #Volunteering
                extracurricular  #Extracurricular Activities
            ]

            #This code calculates the difference between each user input and the corresponding average value.
            #It uses a list comprehension to iterate over the indices of the lists and subtract the average from the user input.
            #ChatGPT helped us in putting this calculation together.
            differences = [user_input_values[i] - average_values[i] for i in range(len(user_input_values))]

            #A Pandas DataFrame is created to store the feature names (categories) and their differences from the average.
            #This DataFrame displays the values as a table.
            df_differences = pd.DataFrame({
                "Feature": categories,
                "Difference from Average": differences
            })

            #This code snippet initializes the session state variable 'show_table', which keeps track of whether the table should be displayed or hidden.
            #(API Reference/Caching and state - Streamlit Docs)
            if 'show_table' not in st.session_state:
                st.session_state['show_table'] = False

            #This code determines whether the table is shown or hidden with the help of the button.
            #If show_table is True, the DataFrame is displayed as a table in Streamlit, with "Feature" set as the row index.
            #If show_table is False, a message is displayed prompting the user to click the button.
            #(API Reference/Input widgets/Status elements/Caching and state/Table elements - Streamlit Docs)
            if st.button("Table 1: Differences between inputs and average values"):
                st.session_state['show_table'] = not st.session_state['show_table']

            if st.session_state['show_table']:
                st.table(df_differences.set_index('Feature'))
            else:
                st.info("Click the button to display the table.")

        #This code snippet adds a custom formatted heading titled Grade Prediction.
        #(API Reference/Text elements - Streamlit Docs)
        #(Supported by ChatGPT)
        st.markdown("<h5 style='font-size: 20px;'>Grade Prediction</h5>", unsafe_allow_html=True)

        #Here, we again create two colums that will be displayed side by side.
        #The columns represent the data that is subsequently used to create a pie chart.
        #(API Reference/Layouts and containers - Streamlit Docs)
        col3, col4 = st.columns(2)

        #We start working in the left column (col3)
        with col3:
            #The title of the chart is added for increased overview.
            #(API Reference/Write and magic - Streamlit Docs)
            st.write("Figure 2: Predicted probabilities of grades")

            #This if-statement is added to check if the user has completed the questionnaire and the responses are saved in session state.
            #(API Reference/Caching and state - Streamlit Docs)
            if st.session_state.responses:
                try:
                    #Here, we try to retrieve responses from session state.
                    #Each variable correspondends to a specific question in the questionnaire.
                    age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

                    #We define a function in order to convert swiss grades to US grades (4-scale-GPA) to comply with our GitHub-API.
                    #The formula was created with the help of ChatGPT.
                    def swiss_to_us_gpa(swiss_grade):
                        return 2 + ((swiss_grade - 1) / 5) * 2

                    swiss_grade = performance  #Takes the user's Swiss grade (performance) as input.
                    us_gpa = swiss_to_us_gpa(swiss_grade) #Here, the conversion ultimately takes place. The code calls the swiss_to_us_gpa function to convert the grade into the US GPA format.
                    #The resulting us_gpa is used in further calculations or visualizations, likely involving predictions or comparisons (Supported by ChatGPT).

                    #In this ML part we relied heavely on the help of ChatGPT.
                    #If needed we adjusted code snippets on error statements as an example.
                    scaler = load('scaler.pkl')  #In the beggining, the code loads the correct scaler saved during training phase of the ML Model. 
                    #This is crucial to scale new input data consistently with the training data.

                    #This code snippet Combines the user-provided inputs into a 2D array (new_data) suitable for predictions
                    #The model expects 12 features, so we ensure all features are included
                    new_data = np.array([
                        [age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, us_gpa]
                    ])

                    #The scaling to new data is applied (using the previously fitted scaler)
                    new_data_scaled = scaler.transform(new_data)  # Use transform to scale new data without fitting again

                    #This part of the code defines a function to combine smaller pieces (chunks) of a file into a complete file.
                    #output_file: The name of the final file created after combining all the chunks.
                    #chunk_files: A list of the smaller file parts that need to be merged.
                    #'wb' = write binary (used for saving binary data), 'rb' = read binary (used for reading binary data).
                    def reassemble_file(output_file, chunk_files):
                        with open(output_file, 'wb') as output:
                            for chunk_file in chunk_files:
                                with open(chunk_file, 'rb') as file:
                                    output.write(file.read())

                    #This is the list of model file chunks used to reassemble the model file.
                    chunk_files = [
                        'random_forest_model.pkl.part0',
                        'random_forest_model.pkl.part1',
                    ]
                    
                    #Here, the reassembly takes place to create the full model file.
                    reassemble_file('random_forest_model.pkl', chunk_files)

                    #Our pre-trained random forest model is loaded.
                    model = load('random_forest_model.pkl')  #The correct random forest model has to be loaded here.

                    #The random forest model is used to predict grades based on the scaled input data.
                    #The latter code get probabilities for each possible grade to see how confident the model is.
                    #It gives confidence levels (e.g., [80%, 15%, 5%])
                    predictions = model.predict(new_data_scaled)
                    probabilities = model.predict_proba(new_data_scaled)

                    #This dictionary was created to map the grades to new values: 0 -> 6, 1 -> 5, 2 -> 4, 3 -> 3, 4 -> 2
                    #Grades are mapped for better readability and more user-friendliness
                    grade_mapping = {0: "5.5-6", 1: "4.5-5", 2: 4, 3: "3-4", 4: "1-3"}

                    #To increase contrast and ultimately user-friendliness, custom colors for the pie chart were defined in the list below.
                    color_palette = ['#a3f0a3', '#c9f7c9', '#f4e1a1', '#f8b4b4', '#ff7373']  #The color palette ranges from light green to pastel red.

                    #The predictions and probabilities from before are used to create the pie chart.
                    #Ultimately, we used plotly again to create our pie chart.
                    import plotly.graph_objects as go

                    #This loop iterates over the predictions and probabilities lists simultaneously.
                    for i, (prediction, prob) in enumerate(zip(predictions, probabilities)):
                        
                        #A list comprehension is used to create a list mapped_labels that holds the grade labels.
                        #For each prob (which is a list of probabilities), it maps each index j to a grade using the grade_mapping dictionary.
                        #This results in labels like ['Grade: 5.5-6', 'Grade: 4.5-5', 'Grade: 4', ...].
                        mapped_labels = [f'Grade: {grade_mapping[j]}' for j in range(len(prob))]

                        #Here, the code finds the grade with the highest probability according to the data gathered in the questionnaire.
                        max_prob_index = prob.argmax()  #Index of the highest probability found in the prob list.
                        max_prob = prob[max_prob_index]  #max_prob is the highest probability value.
                        predicted_grade = grade_mapping[max_prob_index] #predicted_grade is the grade corresponding to that highest probability.

                        #Now, we display the message with the highest probability grade
                        #Subsequently, the pie chart is created with the predicted probabilities per grade
                        fig = go.Figure(data=[go.Pie(
                            labels=mapped_labels,
                            values=prob,
                            textinfo='label+percent',
                            marker=dict(colors=color_palette),
                            hoverinfo='label+percent'
                        )])

                        #fig.update_layout() is used to fine-tune the appearance of the pie chart (fig).
                        #Hides the legend in the chart, since the chart labels (grade ranges) will already be displayed on the pie slices.
                        fig.update_layout(
                            showlegend=False,
                            height=380,  #Adjust the height of the chart
                            width=380,   #Adjust the width of the chart
                            margin=dict(t=20, b=20, l=20, r=20)  #Set margins around the chart for a cleaner look
                        )

                        #st.plotly_chart(fig, use_container_width=True) displays the created pie chart (fig) in the Streamlit app.
                        #(API Reference/Chart elements - Streamlit Docs)
                        st.plotly_chart(fig, use_container_width=True)

                #This block of code is inside an exception handling structure (the try-except block).
                #If any error occurs during the loading of the model or making predictions, it catches the error and displays an error message using st.error().
                #If the user tries to make a prediction before completing the questionnaire, the else block is triggered and a warning message is displayed.
                #(API Reference/Status elements - Streamlit Docs)
                except Exception as e:
                    st.error(f"Error loading model or making predictions: {e}")
            else:
                st.warning("Please complete the questionnaire first!")

        #This code works on the column, which is displayed bottom right of the webpage.
        with col4: 
            #This dictionary contains the features (input variables) used in the model and their corresponding importance (shown in percentages).
            #The percentages show how much each feature contributes to the model's predictions.
            #For example, the 'GPA' feature contributes 46.36%, which means it's the most important factor for the predictions.
            
            data = {
                'Feature': ['Age', 'Gender', 'ParentalEducation', 'StudyTimeWeekly', 'Absences', 
                            'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 
                            'Volunteering', 'GPA'],
                'Importance (%)': [4.71, 2.35, 4.61, 6.88, 19.69, 2.68, 6.28, 2.03, 2.01, 1.37, 1.02, 46.36]
            }

            # The data is converted into a DataFrame
            # If the button is clicked, session state is initialized
            if 'show_table1' not in st.session_state:
                st.session_state['show_table1'] = False

            # This button allows the user to toggle the visibility of the "Feature Importance" table.
            # If 'show_table1' is True, the table is shown; if False, the table is hidden.
            # This provides an interactive way for the user to view or hide the table as needed.
            #(API Reference/Input widgets/Caching and state - Streamlit Docs)
            if st.button("Table 2: Feature Importance"):
                st.session_state['show_table1'] = not st.session_state['show_table1']

            if st.session_state['show_table1']:
                # The data is converted into a data frame and also sorted by importance (%) in descending order
                df = pd.DataFrame(data)
                df_sorted = df.sort_values(by='Importance (%)', ascending=False)

                # Here, the DataFrame is formatted to display one decimal point for easier readability
                df_formatted = df_sorted.set_index('Feature').style.format("{:.1f}", subset=['Importance (%)'])

                # Ultimately, the formatted table is displayed in Streamlit
                #(API Reference/Data elements - Streamlit Docs)
                st.table(df_formatted)

            else:
                # The user is informed that he can click the button to display the full table
                # The table is not displayed by default for aesthetic reasons
                #(API Reference/Status elements - Streamlit Docs)
                st.info("Click the button to display the table.")

        #Now, we display the final prediction and explain how the prediction is calculated
        #This is tho show the user that the grade prediction is not random, but based on his data
        #(API Reference/Write and magic - Streamlit Docs)
        st.write(f"Based on the provided inputs, the model predicts a {max_prob:.1%} likelihood that your grade will be {predicted_grade}. This prediction is derived from an extensive analysis of historical performance data. Each feature contributes differently to predicting your grade. Focus on improving the most impactful ones for better results. Our tests show that the model achieves an accuracy of 91.02%, indicating a strong ability to predict outcomes reliably.")


    #If something goes wrong, the user is provided with an error message
    except ValueError:
        #Handle error if unpacking fails (for example, the list doesn't have 12 elements)
        #(API Reference/Status elements - Streamlit Docs)
        st.error("Error: Incorrect number of responses or malformed data.")

#If the questionnaire has not been completed correctly, the user is informed that all questions must be answered in order to get a report.
#(API Reference/Status elements - Streamlit Docs)
else:
    st.warning("Please complete the questionnaire to view your report.")


#(API Reference/Text elements - Streamlit Docs)
st.markdown("---")

#(API Reference/Text elements - Streamlit Docs)
st.subheader("Save Report")
#Display the email input field where the user can write his preferred email-adress.
#We want to send a email with the user's predicted grade so that they can track the progress of the predicted grades over the semester.
#The API being used here is from SendGrid, which is a service for sending emails.
#The URL of the API is not written directly in the code.
#Instead, the SendGrid Python library (SendGridAPIClient) takes care of this.
#The library sends the request to the SendGrid URL "https://api.sendgrid.com/v3/mail/send" in the background.
#We only need to provide the API key and the email details, and the library handles the rest.
#ChatGPT assisted us in the implementation of this API, mainly in error solving.
#(API Reference/Input widgets - Streamlit Docs)
email = st.text_input("Please enter your email address to save your report.")

#(API Reference/Write and magic - Streamlit Docs)
st.write(os.getenv("MAIL_API"))
#The 'Submit' button is displayed.
#As soon as the user wants to receive the mail with the predicted grade, they can press the 'Submit' button.
#This triggers the delivery of the email through the SendGrid API.
#(API Reference/Input widgets - Streamlit Docs)
if st.button("Submit"):
    if email:

        #Here, we import the SendGridAPIClient class from the SendGrid python library (Supported by ChatGPT)
        #This is needed for the subsequent dispatch of the email via SendGrid API.
        #Additionally, the Mail class from the helper modules of SendGrid is imported.
        #The Mail class is used to create an email message.
        #It can be used to define the sender, recipient, subject, and content of the email that is sent.
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        #The SendGrid API-Key is retrieved from an environment variable (Supported by ChatGPT)
        #Environment variables are stored in the operating system.
        #This way, the API key is not written directly in the code.
        #This was necessary because SendGrid would delete the API-Key if it was exposed publicly.
        #The API-Key will be stored in the streamlit cloud and will be retrieved from there in order to successfully send the email.
        SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  
        
        #Here, a new function in order to send the email is defined (Supported by ChatGPT)
        #It contains information about the sending email address, the receiver, subject and content of the email.
        def send_email(user_email, note):
            message = Mail(
                from_email='gradeboostapp@gmail.com',  #The mail is sent from our own GradeBoost email-address.
                to_emails=email,
                subject='Your projected grade',
                html_content=f'''<strong>Your projected grade is: {note}</strong>
                            <br><br>
                            Thank you for using GradeBoost🚀!'''
            )
            try:
                #The API-Key is used to create an instance of the SendGrid API.
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                
                #The send method is called to send the email with all the information stored in the variable message.
                response = sg.send(message)

                #If the email is sent succesfully, the following message is displayed.
                #If the email can't be sent, an error message is displayed.
                #(API Reference/Write and magic - Streamlit Docs)
                st.write(f"email sent successfully! Status Code: {response.status_code}")
            except Exception as e:
                st.write(f"Error when sending the email: {e}")
        
        #The email function is called and triggers the dispatch of the email (Supported by ChatGPT)
        #(API Reference/Write and magic - Streamlit Docs)
        send_email(email, predicted_grade)
        
    else:
        st.write("Please enter an email address.")
