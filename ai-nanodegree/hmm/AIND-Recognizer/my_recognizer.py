import warnings
from asl_data import SinglesData
from math import inf


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    # iterate over all items in test_set. the key is index, so iterate 
    # over range
    for item_num in range(0, test_set.num_items):
        itemProbabilites = dict()

        # Use these to find the best model for given word
        bestLogL = None
        bestWord = None

        # Iterate over all word/model pairs in models
        for word, model in models.items():
            try:
                # Calculate score for given word using given model
                logL = model.score(*test_set.get_item_Xlengths(item_num))

                # Store result
                itemProbabilites[word] = logL

                # Store model with highest likelihood
                if bestLogL is None or logL > bestLogL:
                    bestLogL = logL
                    bestWord = word
            except:
                # In case of error, likelihood is -inf. This way every model
                # has likelihood assingned as required in unit tests
                itemProbabilites[word] = -inf

        probabilities.append(itemProbabilites)
        guesses.append(bestWord)

    return probabilities, guesses

