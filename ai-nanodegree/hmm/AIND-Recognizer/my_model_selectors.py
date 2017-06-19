import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):

        # Use these variables to store best model for word
        bestBIC = None
        bestModel = None

        # iterate over all possible models
        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:
                # Create new GaussianHMM model
                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag",
                                        n_iter=1000, random_state=self.random_state,
                                        verbose=self.verbose)

                if self.verbose:
                    print("model created for {} with {} states".format(self.this_word, num_states))

                # Fit model with current data
                hmm_model.fit(self.X, self.lengths)

                # Calculate logL
                logL = hmm_model.score(self.X, self.lengths)

                # Calculate parameters as stated in hmm library
                p = num_states * num_states + 2 * num_states * len(self.X[0]) - 1

                # Calculate BIC using formula BIC = -2 * logL + p * logN
                bic = (-2) * logL + p * math.log(len(self.X))

                # Find model with lowest BIC
                if bestBIC is None or bic < bestBIC:
                    bestModel = hmm_model
                    bestBIC = bic
            except:
                if self.verbose:
                    print("failure on {} with {} states".format(self.this_word, num_states))

        return bestModel



class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):

        # Use these variables to store best model
        bestDIC = None
        bestModel = None

        # Iterate over all possible models
        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:
                # Create new Gaussian HMM
                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag",
                                        n_iter=1000, random_state=self.random_state,
                                        verbose=self.verbose)

                if self.verbose:
                    print("model created for {} with {} states".format(self.this_word, num_states))
                
                # Fit model with current data
                hmm_model.fit(self.X, self.lengths)

                # Calculate logL
                logL = hmm_model.score(self.X, self.lengths)

                otherScores = 0

                # Calculate likelihood SUM for all other words
                for otherWord in self.hwords:
                    if otherWord != self.this_word:
                        otherScores += hmm_model.score(*self.hwords[otherWord])

                # Caluclate dicusing formula DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
                dic = logL - (float(1)/(len(self.hwords) - 1)) * otherScores

                # Find model with highest DIC
                if bestDIC is None or dic > bestDIC:
                    bestModel = hmm_model
                    bestDIC = dic
            except:
                if self.verbose:
                    print("failure on {} with {} states".format(self.this_word, num_states))

        return bestModel


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):

        # Use these variables to store best model
        bestLogL = None
        bestModel = None

        # Iterate over all possible models
        for num_states in range(self.min_n_components, self.max_n_components + 1):

            try:
                # Define split method. Use n_splits = 3 wherever possible. This call needs to be 
                # in try/except block, as it throws out exception for n_split = 1. To improve CV
                # performance, we can increase split count up to len(self.sequences), but this 
                # will also hit performance significantly
                split_method = KFold(n_splits=(len(self.sequences) if (len(self.sequences) < 3) else 3))

                cnt = 0
                sumLogL = 0

                # Create new Gaussian HMM
                hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag",
                                        n_iter=1000, random_state=self.random_state, verbose=self.verbose)

                if self.verbose:
                    print("model created for {} with {} states".format(self.this_word, num_states))

                # fit model with training sequences from KFold and calculate SUM logL
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):

                    hmm_model.fit(*combine_sequences(cv_train_idx, self.sequences))
                    sumLogL += hmm_model.score(*combine_sequences(cv_test_idx, self.sequences))
                    cnt += 1

                # Calculate average LogL
                avgLogL = sumLogL / cnt

                # Maximaze average logL to find best model
                if bestLogL is None or avgLogL > bestLogL:
                    bestModel = hmm_model
                    bestLogL = avgLogL
            except:
                if self.verbose:
                    print("failure on {} with {} states".format(self.this_word, num_states))

        return bestModel

