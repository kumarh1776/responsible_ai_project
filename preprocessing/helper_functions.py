import pandas as pd
import numpy as np


# Add in Screener Column if meet criteria to include in analysis
def create_screener(df: pd.DataFrame) -> pd.DataFrame:
    # Add in Screener Column if meet criteria to include in analysis
    # Don't Include those who haven't finished
    df['screener'] = np.where(( \
                (df['Finished'] == False) \
                | ((df['Demo4_99'] == 'No experience with AI') |(df['Demo4_1'].isnull() & df['Demo4_2'].isnull() & df['Demo4_3'].isnull() & df['Demo4_4'].isnull() & df['Demo4_5'].isnull() & df['Demo4_99'].isnull())) \
                # based on Demo 8 response --> company needs to be > $100M or a nonprofit
                | ((df['Demo8'].isnull()) | (df['Demo8'] == 'Less than $100M') | (
                    df['Demo8'].str.contains("Prefer not to say"))) \
                # based on interest in RAI program
                | ((df['Q2'] == 'Not at all') | (df['Q2'].isnull()) | (df['Q7'].isnull()) | (
                    df['Q7'] == "No, not thinking about it")) \
                # based on whether they have an AI tool at their company
                | ((df['Q1_1'].isnull() & (df['Q1_2'].isnull())) == True)), "No", "Yes")
    return df

def create_screener_without_demo4(df: pd.DataFrame) -> pd.DataFrame:
    # Add in Screener Column if meet criteria to include in analysis
    # Don't Include those who haven't finished
    df['screener_without_demo4'] = np.where(( \
                (df['Finished'] == False) \
                # based on Demo 8 response --> company needs to be > $100M or a nonprofit
                | ((df['Demo8'].isnull()) | (df['Demo8'] == 'Less than $100M') | (
                    df['Demo8'].str.contains("Prefer not to say"))) \
                # based on interest in RAI program
                | ((df['Q2'] == 'Not at all') | (df['Q2'].isnull()) | (df['Q7'].isnull()) | (
                    df['Q7'] == "No, not thinking about it")) \
                # based on whether they have an AI tool at their company
                | ((df['Q1_1'].isnull() & (df['Q1_2'].isnull())) == True)), "No", "Yes")
    return df

