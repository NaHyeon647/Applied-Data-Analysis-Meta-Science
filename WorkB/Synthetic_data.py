import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Basic settings
SEED = 42
N_GROUP = 60       # 120 participants in total
BASE_MEAN = 55    # Mean liking score in the mismatched group
SD = 15           # Individual variation in liking scores


# 2. Generate one synthetic dataset
def simulate_data(effect_size, seed):
    rng = np.random.default_rng(seed)
    n = N_GROUP * 2

    # Simulate independent participant profiles.
    # These variables do not affect liking in this simple model.
    data = pd.DataFrame({
        "pitch": rng.choice(["low", "high"], n),
        "tempo": rng.choice(["slow", "fast"], n),
        "beat": rng.choice(["weak", "strong"], n),
        "mode": rng.choice(["minor", "major"], n),
    })

    # Randomly assign exactly 60 participants to each condition.
    data["condition"] = rng.permutation(
        ["matched"] * N_GROUP + ["mismatched"] * N_GROUP
    )

    # effect_size is the mean advantage of matching, in score points.
    means = BASE_MEAN + effect_size * (
        data["condition"] == "matched"
    ).astype(int)

    scores = rng.normal(loc=means, scale=SD, size=n)

    # Limit liking scores to the possible range of 0–100.
    # No rounding is applied.
    data["liking"] = np.clip(scores, 0, 100)

    return data


# 3. Create datasets with and without a true effect.
# Reusing the seed keeps profiles, assignments, and random noise
# identical, making the effect parameter easier to compare.
data_effect = simulate_data(effect_size=10, seed=SEED)
data_null = simulate_data(effect_size=0, seed=SEED)


# 4. Summarise and visualise both datasets.
datasets = [
    ("True effect: +10 points", data_effect),
    ("No true effect: 0 points", data_null),
]

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

for ax, (title, data) in zip(axes, datasets):
    print(f"\n{title}")
    print(
        data.groupby("condition")["liking"]
        .agg(["mean", "std", "count"])
        .round(2)
    )

    groups = [
        data.loc[data["condition"] == condition, "liking"]
        for condition in ["mismatched", "matched"]
    ]

    ax.boxplot(groups)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Mismatched", "Matched"])
    ax.set_title(title)
    ax.set_xlabel("Condition")
    ax.set_ylim(0, 100)

axes[0].set_ylabel("Liking score (0–100)")
plt.tight_layout()
plt.show()