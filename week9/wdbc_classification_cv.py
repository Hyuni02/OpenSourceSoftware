import numpy as np
from sklearn import (datasets, tree, model_selection)
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
import matplotlib

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()

    # Hyperparameter tuning
    best_acc_test = 0
    best_params = {}

    for n_estimators in [100, 200, 300]:
        for learning_rate in [0.01, 0.05, 0.1]:
            # Train a model
            model = AdaBoostClassifier(n_estimators=n_estimators, learning_rate=learning_rate)

            cv_results = model_selection.cross_validate(model, wdbc.data, wdbc.target, cv=5, return_train_score=True)

            # Evaluate the model
            acc_train = np.mean(cv_results['train_score'])
            acc_test = np.mean(cv_results['test_score'])

            # Keep track of the best parameters
            if acc_test > best_acc_test:
                best_acc_test = acc_test
                best_params = {'n_estimators': n_estimators, 'learning_rate': learning_rate}

    # Train the final model with the best parameters
    model = AdaBoostClassifier(n_estimators=best_params['n_estimators'], learning_rate=best_params['learning_rate'])
    model.fit(wdbc.data, wdbc.target)

    # Train a model
    # model = AdaBoostClassifier() # TODO 17

    cv_results = model_selection.cross_validate(model, wdbc.data, wdbc.target, cv=5, return_train_score=True)

    # Evaluate the model
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')