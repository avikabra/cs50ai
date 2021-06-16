import csv
import sys
import datetime

#from sklearn.model_selection import train_test_split
#from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Load data
    evidence = []
    labels = []

    with open(filename, encoding="utf-8") as f:
        reader = csv.reader(f)
        count = 0
        ints = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
        
        for row in reader:
            if count != 0:
                e_to_append = row

                # month
                month_name = row[10]
                datetime_object = datetime.datetime.strptime(month_name[0:3], "%b")
                month_number = datetime_object.month - 1
                e_to_append[10] = month_number

                # visitor type
                if row[-3] == "Returning_Visitor":
                    e_to_append[-3] = 1
                else:
                    e_to_append[-3] = 0

                # weekend
                if row[-2] == "TRUE":
                    e_to_append[-2] = 1
                else:
                    e_to_append[-2] = 0
                    
                # convert
                for i in range(len(e_to_append)-1):
                    if i in ints:
                        e_to_append[i] = int(e_to_append[i])
                    else:
                        e_to_append[i] = float(e_to_append[i])

                evidence.append(e_to_append[:17])

                # label
                if row[-1] == "TRUE":
                    e_to_append[-1] = 1
                else:
                    e_to_append[-1] = 0

                labels.append(e_to_append[-1])
                
            count += 1

    print(evidence[0])
    print(labels[0])
    
    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    num_pos = 0
    num_neg = 0
    pos_acc = 0
    neg_acc = 0
    
    for i in range(len(labels)):
        if labels[i] == 1:
            num_pos += 1
            if predictions[i] == 1:
                pos_acc += 1
        else:
            num_neg += 1
            if predictions[i] == 0:
                neg_acc += 1
                
    sens = pos_acc / num_pos
    spec = neg_acc / num_neg
    return (sens, spec)


if __name__ == "__main__":
    main()
