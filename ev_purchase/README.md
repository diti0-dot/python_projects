## Predicting Electric Vehicle Purchase Intent

## Table of Contents

* [Motivation](#motivation)
* [Data Collection](#data-collection)
* [Preprocessing](#preprocessing)
* [EDA](#eda)
* [Visualizations](#visualizations)
* [Learning Task](#learning-task)
* [Learning Approach](#learning-approach)
* [Communication of Results](#communication-of-results)
* [Data Privacy and Ethical Considerations](#data-privacy-and-ethical-considerations)
* [Added Value](#added-value)

---

## Motivation

I wanted to explore what factors might be associated with a person's interest in purchasing an electric vehicle.

The project started as a data analysis exercise, where I looked at the dataset from a business perspective and tried to understand the patterns behind EV purchase intent. I then extended the analysis into a machine learning problem to see whether those patterns could also be used to predict whether someone would buy an EV.

The main things I was interested in were income, commuting distance, environmental concern, range anxiety, access to charging, subsidies, and demographic characteristics.

I am also using this project as an opportunity to document my machine learning workflow while participating in the Kaggle Playground Series. Rather than focusing only on the final competition score, I am using the process to experiment with preprocessing, feature engineering, model selection, and evaluation.

---

## Data Collection

The dataset comes from the Kaggle Playground Series Season 6 Episode 9, *Predicting Electric Vehicle Purchases*.

The dataset contains information about potential EV buyers, including:

* Age
* Annual income
* Daily commute distance
* City type
* Current car type
* Number of cars owned
* Charging stations near home and work
* Whether home charging is possible
* Whether a subsidy is available
* Environmental concern
* Range anxiety
* Gender
* EV purchase intent

The target variable is `Will_Buy_EV`, which contains `Yes` and `No`.

The dataset is already provided in tabular CSV format, so the initial data collection step mainly involved loading the training and test datasets and inspecting their structure.

---

## Preprocessing

Before building a model, I first checked the shape, columns, data types, missing values, unique values, and target distribution.

Categorical variables needed to be converted into numerical representations before they could be used by the model.

Binary variables such as:

* `Home_Charging_Possible`
* `Subsidy_Available`

were mapped to numerical values.

Other categorical variables were one-hot encoded, including city type, current car type, gender, environmental concern, and range anxiety.

For the numerical variables, I used `StandardScaler` so that variables with different ranges could be used together by the logistic regression model.

The scaler was fitted only on the training data and then applied to both the training and validation sets to avoid data leakage.

I also experimented with feature engineering, including squared income and commute variables, and tested different representations of environmental concern and range anxiety.

One additional feature I explored was a combined score based on several of the strongest variables in the dataset. This was useful for investigating how much of the prediction signal could be captured by combining the main factors.

---

## EDA

The exploratory analysis focused on understanding the distribution of the target and how different variables relate to EV purchase intent.

I looked at factors such as income, commute distance, city type, environmental concern, range anxiety, charging availability, and subsidies.

One of the main observations was that EV purchase intent is not evenly distributed across the dataset. Most observations belong to the `No` class, while a smaller proportion belong to the `Yes` class.

This made class-aware evaluation important when comparing models.

I also explored how purchase intent changes across different categories and numerical ranges. The EDA helped identify which variables were worth investigating further during the modelling stage.

The SQL and Power BI part of the project contains the main exploratory analysis and dashboard:

[What Drives EV Purchase Intent?](https://github.com/diti0-dot/sql-projects/tree/main/ev_purchases#what-drives-ev-purchase-intent)

---

## Visualizations

I used visualizations to move beyond simply looking at individual columns and instead compare patterns between potential buyers and non-buyers.

The Power BI dashboard focuses on the main factors associated with EV purchase intent and allows the data to be explored interactively.

Some of the areas explored include:

* Purchase intent by city type
* Income
* Daily commute distance
* Range anxiety
* Environmental concern
* Subsidy availability
* Home charging availability

The goal was to make the results easier to interpret from a business perspective rather than presenting the analysis as a collection of unrelated charts.

[What Drives EV Purchase Intent?](https://github.com/diti0-dot/sql-projects/tree/main/ev_purchases#what-drives-ev-purchase-intent)

---

## Learning Task

The machine learning problem is a **binary classification** task.

The model predicts whether an individual is likely to purchase an electric vehicle:

```text
No  →  0
Yes →  1
```

The target variable is:

```text
Will_Buy_EV
```

The input variables include demographic, financial, behavioural, and EV-related characteristics such as income, commute distance, environmental concern, range anxiety, charging access, subsidies, and vehicle ownership.

---

## Learning Approach

I started with logistic regression as a baseline because it provides a relatively simple and interpretable way to model binary outcomes.

I also experimented with Random Forest and different preprocessing and feature engineering approaches.

For evaluation, I looked at both accuracy and ROC AUC. ROC AUC is particularly important here because the Kaggle task evaluates the predicted probability of EV purchase rather than only the final class prediction.

The baseline logistic regression model achieved a ROC AUC of approximately:

**0.9380**

After experimenting with categorical encoding and feature engineering, the ROC AUC improved to approximately:

**0.9386**

I also tested different values of the logistic regression regularization parameter `C`. The results showed only very small changes, suggesting that tuning the parameter further was less useful than understanding the underlying features and structure of the data.

The current model uses:

* Logistic Regression
* One-hot encoding
* Standard scaling
* Feature engineering
* Stratified train/test split
* ROC AUC evaluation

I am continuing to use the project to understand which modelling decisions actually make a meaningful difference rather than tuning parameters without understanding the result.


<img width="590" height="490" alt="image" src="https://github.com/user-attachments/assets/dc415bdb-af23-4a67-a102-ddfd48986efb" />

Figure 1. ROC curve for the logistic regression model predicting EV purchase. The model achieves an AUC of 0.9384, indicating strong discriminative ability. The curve rises steeply toward the top-left corner, meaning the model captures a high proportion of true EV buyers while keeping false positives low. Notably, at a false positive rate of just 20%, the model correctly identifies roughly 95% of actual EV buyers.


---

## Communication of Results

The project combines several stages of analysis rather than treating the machine learning model as the only result.

The workflow is:

```text
Data
  ↓
Cleaning & Preprocessing
  ↓
SQL Exploration
  ↓
Python Analysis
  ↓
Power BI Visualization
  ↓
Feature Engineering
  ↓
Machine Learning
  ↓
Model Evaluation
```

The SQL and Power BI work focuses on understanding the data and communicating the main patterns.

The Python work then builds on that analysis by testing whether those patterns can be used for prediction.

I am also documenting the modelling process as I participate in the Kaggle Playground Series competition, using the competition as a way to experiment with different approaches and evaluate what works.

---

## Data Privacy and Ethical Considerations

The dataset does not require me to collect personal information from real individuals. It is provided as a prepared dataset for analysis and modelling.

Because the task involves predicting purchasing behaviour, it is still important to be careful about interpreting the results.

A model predicting EV purchase intent should not be treated as proof that a particular person will purchase an EV. The predictions represent patterns learned from the available data.

Variables such as income, gender, age, and location-related characteristics can also introduce biases into a predictive model. For that reason, model performance should be considered alongside the characteristics and limitations of the dataset.

---

## Added Value

The main value of this project is the opportunity to connect several parts of the data workflow into one project.

Instead of stopping at exploratory analysis, I am taking the data through:

**SQL → Python → Power BI → Machine Learning**

This lets me look at the same problem from different perspectives.

The analysis helps identify patterns in EV purchase intent, while the machine learning stage tests whether those patterns can be used to make predictions.

The project is also helping me understand practical machine learning decisions such as handling categorical variables, avoiding data leakage, dealing with class imbalance, selecting evaluation metrics, and deciding whether feature engineering actually improves a model.

I will continue updating the project as I experiment with different approaches and learn more from the results.
