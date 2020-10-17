import numpy as np
import pandas as pd
import random
import json

class ContentRecommendation:

    class __RecommendationResult:

        def __init__(self, id, title, score):
            self.id = id
            self.title = title
            self.score = score

    # drop off the repeated elements
    def __removeRepeatingResults(self,game_name,results,):
        drop_off_results_id = []
        for i in range(0,len(results)):
            if game_name == results[i].title:
                drop_off_results_id.append(i)
            for j in range(i+1,len(results)):
                if results[i].title == results[j].title:
                    if results[i].score >= results[j].score:
                        drop_off_results_id.append(j)
                    else:
                        drop_off_results_id.append(i)

        new_results = []
        for i in range(0,len(results)):
            judge = True
            for j in drop_off_results_id:
                if i==j:
                    judge = False

            if judge:
                new_results.append(results[i])

        return new_results

    def __recommendationFilter(self,data,results,game_id,recommendation_num):


        new_results = self.__removeRepeatingResults(data["title"][game_id],results)

        # After the processing above, if the number of recommendation result > recommendation_num,
        # then the score of the results is sorted, taking the first 2 / 3. The last 1/3 will be selected randomly
        final_results = []
        if len(new_results)>recommendation_num:
            new_results = sorted(new_results,key=lambda x:x.score,reverse = True)
            random_recommender_num =  int(recommendation_num/3+0.5)
            ranking_recommender_num = recommendation_num - random_recommender_num
            final_results = new_results[0:ranking_recommender_num]
            for i in range(0,random_recommender_num):
                start = ranking_recommender_num + int(i*random_recommender_num/3+0.5)
                end = ranking_recommender_num + int((i+1)*random_recommender_num/3+0.5)
                final_results.append(new_results[random.randint(start,end-1)])
        else:
            final_results = new_results


        return final_results

    def __getInitialRecommendation(self,data,search_result_id,model,recommendation_num,is_reversed,):

        # get the similarity scores of all the game with this game
        sim_scores = list(enumerate(model[search_result_id]))
        # sort those games
        sim_scores = sorted(sim_scores,key=lambda x:x[1], reverse=is_reversed)
        # get the top N games
        sim_scores = sim_scores[0:recommendation_num*3]
        # get the index of those games
        data_indices = [i[0] for i in sim_scores]
        # construct result set
        recommendation_results = []
        for i in range(0,len(data_indices)):
            result = self.__RecommendationResult(data_indices[i],data['title'][data_indices[i]],float(data["score"][data_indices[i]]))
            recommendation_results.append(result)

        recommendation_results = self.__recommendationFilter(data,recommendation_results,search_result_id,recommendation_num)
        return recommendation_results

    def getCookieRecommendation(self,conn,game_id_lst,rec_num,tfidf_path,cv_path):
        game_data = pd.read_sql('select * from GameDetail',conn)
        if(len(game_id_lst) < rec_num):
            game_num = len(game_id_lst)
        else:
            game_num = rec_num
        #load the models, spliting with ','
        tfidf_model = np.loadtxt(tfidf_path,delimiter=',')
        cv_model = np.loadtxt(cv_path,delimiter=',')
        recommedation_set = []
        for i in range(0, game_num):
            tfidf_recommendation_results = self.__getInitialRecommendation(game_data,game_id_lst[i],tfidf_model,1,True)
            cv_recommendation_results = self.__getInitialRecommendation(game_data,game_id_lst[i],cv_model,1,True)
            recommedation_set += tfidf_recommendation_results+cv_recommendation_results

        new_recommendation = self.__removeRepeatingResults('',recommedation_set)

        final_recommendation = []
        if len(new_recommendation)>rec_num:
            id_array = []
            for i in range(0,rec_num):
                while True:
                    id = random.randint(0,len(new_recommendation)-1)
                    if id not in id_array:
                        id_array.append(id)
                        final_recommendation.append(new_recommendation[id])
                        break
        else:
            final_recommendation = new_recommendation

        json_object = 0
        for i in range(0,len(final_recommendation)):
            dataframe = pd.read_sql('select * from GameDetail where gameId='+str(final_recommendation[i].id),conn)
            if i==0:
                json_object = dataframe
            else:
                json_object = json_object.append(dataframe,ignore_index=True)

        json_object = json_object.to_json(orient='records')

        return json_object

    def getRecommendation(self,conn,game_id,game_num,tfidf_path,cv_path):

        game_data = pd.read_sql('select * from GameDetail',conn)

        #load the models, spliting with ','
        tfidf_model = np.loadtxt(tfidf_path,delimiter=',')
        cv_model = np.loadtxt(cv_path,delimiter=',')
        tfidf_recommendation_results = self.__getInitialRecommendation(game_data,game_id,tfidf_model,game_num,True)
        cv_recommendation_results = self.__getInitialRecommendation(game_data,game_id,cv_model,game_num,True)

        new_recommendation = self.__removeRepeatingResults('',tfidf_recommendation_results+cv_recommendation_results)

        final_recommendation = []
        if len(new_recommendation)>game_num:
            id_array = []
            for i in range(0,game_num):
                while True:
                    id = random.randint(0,len(new_recommendation)-1)
                    if id not in id_array:
                        id_array.append(id)
                        final_recommendation.append(new_recommendation[id])
                        break
        else:
            final_recommendation = new_recommendation

        json_object = 0
        for i in range(0,len(final_recommendation)):
            dataframe = pd.read_sql('select * from GameDetail where gameId='+str(final_recommendation[i].id),conn)
            if i==0:
                json_object = dataframe
            else:
                json_object = json_object.append(dataframe,ignore_index=True)

        json_object = json_object.to_json(orient='records')

        return json_object
