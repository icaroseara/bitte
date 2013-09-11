import math
from bitte.apps.recommender.helper import Helper
from collections import Counter
__author__ = 'icaro'

class UserSimilarityFactory(object):
    """
        Abstract Factory
    """
    @staticmethod
    def get_factory(similarity_type):
        if similarity_type is 'euclidean':
            return EuclideanFactory()
        elif similarity_type is 'pearson':
            return PearsonFactory()
        elif similarity_type is 'jaccard':
            return JaccardFactory()
        elif similarity_type is 'cosine':
            return CosineFactory()
        raise TypeError('Unknown Factory.')

class EuclideanFactory:
    """
        Factory
    """
    def similarity(self,prefs,user1,user2):
        """
            Returns a distance-based similarity score for user1 and user2
        """
        sim = {}
        for item in prefs[user1]:
            if item in prefs[user2]:
                sim[item] = 1

        if len(sim) == 0: return 0 #No similarities
        dist = 0.0

        for item in sim:
            dist += pow((prefs[user1][item][0] - prefs[user2][item][0]),2)
        return 1/(1 + math.sqrt(dist))

class PearsonFactory:
    """
        Factory
    """
    def similarity(self,prefs,user1,user2):
        """
            Returns the Pearson correlation coefficient for user1 and user2
        """
        sim = {}
        rating = 0
        for item in prefs[user1]:
            if item in prefs[user2]:
                sim[item] = 1
        n = len(sim)
        if n == 0: return 0 #No similarities
        #Sum of ratings
        sum1 = sum([prefs[user1][item][rating] for item in sim])
        sum2 = sum([prefs[user2][item][rating] for item in sim])
        #Sum of ratings squared
        sumSq1 = sum([(prefs[user1][item][rating]) ** 2 for item in sim])
        sumSq2 = sum([(prefs[user2][item][rating]) ** 2 for item in sim])
        #Sum of product of ratings
        sumProd = sum([(prefs[user1][item][rating])*(prefs[user2][item][rating]) for item in sim])

        num=(n*sumProd)-(sum1*sum2)
        den=math.sqrt((n*sumSq1 - sum1**2)*(n*sumSq2 - sum2**2))
        if den==0: return 0
        r=num/den
        return r

class JaccardFactory:
    """
        Factory
    """
    def similarity(self,prefs,user1,user2):
        return 0

class CosineFactory:
    """
        Factory
    """
    def similarity(self,prefs,user1,user2):
        return 0

    def context_between_similarity(self, ctx1,ctx2):
        terms = set(ctx1).union(ctx2)
        dotprod = sum(ctx1.get(k, 0) * ctx2.get(k, 0) for k in terms)
        magA = math.sqrt(sum(ctx1.get(k, 0)**2 for k in terms))
        magB = math.sqrt(sum(ctx2.get(k, 0)**2 for k in terms))
        sim =  dotprod / (magA * magB)
        return sim