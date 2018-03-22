import pandas as pd


def grid_scores_to_df(grid_scores):
    """
    Convert a sklearn.grid_search.GridSearchCV.grid_scores_ attribute to a tidy
    pandas DataFrame where each row is a hyperparameter-fold combinatination.
    """
    rows = list()
    for i, row in enumerate(grid_scores['params']):
        row['mean'] = grid_scores['mean_test_score'][i]
        row['std'] = grid_scores['std_test_score'][i]

        rows.append(row)

    df = pd.DataFrame(rows)
    return df