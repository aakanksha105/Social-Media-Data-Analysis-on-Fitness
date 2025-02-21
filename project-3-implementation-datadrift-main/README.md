
Social Media Analysis - Project 3 Implementation

List of files:

app.py

background.py

templates/index.html

templates/analysis.html

static/css/style.css

static/images/background_wordcloud.png

.env

Execution steps-
Step 1: Run the Python File
Login to VM 128.226.29.110 and Open a terminal in the '/4chan-crawler-username' directory where your project files are located.
Activate Python virtual environment: source env/bin/activate
Execute: python3 background.py
Run the Flask application by executing the following command: python3 app.py
The terminal will display a message indicating that the application is running:
* Running on http://127.0.0.1:5000/


![Execution](https://github.com/user-attachments/assets/f27c0be1-c64e-4cc1-8e44-589c347cc5b8)



Step 2: Open the Web Application
Open a browser and go to the URL displayed in the terminal: http://127.0.0.1:5000/

The Social Media Analysis Dashboard will appear with options to perform four analyses:

Toxicity vs Engagement
Sentiment Over Time
Toxicity Distribution
Reddit Toxicity Over Time


<img width="955" alt="image" src="https://github.com/user-attachments/assets/e9d330f6-fe31-425b-a7c1-49499e475bca" />



Step 3: Select an Analysis
Click on one of the analysis buttons to proceed.

For example, click on Toxicity vs Engagement.
You will be redirected to the analysis page with filters for input parameters.


<img width="485" alt="image" src="https://github.com/user-attachments/assets/ad229e1e-ab6d-443b-aa10-3f204d1593c8" />



Step 4: Provide Input Parameters and Generate the Analysis
Fill out the input fields for the chosen analysis:
Toxicity vs Engagement Analysis: Enter the Start Date and End Date. After providing input parameters, click the Generate Analysis button.

Output: 


<img width="458" alt="image" src="https://github.com/user-attachments/assets/46e587a2-e2da-423a-bac5-0744b1413068" />


Sentiment Over Time Analysis: Enter the Start Date and End Date.


<img width="482" alt="image" src="https://github.com/user-attachments/assets/a8973caf-ee2f-4b91-8431-a899ca52e0d2" />



Output:



<img width="455" alt="image" src="https://github.com/user-attachments/assets/0e389bea-ec73-4934-86e8-5b8fb423e0e6" />



Toxicity Distribution Analysis: Enter the Start Date and End Date.



<img width="479" alt="image" src="https://github.com/user-attachments/assets/f15e2c35-42c1-437b-b344-11fd66365e37" />



Output:


<img width="446" alt="image" src="https://github.com/user-attachments/assets/07e5e5ce-ecff-4b9c-bd11-96bb1abfcfad" />



Reddit Toxicity Over Time Analysis: Enter the Start Date, End Date, and the range for Minimum Comments and Maximum Comments.


<img width="467" alt="image" src="https://github.com/user-attachments/assets/ddc010c4-682b-4965-b210-0e68c3c3d4f7" />


Output:



<img width="447" alt="image" src="https://github.com/user-attachments/assets/55cb5c32-96e3-4e6d-a1fe-b265edfedfd9" />



After completing an analysis, you can easily return to the main dashboard. Simply close the analysis popup by clicking the ✖ button or anywhere outside the popup. Then, use the Home button on the analysis page to navigate back to the dashboard, where you can choose another analysis or review the options again.

