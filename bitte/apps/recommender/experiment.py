# -*- coding:utf-8 -*-
# bitte - context aware recommender system for tourism activities
__author__ = 'icaro'
import pandas as pd
from bitte.apps.recommender.similarities import UserSimilarityFactory
from bitte.apps.recommender.geo_location_distance import Nearby
from bitte.apps.recommender.models import *
from django.contrib.auth.models import User
from collections import Counter
from bitte.apps.recommender.helper import *
from bitte.apps.recommender.evaluator import RecommenderEvaluator
import csv

#compare = lambda x, y: Counter(x) == Counter(y)

class AutoVivification(dict):
    """
        initialize dict of dict in python
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class Experimenter:

    # globals variables
    MAX_DISTANCE = 30 # max distance from current location to  activities location
    USER_ID = 15 # given user
    TOP_N_QTD = 10

    # atributes
    contexto = Context()

    rating = 0
    optimum = 0

    def __init__(self):
        self.rating = 0
        self.optimum = 3.0

    def generic_pre_filter(self, list_of_ratings, given_context):
        """
            Reduction-based approach, that reduces the problem of multi dimentional contextual recommendations
            to standard 2D recommendations space
        """
        contextualized_dataset = []
        context = []

        for rows in list_of_ratings:
            if rows[0] == self.USER_ID:
                contextualized_dataset.append(rows)
            else:
                context = rows[3:]
                # Context
                generalized_companion = context[1:6] == given_context[1:6]
                generalized_temperature = context[0:1]+context[2:6]== given_context[0:1]+ given_context[2:6]
                generalized_motivation = context[0:2]+context[3:6]== given_context[0:2]+ given_context[3:6]
                # Time
                generalized_day_of_week = context[0:3]+context[4:6] == given_context[0:3]+ given_context[4:6]
                generalized_local_time = context[0:4] + context[5:6]== given_context[0:4] + given_context[5:6]
                generalized_season = context[0:5] == given_context[0:5]

                if generalized_companion or generalized_temperature or generalized_motivation or generalized_day_of_week or generalized_local_time or generalized_season:
                    contextualized_dataset.append(rows)
        return contextualized_dataset

    def get_other_prefs(self,users_db, user_id):
        """
            Gets all preferences from users dataset
        """
        limit = int(len(users_db[user_id])/3.0)

        given_user_prefs = AutoVivification()
        import copy;

        other_users_prefs, i = copy.deepcopy(users_db), 0
        for item in users_db[user_id]:
            given_user_prefs[user_id][item] = other_users_prefs[user_id][item]
            del(other_users_prefs[user_id][item])
            i += 1
            if i > limit: break
        return other_users_prefs, given_user_prefs

    def get_recommendations_2d(self,prefs_others, user_id,user_context,user_total_prefs=1,similarity='euclidean'):
        """
            Gets recommendations for a person by using a weighted average  of every other user's rankings
        """
        totals = {}
        simSum = {}
        if user_total_prefs > 0:
            factory = UserSimilarityFactory.get_factory(similarity)
            for other_id in prefs_others:
                if other_id == user_id: continue
                sim = factory.similarity(prefs_others, user_id, other_id)
                if sim <= 0: continue
                for item in prefs_others[other_id]:
                    if item not in prefs_others[user_id] or prefs_others[user_id][item][self.rating] == 0:
                            totals.setdefault(item, 0)
                            totals[item] += prefs_others[other_id][item][self.rating] * sim
                            #Similarity sums
                            simSum.setdefault(item, 0)
                            simSum[item] += sim
            rankings = [(total/simSum[item], item) for item,total in totals.items()]
            rankings.sort()
            rankings.reverse()
            return rankings
        else:
            similarity = 'cosine'
            factory = UserSimilarityFactory.get_factory(similarity)
            for other_id in prefs_others:
                if other_id == user_id: continue
                for item in prefs_others[other_id]:
                    other_context = Counter(prefs_others[other_id][item][1:])
                    user_context = Counter(user_context)
                    sim = factory.context_between_similarity(other_context, user_context)
                    totals.setdefault(item, 0)
                    totals[item] += prefs_others[other_id][item][self.rating] * sim
                    #Similarity sums
                    simSum.setdefault(item, 0)
                    simSum[item] += sim
            rankings = [(total/simSum[item], item) for item,total in totals.items()]
            rankings.sort()
            rankings.reverse()
            return rankings

    def get_nearby_activities(self, lat, long):
        """
            Getting the activities that is nearby the user location
        """
        nearby = Nearby()

        lon_max, lon_min, lat_max, lat_min = nearby.bounding_box(lat, long, self.MAX_DISTANCE)

        activities = Item.objects.filter(
            lat_position__lte=lat_max,
            lat_position__gte=lat_min,
            long_position__lte=lon_max,
            long_position__gte=lon_min).values('id')
        return activities

    def top_n_recommendation(self, recommentations_list):
        """
            This method prints the Top-N list from recommendations
        """
        log = Helper()

        recommentations_list = recommentations_list[:self.TOP_N_QTD]
        reco_item_list = []
        for r in recommentations_list:
            rating,id = r
            item = Item.objects.get(id=id)
            itemphoto = ItemPhoto.objects.get(item=item)
            complement = (item.id,rating,item.name,item.description,item.long_position,
                          item.lat_position,itemphoto.photo.url)
            reco_item_list.append(complement)
        return reco_item_list


    def set_current_context(self, current_context):
        """
            Setting the User current context
        """
        self.contexto.weather  = str(current_context.weather) # temperature
        self.contexto.companion = str(current_context.companion) # companion
        self.contexto.motivation = str(current_context.motivation) # motivation
        # Time
        self.contexto.date = current_context.date # local_time
        #Location
        self.contexto.lat_position = current_context.lat_position #latitude
        self.contexto.long_position = current_context.long_position #longitude
        self.contexto.save()

    def convert_context_to_list(self):
        """
            Convert the current user context to Python list
        """
        given_context = []
        user = User.objects.get(id = self.USER_ID)
        user_profile = user.get_profile()

        # Profile
        #given_context.append(user_profile.age_group) # age_group
        #given_context.append(user_profile.gender) # gender
        # Context
        given_context.append(str(self.contexto.companion)) # companion
        given_context.append(str(self.contexto.weather)) # temperature
        given_context.append(str(self.contexto.motivation)) # motivation
        # Time
        given_context.append(self.contexto.day_of_week) # day_of_week
        given_context.append(self.contexto.local_time) # local_time
        given_context.append(self.contexto.season) # season
        #Location
        #given_context.append(self.contexto.lat_position) #latitude
        #given_context.append(self.contexto.long_position) #longitude

        return given_context

    def create_list_of_ratings(self,r,contexto):
        contexto = contexto.split("|")
        return int(r.user_id),int(r.item_id),int(r.value),contexto[0],contexto[1],contexto[2],contexto[3],contexto[4],contexto[5]

    def get_user_context(self):
        user_context = [str(self.contexto.companion),
                        str(self.contexto.weather),
                        str(self.contexto.motivation),
                        self.contexto.day_of_week,
                        self.contexto.local_time,
                        self.contexto.season]
        return user_context

    def remove_for_testing(self,users_db,user_id):
        limit = int(len(users_db[user_id])/3.0)
        test_udb = AutoVivification()
        import copy;

        train_udb, i = copy.deepcopy(users_db), 0
        for item in users_db[user_id]:
            test_udb[user_id][item] = train_udb[user_id][item]
            del(train_udb[user_id][item])
            i += 1
            if i > limit: break
        return train_udb, test_udb


    def get_recommendations(self, prefs, user_id,similarity='euclidean'):
        totals = {}
        simSum = {}
        factory = UserSimilarityFactory.get_factory(similarity)
        for other_id in prefs:
                if other_id == user_id: continue
                sim = factory.similarity(prefs, user_id, other_id)
                if sim <= 0: continue
                for item in prefs[other_id]:
                    if item not in prefs[user_id] or prefs[user_id][item][self.rating] == 0:
                            totals.setdefault(item, 0)
                            totals[item] += prefs[other_id][item][self.rating] * sim
                            #Similarity sums
                            simSum.setdefault(item, 0)
                            simSum[item] += sim
        rankings = [(total/simSum[item], item) for item,total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings

    def make_experiment(self):
        """
            Main method
        """
        users_to_test = [40,134,60,42,37,70,72,98,104,75,51,86,258,629,
                         52,350,137,151,185,106,165,76,55,99,50,648,63, # 38 users
                         627,837,243,384,58,253,1163,257,168,127,80] # total 503 ratings

        #users_to_test = users_to_test = [40]

        for u in users_to_test:
            user_target = User.objects.get(id=u)
            current_context = CurrentContext.objects.filter(user=user_target)[0]
            self.USER_ID = current_context.user.id
            self.MAX_DISTANCE = 20
            self.set_current_context(current_context.context)
            log = Helper()
            #log.logger("id",u)
            things_to_do = Item.objects.all().values('id')
            # converting things to do objects in one Python List
            list_of_things_to_do = [int(t["id"]) for t in things_to_do]

            # getting ratings of the list of activities nearby the user
            ratings = Rating.objects.filter(item_id__in = list_of_things_to_do).select_related('rating__item','rating__context')
            log = Helper()

            list_of_ratings=[]

            for r in ratings:
                ctx = str(r.context)
                list_of_ratings.append(self.create_list_of_ratings(r,ctx))

            udb = AutoVivification()

            for rows in list_of_ratings:
                udb[rows[0]][rows[1]] = rows[2:]

            train_udb, test_udb = self.remove_for_testing(udb,self.USER_ID)
            recs =  self.get_recommendations(train_udb,self.USER_ID)

            evaluate = RecommenderEvaluator()

            precision_train= evaluate.precision(self.USER_ID, recs, test_udb)
            recall_train = evaluate.recall(self.USER_ID, recs, test_udb)
            f1score_train = evaluate.f_measure(precision_train, recall_train)

            #log.logger("Conventional","2D")
            #log.logger("precision_train",precision_train)
            #log.logger("recall_train",recall_train)
            #log.logger("f1score_train",f1score_train)

            f = open('2D.txt','a')
            f.write(str(precision_train)+','+ str(recall_train)+','+str(f1score_train)+'\n')
            f.close()

            # getting activities nearby the user current locations
            self.contexto.lat_position = -12.970382
            self.contexto.long_position = -38.512382
            things_to_do = self.get_nearby_activities(self.contexto.lat_position, self.contexto.long_position)
            # converting things to do objects in one Python List
            list_of_things_to_do = [int(t["id"]) for t in things_to_do]

            # getting ratings of the list of activities nearby the user
            ratings = Rating.objects.filter(item_id__in = list_of_things_to_do).select_related('rating__item','rating__context')


            list_of_ratings=[]

            for r in ratings:
                ctx = str(r.context)
                list_of_ratings.append(self.create_list_of_ratings(r,ctx))

            udb = AutoVivification()

            for rows in list_of_ratings:
                udb[rows[0]][rows[1]] = rows[2:]

            train_udb, test_udb = self.remove_for_testing(udb,self.USER_ID)
            # getting user current context
            given_context = self.convert_context_to_list()

            #log.logger("test_context",given_context)

            # pre-filtering
            contextualized_db = self.generic_pre_filter(list_of_ratings, given_context)

            user_total_prefs = len(test_udb)
            user_context = self.get_user_context()

            # Generated by Collaborative Filtering
            contextual_recommentations_list =  self.get_recommendations_2d(train_udb, self.USER_ID, user_context,user_total_prefs)

            precision_test = evaluate.precision(self.USER_ID, contextual_recommentations_list, test_udb)
            recall_test =  evaluate.recall(self.USER_ID, contextual_recommentations_list, test_udb)
            f1score_test = evaluate.f_measure(precision_test, recall_test)

            #log.logger("Contextual","3D")
            #log.logger("precision_test",precision_test)
            #log.logger("recall_test",recall_test)
            #log.logger("f1score_test",f1score_test)
            f = open('3D.txt','a')
            f.write(str(precision_test)+','+ str(recall_test)+','+ str(f1score_test)+'\n')
            f.close()

            #precision_melhora = (100 * recall_test/recall_train)-100
            #recall_melhora = (100 * recall_test/recall_train)-100
            #f1score_melhora = (100 * f1score_test/f1score_train)-100

            #f = open('melhoras.txt','a')
            #f.write(str(precision_melhora)+','+ str(recall_melhora)+','+ str(f1score_melhora)+'\n')
            #f.close()

            #log.logger("Comparativo","melhora")
            #log.logger("precision_melhora", (100 * precision_test/precision_train)-100)
            #log.logger("recall_melhora", (100 * recall_test/recall_train)-100)
            #log.logger("f1score_melhora", (100 * f1score_test/f1score_train)-100)

        return "deu certo"





