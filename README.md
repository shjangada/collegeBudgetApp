# collegeBudgetApp
Application for ai@uiuc -- a college budget app that tracks expenses, income, and budget while providing AI suggestions.

I created this app because after coming to college, most of my conversations with new people are about our spending and budgets. An app like this would make it easier for people to keep track of and get suggestions on how much they are spending. 

OpenAI is used in two ways: on the home page, in the form of an AI Financial Advisor. Similar to a live chat button found on other websites, this allows users to input any questions or concerns they may have and have a conversation with Chat GPT. Second, OpenAI is used in expenses.html, where users can ask for suggestions or advice using data from their recent expenses.

There are 5 pages:
1) index.html

This is the home page, where users can enter an initial budget that is transferred to budget_generator and expenses. This page also has the live chat feature and buttons to take users to the other pages.
  
2) budget_generator.html

This page creates a sample budget division for users after they input the initial budget. The enterred value is split into categories like housing, entertainment, and food. This information is also displayed graphically in the form of a pie chart.
   
3) expenses.html

This page has three key features. First, users input the date, reason, and amount of their expense, and this information is saved in the form of the expense table. Users may also use the "Clear Log" button to remove these expenses. This will reset the initial budget.

Next, the entries in the expense log are plotted as points in the graph. The x entry in the expense log is the x point on the chart. This makes it easier for users to visualize the frequency and intensity at which they are spending.

Finally, users have access to the "Get Suggestion" AI feature on this page. They can either ask questions or enter the data in their expense log to get a response from the AI.
  
4) suggestions.html

This is the page that users are redirected to in case they want suggestions based on their expenses. 

5) income.html

This page provides a space for users to enter their income and any money coming in, such as scholarships and paychecks.


The general style guidelines such as background, button colors, and fonts can be found in styles.css
