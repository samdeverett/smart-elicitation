from data import call_api, create_df
from suggestions import get_suggestions


if __name__=="__main__":

    # Get data
    response = call_api()
    df = create_df(response)

    # Get claims
    claims = list(df.claim.values[16:24])

    # Generate suggestions from claims
    get_suggestions(claims, verbose=True)
