from bitte.apps.recommender.helper import *
class RecommenderEvaluator:
    """
        Implementation of tecniques for evaluation the utility of
        recommendations produced by a recommendation system
    """
    RATING = 0
    OPTIMUM = 3.0
    # Classification accuracy metrics allow to evaluate how effectively
    # predictions help the active user
    # in distinguishing good items from bad items

    def precision(self,user_id, recommendations, udb):
        """
            This method measure the proportion of the recommendations that are good recommendations
        """
        all = len(recommendations)
        #log = Helper()
        #log.logger("all",all)
        tp = 0
        for (x, y) in recommendations:
            for item in udb[user_id].keys():
                if item == y and (round(x) - 1 <= udb[user_id][item][self.RATING] <= round(x) + 1):
                #if item == y:
                    tp += 1
        #log.logger("tp",tp)
        #log.logger("all",float(all))
        #log.logger("tp/float(all)",tp/float(all))
        return tp/float(all)

    def recall(self,user_id, recommendations, udb):
        """
            This method measure the proportion of the good recommendations that appear in top recommendations
        """
        tp = 0
        good_items = 0
        for item in udb[user_id].keys():
            if  self.OPTIMUM + 1 >= udb[user_id][item][self.RATING] >= self.OPTIMUM - 1:
                    good_items += 1
                    for (x, y) in recommendations:
                        if item == y:
                            tp += 1
        return tp/float(good_items)

    def f_measure(self,precision, recall):
        """
            f1score algorithm
            Calculates the fmeasure for precision p and recall r.
        """
        return 2 * (precision * recall)/(precision + recall)


    #Errors metrics measure how much the prediction p is close to the true numerical rating a expressed by the user

    def mean_absolute_error(self):
        """
            MAE
        """

    def mean_squared_error(self):
        """
            MSE
        """

    def root_mean_squared_error(self):
        """
            RMSE
        """

