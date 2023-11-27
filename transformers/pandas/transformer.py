import pandas as pd

def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data[data["result"] != "'None x None'"]
    data["home_team"] = data["teams"].apply(lambda x: x[1:-1].split(" x ")[0])
    data["away_team"] = data["teams"].apply(lambda x: x[1:-1].split(" x ")[1])
    data["home_goals"] = data["result"].apply(lambda x: int(x[1:-1].split(" x ")[0]))
    data["away_goals"] = data["result"].apply(lambda x: int(x[1:-1].split(" x ")[1]))


    def get_home_result(x):
        if x["home_goals"] > x["away_goals"]:
            return 3
        if x["home_goals"] == x["away_goals"]:
            return 1
        return 0


    def get_away_result(x):
        if x["home_goals"] < x["away_goals"]:
            return 3
        if x["home_goals"] == x["away_goals"]:
            return 1
        return 0


    data["home_points"] = data.apply(lambda x: get_home_result(x), axis="columns")
    data["away_points"] = data.apply(lambda x: get_away_result(x), axis="columns")
    data["home_conceded_goals"] = data["away_goals"]
    data["away_conceded_goals"] = data["home_goals"]
    data["home_goal_difference"] = data.apply(
        lambda x: x["home_goals"] - x["away_goals"], axis="columns"
    )
    data["away_goal_difference"] = data.apply(
        lambda x: x["away_goals"] - x["home_goals"], axis="columns"
    )
    data = data.drop(["result", "round", "teams", "date_time"], axis="columns")
    home_data = data.drop(
        [
            "away_team",
            "away_goals",
            "away_points",
            "away_goal_difference",
            "away_conceded_goals",
        ],
        axis="columns",
    )
    home_data = home_data.rename(
        {
            "home_team": "team",
            "home_goals": "goals",
            "home_points": "points",
            "home_goal_difference": "goal_difference",
            "home_conceded_goals": "conceded_goals",
        },
        axis="columns",
    )
    away_data = data.drop(
        [
            "home_team",
            "home_goals",
            "home_points",
            "home_goal_difference",
            "home_conceded_goals",
        ],
        axis="columns",
    )
    away_data = away_data.rename(
        {
            "away_team": "team",
            "away_goals": "goals",
            "away_points": "points",
            "away_goal_difference": "goal_difference",
            "away_conceded_goals": "conceded_goals",
        },
        axis="columns",
    )

    data = pd.concat([home_data, away_data], ignore_index=True)

    sum_grouped_data = data.groupby("team").sum()
    count_grouped_data = data.groupby(["team", "points"]).size().unstack(fill_value=0)
    grouped_data = count_grouped_data.join(sum_grouped_data, on="team").sort_values(
        by=["points",3,"goal_difference"], ascending=False
    )
    grouped_data = grouped_data.rename(
        {
            3: "W",
            1: "D",
            0: "L",
        },
        axis="columns",
    )
    grouped_data["matches"] = grouped_data.apply(lambda x: x["W"] + x["D"] + x["L"], axis="columns")
    grouped_data = grouped_data.reset_index()
    grouped_data = grouped_data.rename(index=lambda x: x + 1)
    grouped_data["rank"] = grouped_data.index

    column_order = ["rank","team","points","matches", "W", "D", "L", "goals", "conceded_goals", "goal_difference"]
    grouped_data = grouped_data[column_order]

    grouped_data["%"] = grouped_data.apply(
        lambda x: int(round( 100 * x["points"] / ((x["W"] + x["D"] + x["L"]) * 3), 2)), axis="columns"
    )
    return grouped_data
