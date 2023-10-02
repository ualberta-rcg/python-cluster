def main(model_name):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_score, recall_score

    # Set a random seed if you want repeatability
    # np.random.seed(1337)

    # Load data
    train_df = pd.read_csv('titanic-train.csv')

    # Choose features and lables
    features = ["Pclass", "Sex", "SibSp", "Parch"]
    X = pd.get_dummies(train_df[features], drop_first=True)
    y = train_df['Survived']

    # Split data into training and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    # Initialize model and fit to training data
    model = get_model(model_name)
    model = model.fit(X_train, y_train)

    # Use model to predict on unseen test data
    predictions = model.predict(X_test)

    # Evaluate how well the model did
    print()
    print('Model: {}'.format(args.model))
    print('Accuracy: {}'.format(accuracy_score(y_test, predictions)))
    print('Precision: {}'.format(precision_score(y_test, predictions)))
    print('Recall: {}'.format(recall_score(y_test, predictions)))

def get_model(model_name):
    if (model_name == "decision_tree"):
        return get_decision_tree()
    elif (model_name == "random_forest"):
        return get_random_forest()
    elif (model_name == "state_vector_machine"):
        return get_state_vector_machine()

def get_decision_tree():
    from sklearn.tree import DecisionTreeClassifier
    return DecisionTreeClassifier(max_depth=3)

def get_random_forest():
    from sklearn.ensemble import RandomForestClassifier
    return RandomForestClassifier(max_depth=3, n_estimators=100)

def get_state_vector_machine():
    from sklearn.svm import SVC
    return SVC(kernel="linear", C=1.0)

def get_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",
                        choices={"decision_tree",
                                 "random_forest",
                                 "state_vector_machine"},
                        help="Select which model to use",
                        required=True)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = get_arguments()
    model_name = args.model
    main(model_name)