def multiselect_encoding(df_mit: pd.DataFrame) -> pd.DataFrame:
    # One Hot Encoding Multiselect Columns
    df_mit["Demo4_1"] = np.where(
        df_mit["Demo 4"].str.contains("algorithms", case=False, na=False),
        "Experience developing AI algorithms & techniques",
        "",
    )
    df_mit["Demo4_2"] = np.where(
        df_mit["Demo 4"].str.contains("production", case=False, na=False),
        "Experience deploying AI solutions in production",
        "",
    )
    df_mit["Demo4_3"] = np.where(
        df_mit["Demo 4"].str.contains("users interact", case=False, na=False),
        "Experience managing AI development/how end users interact with AI",
        "",
    )
    df_mit["Demo4_4"] = np.where(
        df_mit["Demo 4"].str.contains("end user of AI", case=False, na=False),
        "Experience as an end user of AI",
        "",
    )
    df_mit["Demo4_5"] = np.where(
        df_mit["Demo 4"].str.contains("assessing third", case=False, na=False),
        "Experience assessing third-party solutions",
        "",
    )
    df_mit["Demo4_99"] = np.where(
        df_mit["Demo 4"].str.contains("no experience", case=False, na=False),
        "No experience with AI",
        "",
    )

    df_mit["Demo7_1"] = np.where(
        df_mit["Demo 7"].str.contains("North America", case=False, na=False),
        "North America",
        "",
    )
    df_mit["Demo7_2"] = np.where(
        df_mit["Demo 7"].str.contains("South America", case=False, na=False),
        "South America",
        "",
    )
    df_mit["Demo7_3"] = np.where(
        df_mit["Demo 7"].str.contains("Eastern Europe", case=False, na=False),
        "Eastern Europe",
        "",
    )
    df_mit["Demo7_4"] = np.where(
        df_mit["Demo 7"].str.contains("Western Europe", case=False, na=False),
        "Western Europe",
        "",
    )
    df_mit["Demo7_5"] = np.where(
        df_mit["Demo 7"].str.contains("Middle East", case=False, na=False),
        "Middle East",
        "",
    )
    df_mit["Demo7_6"] = np.where(
        df_mit["Demo 7"].str.contains("Africa", case=False, na=False), "Africa", ""
    )
    df_mit["Demo7_7"] = np.where(
        df_mit["Demo 7"].str.contains("East Asia", case=False, na=False),
        "East Asia",
        "",
    )
    df_mit["Demo7_8"] = np.where(
        df_mit["Demo 7"].str.contains("Oceania", case=False, na=False), "Oceania", ""
    )
    df_mit["Demo7_9"] = np.where(
        df_mit["Demo 7"].str.contains("South Asia", case=False, na=False),
        "South Asia",
        "",
    )
    df_mit["Demo7_10"] = np.where(
        df_mit["Demo 7"].str.contains("Southeast Asia", case=False, na=False),
        "Southeast Asia",
        "",
    )
    df_mit["Demo7_11"] = np.where(
        df_mit["Demo 7"].str.contains("Northeast Asia", case=False, na=False),
        "Northeast Asia",
        "",
    )

    df_mit["Demo13_1"] = np.where(
        df_mit["Demo 13"].str.contains(
            "MIT Sloan Management Review", case=False, na=False
        ),
        "MIT Sloan Management Review",
        "",
    )
    df_mit["Demo13_2"] = np.where(
        df_mit["Demo 13"].str.contains("Harvard Business Review", case=False, na=False),
        "Harvard Business Review",
        "",
    )
    df_mit["Demo13_3"] = np.where(
        df_mit["Demo 13"].str.contains("The Economist", case=False, na=False),
        "The Economist",
        "",
    )
    df_mit["Demo13_4"] = np.where(
        df_mit["Demo 13"].str.contains("Time", case=False, na=False), "Time", ""
    )
    df_mit["Demo13_5"] = np.where(
        df_mit["Demo 13"].str.contains("Wired", case=False, na=False), "Wired", ""
    )
    df_mit["Demo13_6"] = np.where(
        df_mit["Demo 13"].str.contains("The Atlantic", case=False, na=False),
        "The Atlantic",
        "",
    )
    df_mit["Demo13_7"] = np.where(
        df_mit["Demo 13"].str.contains("MIT Technology Review", case=False, na=False),
        "MIT Technology Review",
        "",
    )
    df_mit["Demo13_8"] = np.where(
        df_mit["Demo 13"].str.contains("VentureBeat", case=False, na=False),
        "VentureBeat",
        "",
    )
    df_mit["Demo13_9"] = np.where(
        df_mit["Demo 13"].str.contains("The Wall Street Journal", case=False, na=False),
        "The Wall Street Journal",
        "",
    )
    df_mit["Demo13_10"] = np.where(
        df_mit["Demo 13"].str.contains("Financial Times", case=False, na=False),
        "Financial Times",
        "",
    )

    df_mit["Q1_1"] = np.where(
        df_mit["Q1"].str.contains("build", case=False, na=False),
        "Builds Own AI Tools",
        "",
    )
    df_mit["Q1_2"] = np.where(
        df_mit["Q1"].str.contains("buy", case=False, na=False),
        "Buys/Licenses/Accesses AI Tools",
        "",
    )
    df_mit["Q1_3"] = np.where(
        df_mit["Q1"].str.contains("No", case=False, na=False), "No", ""
    )
    df_mit["Q1_4"] = np.where(
        df_mit["Q1"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q1a_1"] = np.where(
        df_mit["Q1a"].str.contains("internal", case=False, na=False), "Internal Use", ""
    )
    df_mit["Q1a_2"] = np.where(
        df_mit["Q1a"].str.contains("customer", case=False, na=False), "Customer Use", ""
    )
    df_mit["Q1a_99"] = np.where(
        df_mit["Q1a"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q1b_1"] = np.where(
        df_mit["Q1b"].str.contains("internal", case=False, na=False), "Internal Use", ""
    )
    df_mit["Q1b_2"] = np.where(
        df_mit["Q1b"].str.contains("engaging", case=False, na=False),
        "Engaging Customers (Personalized Discount Coupons, Recommendations)",
        "",
    )
    df_mit["Q1b_3"] = np.where(
        df_mit["Q1b"].str.contains("customer use", case=False, na=False),
        "Customer Use",
        "",
    )
    df_mit["Q1b_99"] = np.where(
        df_mit["Q1b"].str.contains("know", case=False, na=False), "I don't know", ""
    )

    df_mit["Q1c_1"] = np.where(
        df_mit["Q1c"].str.contains("externally developed", case=False, na=False),
        "Pre-trained, external AI models",
        "",
    )
    df_mit["Q1c_2"] = np.where(
        df_mit["Q1c"].str.contains("software tools", case=False, na=False),
        "Software with embedded AI",
        "",
    )
    df_mit["Q1c_3"] = np.where(
        df_mit["Q1c"].str.contains("Custom AI", case=False, na=False),
        "Custom AI tools from vendors",
        "",
    )
    df_mit["Q1c_4"] = np.where(
        df_mit["Q1c"].str.contains("Hardware", case=False, na=False),
        "Hardware with embedded AI",
        "",
    )
    df_mit["Q1c_99"] = np.where(
        df_mit["Q1c"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q3_1_1"] = np.where(
        df_mit["Q3_1"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_1_2"] = np.where(
        df_mit["Q3_1"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_2_1"] = np.where(
        df_mit["Q3_2"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_2_2"] = np.where(
        df_mit["Q3_2"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_3_1"] = np.where(
        df_mit["Q3_3"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_3_2"] = np.where(
        df_mit["Q3_3"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_4_1"] = np.where(
        df_mit["Q3_4"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_4_2"] = np.where(
        df_mit["Q3_4"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_5_1"] = np.where(
        df_mit["Q3_5"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_5_2"] = np.where(
        df_mit["Q3_5"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_6_1"] = np.where(
        df_mit["Q3_6"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_6_2"] = np.where(
        df_mit["Q3_6"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_7_1"] = np.where(
        df_mit["Q3_7"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_7_2"] = np.where(
        df_mit["Q3_7"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_8_1"] = np.where(
        df_mit["Q3_8"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_8_2"] = np.where(
        df_mit["Q3_8"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_9_1"] = np.where(
        df_mit["Q3_9"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_9_2"] = np.where(
        df_mit["Q3_9"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_10_1"] = np.where(
        df_mit["Q3_10"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_10_2"] = np.where(
        df_mit["Q3_10"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_11_1"] = np.where(
        df_mit["Q3_11"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_11_2"] = np.where(
        df_mit["Q3_11"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_12_1"] = np.where(
        df_mit["Q3_12"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_12_2"] = np.where(
        df_mit["Q3_12"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_13_1"] = np.where(
        df_mit["Q3_13"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_13_2"] = np.where(
        df_mit["Q3_13"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )
    df_mit["Q3_14_1"] = np.where(
        df_mit["Q3_14"].str.contains("builds", case=False, na=False),
        "AI tools it builds",
        "",
    )
    df_mit["Q3_14_2"] = np.where(
        df_mit["Q3_14"].str.contains("buys", case=False, na=False),
        "AI tools it buys",
        "",
    )

    df_mit["Q3a_1"] = np.where(
        df_mit["Q3a"].str.contains("Internal data", case=False, na=False),
        "Internal data",
        "",
    )
    df_mit["Q3a_2"] = np.where(
        df_mit["Q3a"].str.contains("Customer data", case=False, na=False),
        "Customer data",
        "",
    )
    df_mit["Q3a_3"] = np.where(
        df_mit["Q3a"].str.contains("Third-party data purchased", case=False, na=False),
        "Third-party data purchased",
        "",
    )
    df_mit["Q3a_4"] = np.where(
        df_mit["Q3a"].str.contains(
            "Third-party data otherwise acquired", case=False, na=False
        ),
        "Third-party data otherwise acquired",
        "",
    )
    df_mit["Q3a_5"] = np.where(
        df_mit["Q3a"].str.contains("Pre-trained models", case=False, na=False),
        "Pre-trained models",
        "",
    )
    df_mit["Q3a_6"] = np.where(
        df_mit["Q3a"].str.contains("In-house models", case=False, na=False),
        "In-house models",
        "",
    )
    df_mit["Q3a_7"] = np.where(
        df_mit["Q3a"].str.contains("External benchmarks", case=False, na=False),
        "External benchmarks",
        "",
    )
    df_mit["Q3a_8"] = np.where(
        df_mit["Q3a"].str.contains("External libraries", case=False, na=False),
        "External libraries",
        "",
    )
    df_mit["Q3a_9"] = np.where(
        df_mit["Q3a"].str.contains("Other", case=False, na=False), "Other", ""
    )
    df_mit["Q3a_99"] = np.where(
        df_mit["Q3a"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q4_1_1"] = np.where(
        df_mit["Q4_1"].str.contains("automate", case=False, na=False),
        "To automate internal processes",
        "",
    )
    df_mit["Q4_1_2"] = np.where(
        df_mit["Q4_1"].str.contains("augment internal", case=False, na=False),
        "To augment internal processes",
        "",
    )
    df_mit["Q4_1_3"] = np.where(
        df_mit["Q4_1"].str.contains("augment worker", case=False, na=False),
        "To augment worker performance",
        "",
    )

    df_mit["Q4_2_1"] = np.where(
        df_mit["Q4_2"].str.contains("automate", case=False, na=False),
        "To automate internal processes",
        "",
    )
    df_mit["Q4_2_2"] = np.where(
        df_mit["Q4_2"].str.contains("augment internal", case=False, na=False),
        "To augment internal processes",
        "",
    )
    df_mit["Q4_2_3"] = np.where(
        df_mit["Q4_2"].str.contains("augment worker", case=False, na=False),
        "To augment worker performance",
        "",
    )

    df_mit["Q13a_1"] = np.where(
        df_mit["Q13a"].str.contains("Evaluation of vendor", case=False, na=False),
        "Evaluation of vendor RAI practices as part of selection criteria",
        "",
    )
    df_mit["Q13a_2"] = np.where(
        df_mit["Q13a"].str.contains("Contractual language", case=False, na=False),
        "Contractual language mandating adherence to RAI principles",
        "",
    )
    df_mit["Q13a_3"] = np.where(
        df_mit["Q13a"].str.contains("Vendor pre-certification", case=False, na=False),
        "Vendor pre-certification",
        "",
    )
    df_mit["Q13a_4"] = np.where(
        df_mit["Q13a"].str.contains("Vendor audits", case=False, na=False),
        "Vendor audits of its own tools",
        "",
    )
    df_mit["Q13a_5"] = np.where(
        df_mit["Q13a"].str.contains("Internally conducted", case=False, na=False),
        "Internally conducted product-level reviews or audits",
        "",
    )
    df_mit["Q13a_6"] = np.where(
        df_mit["Q13a"].str.contains(
            "Adherence to regulatory requirements", case=False, na=False
        ),
        "Adherence to regulatory requirements",
        "",
    )
    df_mit["Q13a_7"] = np.where(
        df_mit["Q13a"].str.contains(
            "Adherence to industry standards", case=False, na=False
        ),
        "Adherence to industry standards",
        "",
    )
    df_mit["Q13a_99"] = np.where(
        df_mit["Q13a"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q14_1"] = np.where(
        df_mit["Q14(Q4)"].str.contains("AI ethical principles", case=False, na=False),
        "AI ethical standards",
        "",
    )
    df_mit["Q14_2"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Human rights standards", case=False, na=False),
        "Human rights standards",
        "",
    )
    df_mit["Q14_3"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Risk taxonomy", case=False, na=False),
        "Risk taxonomy",
        "",
    )
    df_mit["Q14_4"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Policies and standards", case=False, na=False),
        "Policies and standards",
        "",
    )
    df_mit["Q14_5"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Specific roles and responsibilities within the organization",
            case=False,
            na=False,
        ),
        "Specific roles and responsibilities within the organization",
        "",
    )
    df_mit["Q14_6"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Board of director expertise", case=False, na=False
        ),
        "Board of director expertise",
        "",
    )
    df_mit["Q14_7"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "External advisers/reviewers", case=False, na=False
        ),
        "External advisers/reviewers",
        "",
    )
    df_mit["Q14_8"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Governance and escalation processes", case=False, na=False
        ),
        "Governance and escalation processes",
        "",
    )
    df_mit["Q14_9"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Integration into product development processes", case=False, na=False
        ),
        "Integration into product development processes",
        "",
    )
    df_mit["Q14_10"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Ongoing monitoring and control", case=False, na=False
        ),
        "Ongoing monitoring and control for product-level risks",
        "",
    )
    df_mit["Q14_11"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Ongoing monitoring and refinement", case=False, na=False
        ),
        "Ongoing monitoring and refinement of the RAI program",
        "",
    )
    df_mit["Q14_12"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Code libraries and software tools", case=False, na=False
        ),
        "Code libraries and software tools",
        "",
    )
    df_mit["Q14_13"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Questionnaires", case=False, na=False),
        "Questionnaires, product risk assessments, product impact assessments",
        "",
    )
    df_mit["Q14_14"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Training and technical", case=False, na=False),
        "Training and technical tutorials",
        "",
    )
    df_mit["Q14_15"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Metrics and reporting", case=False, na=False),
        "Metrics and reporting",
        "",
    )
    df_mit["Q14_16"] = np.where(
        df_mit["Q14(Q4)"].str.contains(
            "Communication and cultural change", case=False, na=False
        ),
        "Communication and cultural change",
        "",
    )
    df_mit["Q14_17"] = np.where(
        df_mit["Q14(Q4)"].str.contains("Regulatory affairs", case=False, na=False),
        "Regulatory affairs",
        "",
    )
    df_mit["Q14_18"] = np.where(
        df_mit["Q14(Q4)"].str.contains("", case=False, na=False), "", ""
    )

    df_mit["Q16_1"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Transparency", case=False, na=False),
        "Transparency",
        "",
    )
    df_mit["Q16_2"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Explainability", case=False, na=False),
        "Explainability",
        "",
    )
    df_mit["Q16_3"] = np.where(
        df_mit["Q16(Q6)"].str.contains(
            "Social and environmental impact", case=False, na=False
        ),
        "Social and environmental impact",
        "",
    )
    df_mit["Q16_4"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Accountability", case=False, na=False),
        "Accountability",
        "",
    )
    df_mit["Q16_5"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Fairness and equity", case=False, na=False),
        "Fairness and equity",
        "",
    )
    df_mit["Q16_6"] = np.where(
        df_mit["Q16(Q6)"].str.contains(
            "Safety, security, and robustness", case=False, na=False
        ),
        "Safety, security, and robustness",
        "",
    )
    df_mit["Q16_7"] = np.where(
        df_mit["Q16(Q6)"].str.contains(
            "Data security/cybersecurity", case=False, na=False
        ),
        "Data security/cybersecurity",
        "",
    )
    df_mit["Q16_8"] = np.where(
        df_mit["Q16(Q6)"].str.contains(
            "data protection", case=False, na=False
        ),
        "Data privacy (data protection)",
        "",
    )
    df_mit["Q16_9"] = np.where(
        df_mit["Q16(Q6)"].str.contains(
            "Individual/personal privacy", case=False, na=False
        ),
        "Individual/personal privacy",
        "",
    )
    df_mit["Q16_10"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Human wellbeing", case=False, na=False),
        "Human wellbeing",
        "",
    )
    df_mit["Q16_13"] = np.where(
        df_mit["Q16(Q6)"].str.contains("Other", case=False, na=False), "Other", ""
    )

    df_mit["Q21_1_1"] = np.where(
        df_mit["Q22_1"].str.contains("RAI efforts", case=False, na=False),
        "Data science team involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_2"] = np.where(
        df_mit["Q22_2"].str.contains("RAI efforts", case=False, na=False),
        "SVP involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_3"] = np.where(
        df_mit["Q22_3"].str.contains("RAI efforts", case=False, na=False),
        "CIO involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_4"] = np.where(
        df_mit["Q22_4"].str.contains("RAI efforts", case=False, na=False),
        "CEO involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_5"] = np.where(
        df_mit["Q22_5"].str.contains("RAI efforts", case=False, na=False),
        "CTO involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_6"] = np.where(
        df_mit["Q22_6"].str.contains("RAI efforts", case=False, na=False),
        "CISO involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_7"] = np.where(
        df_mit["Q22_7"].str.contains("RAI efforts", case=False, na=False),
        "Chief data officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_8"] = np.where(
        df_mit["Q22_8"].str.contains("RAI efforts", case=False, na=False),
        "Chief privacy officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_9"] = np.where(
        df_mit["Q22_9"].str.contains("RAI efforts", case=False, na=False),
        "Chief AI ethics officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_10"] = np.where(
        df_mit["Q22_10"].str.contains("RAI efforts", case=False, na=False),
        "Chief compliance officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_11"] = np.where(
        df_mit["Q22_11"].str.contains("RAI efforts", case=False, na=False),
        "Chief legal counsel involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_12"] = np.where(
        df_mit["Q22_12"].str.contains("RAI efforts", case=False, na=False),
        "Chief AI officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_13"] = np.where(
        df_mit["Q22_13"].str.contains("RAI efforts", case=False, na=False),
        "Chief digital officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_14"] = np.where(
        df_mit["Q22_14"].str.contains("RAI efforts", case=False, na=False),
        "Board of directors involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_15"] = np.where(
        df_mit["Q22_15"].str.contains("RAI efforts", case=False, na=False),
        "Responsible AI committee involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_16"] = np.where(
        df_mit["Q22_16"].str.contains("RAI efforts", case=False, na=False),
        "External adviser/committee involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_17"] = np.where(
        df_mit["Q22_17"].str.contains("RAI efforts", case=False, na=False),
        "Other involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_19"] = np.where(
        df_mit["Q22_19"].str.contains("RAI efforts", case=False, na=False),
        "Chief risk officer involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_20"] = np.where(
        df_mit["Q21_20"].str.contains("RAI efforts", case=False, na=False),
        "Director involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_21"] = np.where(
        df_mit["Q21_21"].str.contains("RAI efforts", case=False, na=False),
        "Manager involved in RAI efforts",
        "",
    )
    df_mit["Q21_1_22"] = np.where(
        df_mit["Q21_22"].str.contains("RAI efforts", case=False, na=False),
        "Legal Department involved in RAI efforts",
        "",
    )

    df_mit["Q21_2_1"] = np.where(
        df_mit["Q22_1"].str.contains("first-party", case=False, na=False),
        "Data science team involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_2"] = np.where(
        df_mit["Q22_2"].str.contains("first-party", case=False, na=False),
        "SVP involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_3"] = np.where(
        df_mit["Q22_3"].str.contains("first-party", case=False, na=False),
        "CIO involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_4"] = np.where(
        df_mit["Q22_4"].str.contains("first-party", case=False, na=False),
        "CEO involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_5"] = np.where(
        df_mit["Q22_5"].str.contains("first-party", case=False, na=False),
        "CTO involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_6"] = np.where(
        df_mit["Q22_6"].str.contains("first-party", case=False, na=False),
        "CISO involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_7"] = np.where(
        df_mit["Q22_7"].str.contains("first-party", case=False, na=False),
        "Chief data officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_8"] = np.where(
        df_mit["Q22_8"].str.contains("first-party", case=False, na=False),
        "Chief privacy officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_9"] = np.where(
        df_mit["Q22_9"].str.contains("first-party", case=False, na=False),
        "Chief AI ethics officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_10"] = np.where(
        df_mit["Q22_10"].str.contains("first-party", case=False, na=False),
        "Chief compliance officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_11"] = np.where(
        df_mit["Q22_11"].str.contains("first-party", case=False, na=False),
        "Chief legal counsel involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_12"] = np.where(
        df_mit["Q22_12"].str.contains("first-party", case=False, na=False),
        "Chief AI officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_13"] = np.where(
        df_mit["Q22_13"].str.contains("first-party", case=False, na=False),
        "Chief digital officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_14"] = np.where(
        df_mit["Q22_14"].str.contains("first-party", case=False, na=False),
        "Board of directors involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_15"] = np.where(
        df_mit["Q22_15"].str.contains("first-party", case=False, na=False),
        "Responsible AI committee involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_16"] = np.where(
        df_mit["Q22_16"].str.contains("first-party", case=False, na=False),
        "External adviser/committee involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_17"] = np.where(
        df_mit["Q22_17"].str.contains("first-party", case=False, na=False),
        "Other involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_19"] = np.where(
        df_mit["Q22_19"].str.contains("first-party", case=False, na=False),
        "Chief risk officer involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_20"] = np.where(
        df_mit["Q21_20"].str.contains("first-party", case=False, na=False),
        "Director involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_21"] = np.where(
        df_mit["Q21_21"].str.contains("first-party", case=False, na=False),
        "Manager involved in risk of AI tools they build",
        "",
    )
    df_mit["Q21_2_22"] = np.where(
        df_mit["Q21_22"].str.contains("first-party", case=False, na=False),
        "Legal Department involved in risk of AI tools they build",
        "",
    )

    df_mit["Q21_3_1"] = np.where(
        df_mit["Q22_1"].str.contains("third-party", case=False, na=False),
        "Data science team involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_2"] = np.where(
        df_mit["Q22_2"].str.contains("third-party", case=False, na=False),
        "SVP involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_3"] = np.where(
        df_mit["Q22_3"].str.contains("third-party", case=False, na=False),
        "CIO involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_4"] = np.where(
        df_mit["Q22_4"].str.contains("third-party", case=False, na=False),
        "CEO involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_5"] = np.where(
        df_mit["Q22_5"].str.contains("third-party", case=False, na=False),
        "CTO involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_6"] = np.where(
        df_mit["Q22_6"].str.contains("third-party", case=False, na=False),
        "CISO involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_7"] = np.where(
        df_mit["Q22_7"].str.contains("third-party", case=False, na=False),
        "Chief data officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_8"] = np.where(
        df_mit["Q22_8"].str.contains("third-party", case=False, na=False),
        "Chief privacy officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_9"] = np.where(
        df_mit["Q22_9"].str.contains("third-party", case=False, na=False),
        "Chief AI ethics officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_10"] = np.where(
        df_mit["Q22_10"].str.contains("third-party", case=False, na=False),
        "Chief compliance officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_11"] = np.where(
        df_mit["Q22_11"].str.contains("third-party", case=False, na=False),
        "Chief legal counsel involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_12"] = np.where(
        df_mit["Q22_12"].str.contains("third-party", case=False, na=False),
        "Chief AI officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_13"] = np.where(
        df_mit["Q22_13"].str.contains("third-party", case=False, na=False),
        "Chief digital officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_14"] = np.where(
        df_mit["Q22_14"].str.contains("third-party", case=False, na=False),
        "Board of directors involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_15"] = np.where(
        df_mit["Q22_15"].str.contains("third-party", case=False, na=False),
        "Responsible AI committee involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_16"] = np.where(
        df_mit["Q22_16"].str.contains("third-party", case=False, na=False),
        "External adviser/committee involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_17"] = np.where(
        df_mit["Q22_17"].str.contains("third-party", case=False, na=False),
        "Other involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_19"] = np.where(
        df_mit["Q22_19"].str.contains("third-party", case=False, na=False),
        "Chief risk officer involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_20"] = np.where(
        df_mit["Q21_20"].str.contains("third-party", case=False, na=False),
        "Director involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_21"] = np.where(
        df_mit["Q21_21"].str.contains("third-party", case=False, na=False),
        "Manager involved in risk of AI tools they buy",
        "",
    )
    df_mit["Q21_3_22"] = np.where(
        df_mit["Q21_22"].str.contains("third-party", case=False, na=False),
        "Legal Department involved in risk of AI tools they buy",
        "",
    )

    df_mit["Q22b_1"] = np.where(
        df_mit["Q22b"].str.contains(
            "Directly engages in product-level discussions", case=False, na=False
        ),
        "Directly engages in product-level discussions",
        "",
    )
    df_mit["Q22b_2"] = np.where(
        df_mit["Q22b"].str.contains(
            "Leads internal communication", case=False, na=False
        ),
        "Leads internal communication",
        "",
    )
    df_mit["Q22b_3"] = np.where(
        df_mit["Q22b"].str.contains(
            "Leads external communication", case=False, na=False
        ),
        "Leads external communication",
        "",
    )
    df_mit["Q22b_4"] = np.where(
        df_mit["Q22b"].str.contains(
            "Shapes our organization's policy and approach", case=False, na=False
        ),
        "Shapes our organization's policy and approach",
        "",
    )
    df_mit["Q22b_7"] = np.where(
        df_mit["Q22b"].str.contains(
            "Responsible for shareholder accountability", case=False, na=False
        ),
        "Responsible for shareholder accountability",
        "",
    )
    df_mit["Q22b_8"] = np.where(
        df_mit["Q22b"].str.contains("Board oversight", case=False, na=False),
        "Board oversight",
        "",
    )
    df_mit["Q22b_9"] = np.where(
        df_mit["Q22b"].str.contains("Driving multi", case=False, na=False),
        "Driving multistakeholder/industrywide engagement on principles",
        "",
    )
    df_mit["Q22b_10"] = np.where(
        df_mit["Q22b"].str.contains(
            "Setting performance targets tied to RAI", case=False, na=False
        ),
        "Setting performance targets tied to RAI",
        "",
    )
    df_mit["Q22b_11"] = np.where(
        df_mit["Q22b"].str.contains(
            "Engaging in hiring decisions", case=False, na=False
        ),
        "Engaging in hiring decisions",
        "",
    )
    df_mit["Q22b_5"] = np.where(
        df_mit["Q22b"].str.contains("Other", case=False, na=False), "Other", ""
    )
    df_mit["Q22b_6"] = np.where(
        df_mit["Q22b"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q24b_1"] = np.where(
        df_mit["Q24b"].str.contains("built", case=False, na=False),
        "AI system was internally built",
        "",
    )
    df_mit["Q24b_2"] = np.where(
        df_mit["Q24b"].str.contains("bought", case=False, na=False),
        "AI system was externally bought, accessed, licensed",
        "",
    )
    df_mit["Q24b_3"] = np.where(
        df_mit["Q24b"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    df_mit["Q25_1"] = np.where(
        df_mit["Q25"].str.contains(
            "Improved recruiting and retention", case=False, na=False
        ),
        "Improved recruiting and retention",
        "",
    )
    df_mit["Q25_2"] = np.where(
        df_mit["Q25"].str.contains("Brand differentiation", case=False, na=False),
        "Brand differentiation",
        "",
    )
    df_mit["Q25_3"] = np.where(
        df_mit["Q25"].str.contains(
            "Increased customer retention", case=False, na=False
        ),
        "Increased customer retention",
        "",
    )
    df_mit["Q25_4"] = np.where(
        df_mit["Q25"].str.contains(
            "Improved long-term profitability", case=False, na=False
        ),
        "Improved long-term profitability",
        "",
    )
    df_mit["Q25_5"] = np.where(
        df_mit["Q25"].str.contains("Accelerated innovation", case=False, na=False),
        "Accelerated innovation",
        "",
    )
    df_mit["Q25_6"] = np.where(
        df_mit["Q25"].str.contains("Better products/services", case=False, na=False),
        "Better products/services",
        "",
    )
    df_mit["Q25_7"] = np.where(
        df_mit["Q25"].str.contains("Other", case=False, na=False), "Other", ""
    )
    df_mit["Q25_8"] = np.where(
        df_mit["Q25"].str.contains("know", case=False, na=False),
        "I don't know",
        "",
    )

    return df_mit
