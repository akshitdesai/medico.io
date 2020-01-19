def predict_dia_sym(tempp):
    import numpy as np
    import pandas
    from sklearn import model_selection
    from sklearn.linear_model import LogisticRegression
    import pickle

    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

    temp = np.asarray(tempp)
    temp.shape
    temp = temp.reshape(1,-1)
    print(temp.reshape(1,-1).shape)
    predicted_ans = loaded_model.predict_proba(temp)

    return predicted_ans
