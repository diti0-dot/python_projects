# Predicting Electric Vehicle Purchase Intent

## Table of Contents
- [Motivation](#motivation)
- [Data](#data)
- [Exploratory Analysis (SQL and Power BI)](#exploratory-analysis-sql-and-power-bi)
- [Preprocessing](#preprocessing)
- [Model](#model)
- [Results](#results)
- [Limitations and Ethical Considerations](#limitations-and-ethical-considerations)

## Motivation
I wanted to explore what factors are associated with a person's interest in buying an electric vehicle: income, commute distance, environmental concern, range anxiety, charging access, subsidies, and demographics.

The project started as a data analysis exercise in SQL and Power BI, looking at the data from a business perspective. I then used what that analysis showed to build a model that predicts whether someone is likely to buy an EV, as part of the Kaggle Playground Series.

## Data
The dataset comes from Kaggle Playground Series Season 6 Episode 9, *Predicting Electric Vehicle Purchases*. It has 668,665 training rows and 286,571 test rows, with no missing values.

Each row is a potential EV buyer, described by age, annual income, daily commute distance, city type, current car type, number of cars owned, charging stations near home and work, home charging availability, subsidy availability, environmental concern, range anxiety, and gender.

The target is `Will_Buy_EV` (Yes/No). The classes are imbalanced: **82.5% No and 17.5% Yes**, so accuracy alone would be misleading and I paid attention to class-level metrics.

## Exploratory Analysis (SQL and Power BI)
Before any modelling, I explored the data in SQL and built a Power BI dashboard to compare buyers and non-buyers across city type, income, commute distance, range anxiety, environmental concern, subsidy availability, and home charging.

[What Drives EV Purchase Intent?](https://github.com/diti0-dot/sql-projects/tree/main/ev_purchases#what-drives-ev-purchase-intent)

This analysis is what I used to decide which variables to focus on when building features for the model, so the dashboard comes first and the model builds on it.

## Preprocessing
- Checked shape, column types, missing values, unique values and the target distribution.
- Mapped the binary columns (`Home_Charging_Possible`, `Subsidy_Available`) to 0/1.
- One-hot encoded city type, current car type, gender, environmental concern level and range anxiety level.
- Scaled the six numerical columns with `StandardScaler`, fitted on the training split only and then applied to the validation split, to avoid data leakage.
- Added one engineered feature, `hidden_score`: a hand-weighted score combining income, environmental concern, subsidy availability and range anxiety, based on the variables that stood out in the analysis.
- I also tried squared income and commute features and an ordinal encoding of range anxiety, but neither is in the final model.

## Model
The task is binary classification (No → 0, Yes → 1). I used **logistic regression** because it is simple and interpretable.

The setup:
- 80/20 stratified train/validation split (`random_state=42`)
- One-hot encoding for categoricals, standard scaling for numericals
- `LogisticRegression` with `C=1.0` and `max_iter=5000`
- Evaluated with ROC AUC, since the competition scores predicted probabilities rather than hard labels

## Results
On the validation split:

| Metric | Value |
|---|---|
| ROC AUC | 0.9384 |
| Accuracy | 0.8946 |

Per-class results:

| Class | Precision | Recall | F1 |
|---|---|---|---|
| No (0) | 0.93 | 0.94 | 0.94 |
| Yes (1) | 0.71 | 0.66 | 0.69 |

The model separates buyers from non-buyers well, but it is noticeably weaker on the minority class: it finds about two thirds of the actual buyers, with about 71% precision. At a 20% false positive rate, the ROC curve shows it catching roughly 95% of buyers.

<img width="590" height="490" alt="image" src="https://github.com/user-attachments/assets/dc415bdb-af23-4a67-a102-ddfd48986efb" />
*ROC curve for the logistic regression model (AUC = 0.9384).*

## Limitations and Ethical Considerations
- The dataset is a prepared Kaggle Playground dataset, so no personal data was collected from real people. The predictions reflect patterns in this dataset and are not evidence that any particular person will buy an EV.
- Income, gender, age and location can introduce bias into a model like this. I did not test how sensitive the predictions are to these variables.
- `hidden_score` was weighted by hand rather than learned, so it should be read as a feature-engineering experiment, not a finding.
- I only evaluated on a single validation split, and the model has not been compared against other algorithms.
