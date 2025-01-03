import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt


# Load the data
votes = pd.read_csv("data/vote_distances.csv")
votes = votes.dropna()
votes["round"] = votes["round"].astype("category")

votes = votes[votes["distance"] > 0]
votes = votes[votes["round"] == "final"]
# votes = votes[votes["year"] == 2023]
# votes = votes[votes["from_country"] == "de"]
# votes["year"] = votes["year"].astype("category")
votes["distance"] = votes["distance"].astype("int")
votes["distance"] = (votes["distance"] - votes["distance"].mean()) / votes[
    "distance"
].std()

## Linear Effects Model
print(votes.head())
mixed_model = smf.mixedlm(
    formula="total_points ~ distance",
    data=votes,
    groups=votes["year"],
).fit()
print(mixed_model.summary())

# Check the assumptions of the linear effects model
votes["residuals"] = mixed_model.resid
votes["fitted_values"] = mixed_model.fittedvalues

# Plot the residuals
plt.scatter(votes["fitted_values"], votes["residuals"])
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs. Fitted values")
plt.axhline(y=0, color="black", linestyle="--")
plt.show()
