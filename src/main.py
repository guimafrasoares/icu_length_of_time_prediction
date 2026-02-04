"""CLI entrypoint for training classification models.

Usage examples:
    python main.py --model xgb
    python main.py -m random_forest

-h shows possible options.
"""

from enum import Enum
import argparse

from modelling_classification import (
    train_xgb_classifier_model,
    train_random_forest_classifier_model,
    train_logistic_regression_model,
    train_knn_classifier_model,
)
from modelling_regression import (
    train_knn_regressor_model,
    train_xgb_regressor_model,
    train_random_forest_regressor_model,
    train_linear_regressor_model,
)
from data_processing import get_prepared_data


class ModelChoice(Enum):
    XGB_CLASSIFIER = "xgb_classifier"
    XGB_REGRESSOR = "xgb_regressor"
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"
    LOGISTIC_REGRESSION = "logistic_regressor"
    LINEAR_REGRESSOR = "linear_regressor"
    KNN_REGRESSOR = "knn_regressor"
    KNN_CLASSIFIER = "knn_classifier"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Train one or more classification models.\n"
            "Possible models: " + ", ".join([e.value for e in ModelChoice])
        )
    )

    parser.add_argument(
        "-m",
        "--model",
        required=True,
        nargs="+",
        choices=[e.value for e in ModelChoice],
        help=(
            "Model(s) to train. Provide one or more of: "
            + ", ".join([e.value for e in ModelChoice])
            + ". Example: -m xgb_classifier random_forest_classifier"
        ),
    )

    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    model_choices = [ModelChoice(m) for m in args.model]

    # Get prepared data
    classification_models = {
        ModelChoice.XGB_CLASSIFIER,
        ModelChoice.RANDOM_FOREST_CLASSIFIER,
        ModelChoice.LOGISTIC_REGRESSION,
        ModelChoice.KNN_CLASSIFIER,
    }

    need_classification = any(mc in classification_models for mc in model_choices)
    X_train, X_test, y_train, y_test = get_prepared_data(
        database_url="postgresql://gms@localhost/mimiciv", classification=need_classification
    )

    mapping = {
        ModelChoice.XGB_CLASSIFIER: train_xgb_classifier_model,
        ModelChoice.XGB_REGRESSOR: train_xgb_regressor_model,
        ModelChoice.RANDOM_FOREST_CLASSIFIER: train_random_forest_classifier_model,
        ModelChoice.RANDOM_FOREST_REGRESSOR: train_random_forest_regressor_model,
        ModelChoice.LOGISTIC_REGRESSION: train_logistic_regression_model,
        ModelChoice.LINEAR_REGRESSOR: train_linear_regressor_model,
        ModelChoice.KNN_REGRESSOR: train_knn_regressor_model,
        ModelChoice.KNN_CLASSIFIER: train_knn_classifier_model,
    }

    # Iterate through requested models and train each
    for mc in model_choices:
        trainer = mapping.get(mc)
        if trainer is None:
            print(f"Unknown model choice: {mc}")
            continue

        print(f"\n--- Training model: {mc.value} ---")
        trainer(X_train, y_train, X_test, y_test)
    print("\nAll requested trainings finished.")


if __name__ == "__main__":
    main()
