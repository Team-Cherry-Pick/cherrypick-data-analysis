from cherrypick_data_analysis.shared.database.database import get_session
import pandas as pd

from cherrypick_data_analysis.shared.database.model import Category


def get_all_category_dataframe():
    session = get_session()
    result = session.query(Category).order_by(Category.category_id).all()

    df = pd.DataFrame([
        {
                "category_id": r.category_id,
                "name" : r.name
        } for r in result
    ])

    return df
