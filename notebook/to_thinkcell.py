import pandas as pd

total_list = ["I dont know", "Not at all", "No", "Other", "None", "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly Agree",
              "Underperforming", "Performing on par", "Outperforming", "Prefer not to say/don't know", "<10", "Less than 10", "10-99", "100-999",
              "1,000-4,999", "5,000-9,999", "10,000-99,999", "100K-1M", ">1M", "Prefer not to say", "Trade school or apprenticeship",
              "Some high school", "High school diploma", "Bachelor's degree", "Master's degree", "Ph.D. or higher", "Less than five", "Six to 10",
              "11 to 20", "More than 20", "To a minor extent", "To some extent", "To a moderate extent", "To a great extent", "Not familiar", "Somewhat familiar", "Familiar",
              "Very familiar", "Extremely familiar", "Less than six months", "Between six months and one year", "Between one and three years",
              "Between three and five years", "More than five years", "No, not thinking about it", "No, but thinking about it", "No, but working on it",
              "Yes, partially implemented", "Yes, fully implemented", "Ad hoc (i.e., team by team, project by project", "Partial (i.e., some business units)",
              "Enterprisewide (i.e., mandatory policies)", "CEO", "C-suite", "SVP/vice president", "Director", "Manager", "Other (please specify)",
              "Board oversight", "Minor", "Significant", "Yes"]

def to_bar_chart_fixed(df: pd.DataFrame, question_list: list[str], type: str):
    # Output is a copied table that you can paste into Excel for a ThinkCell chart

    # df is the mastertable
    # question_list is the list of survey questions to compare
    # type is either "percentage" or "quantity"
    for q in question_list:
        if any((q + "_") in col for col in df.columns):
            df[q] = df[df.columns[pd.Series(df.columns).str.startswith(q)]].count(axis=1)
        else:
            pass
    if (type == "percentage") or (type == "p") or (type == "P"):
        cross_tab = pd.crosstab(df[question_list[0]], df[question_list[1]], normalize="index") * 100
    elif (type == "quantity") or (type == "q") or (type == "Q"):
        cross_tab = pd.crosstab(df[question_list[0]], df[question_list[1]])
    else:
        pass

    # reorder the columns based on the order of the list above
    cross_tab = cross_tab.reindex(columns=total_list)
    # remove all columns with just NaN (the extraneous columns from above)
    cross_tab_altered=cross_tab.dropna(axis=1,how='all')
    # add an extra row at the top to match the format of ThinkCell
    empty = pd.DataFrame([[""] * len(cross_tab.columns)], columns=cross_tab.columns)
    cross_tab = empty.append(cross_tab)
    # copy the table to your clipboard to paste into Excel
    cross_tab_altered.to_clipboard()