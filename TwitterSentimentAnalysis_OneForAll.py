import csv
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split, cross_val_score


def main():
    # will hold text
    data = []
    # will hold label
    target = []

    tkinter.Tk().withdraw()  # Close the root window
    filename = askopenfilename(title='Show me the Data!')

    try:
        # csv_file = open("%s" % filename, "r", encoding="utf8")
        csv_file = open("%s" % filename, "r", encoding="latin1")
        pass
    except IOError:
        print("File does not exist.")
        print("Quiting...")

        sys.exit()

    root = Tk()
    menubar = Menu(root)

    #
    # Create a pulldown menu, and add it to the menu bar
    #
    filemenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    def close_window():
        root.destroy()

    button = Button(root, text="Good-bye.", command=close_window)
    button.pack()

    #
    # Enter test dataset percentage
    #
    label = Label(root, text="Test dataset size (e.g 0.3)")
    label.pack()
    e1 = Entry(root)
    e1.pack()

    #
    # Enter checkbox
    #
    CheckVar1 = IntVar(root)
    C1 = Checkbutton(root, text="Play Game?", variable=CheckVar1, \
                     onvalue=1, offvalue=0, height=5, \
                     width=20)
    C1.pack()

    #
    # Display the menu
    #
    root.config(menu=menubar)

    extractor = StringVar(root)
    extractor.set("Choose Feature Extractor")  # initial value
    modeler = StringVar(root)
    modeler.set("Choose Model")  # initial value
    option = OptionMenu(root, extractor, "tfidf", "countvectorizer")
    option.pack()
    option2 = OptionMenu(root, modeler, "logistic_regression", "random_forest")
    option2.pack()

    def submit():
        spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        #
        # Choose on which column your data exists
        #
        data_column = 4
        for row in spam_reader:
            data.append(row[data_column])
            target.append(int(row[0]))

        #
        # Specify feature extraction algorithm and data (tfidf, countvectorizer)
        #
        i_extractor = extractor.get()
        print("About to fit transform the data with " + i_extractor)
        if i_extractor == "tfidf":
            extr = TfidfVectorizer(min_df=0, max_features=None, strip_accents='unicode', lowercase=True,
                                   analyzer='word', token_pattern=r'\w{3,}', ngram_range=(1, 1),
                                   use_idf=True, smooth_idf=True, sublinear_tf=True, stop_words="english")

            # extr = TfidfVectorizer(min_df=0, max_features=None, strip_accents='unicode', lowercase=True,
            #                        analyzer='char', token_pattern=r'\w{2,}', ngram_range=(1, 1),
            #                        use_idf=True, smooth_idf=True, sublinear_tf=True, stop_words="english")

            # we fit the TfidfVectorizer transform the dataset
            transformed_data = extr.fit_transform(data)
        elif i_extractor == "countvectorizer":
            extr = CountVectorizer()
            transformed_data = extr.fit_transform(data)

        #
        # Specify model and training data set
        #
        i_model = modeler.get()

        #
        # Split to train and test data
        #
        test_p = float(e1.get())
        X_train, X_test, Y_train, Y_test = train_test_split(transformed_data, target, test_size=test_p,
                                                            random_state=42)
        # fit selected model
        print("About to fit the data with ", i_model)
        if i_model == "logistic_regression":
            model = LogisticRegression(C=1.)
            model.fit(X_train, Y_train)
        elif i_model == "random_forest":
            model = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
            model.fit(X_train, Y_train)
        print("model fitted")

        #
        # Evaluate
        #
        predicted_taget = model.predict(X_test)
        # scores = cross_val_score(model, transformed_data, target, cv=5)
        # print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # scores = cross_val_score(model, transformed_data, target, cv=5, scoring='f1_macro')
        # print("F1 Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        print("********************")
        print("****Evaluation******")
        print("********************")
        print("Acuracy_score: ", accuracy_score(Y_test, predicted_taget))
        matrix = confusion_matrix(Y_test, predicted_taget)
        print("\n")
        print("Confusion Matrix")
        print(matrix)
        f1score = f1_score(Y_test, predicted_taget, average="weighted")
        print("\n")
        print("F1_score is: ", f1score)

        if CheckVar1.get() == 1:

            #
            # Live Testing
            #
            print("*********")
            print("*** Let's play a game ;) ***")
            print("*** Try to be positive! For every negative tweet you lose 1 life! ***")
            print("*********")
            starting_health = 3
            while (starting_health > 0):
                print("Your health is: ", starting_health, ". Enter new tweet: ")
                X_new = input()
                transformed_data = extr.transform([X_new])
                Y_new = model.predict(transformed_data)
                if Y_new == 2:
                    print("Positive: +1 life")
                    starting_health += 1
                elif Y_new == 0:
                    print("Negative: -1 life ")
                    starting_health -= 1
                elif Y_new == 1:
                    print("Neutral: Perfectly balanced, as all things should be.")
                else:
                    print("Wat?Try again ... -1 life")
                    starting_health -= 1
            print("Game Over")

    button = Button(root, text="OK", command=submit)
    button.pack()
    mainloop()


if __name__ == "__main__":
    main()
