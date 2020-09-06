import pandas as pd
import rule_engine
import random

class CustomizedRecommendation:

    class __RecommendationResult:

        def __init__(self, id, score):
            self.id = id
            self.score = score

    def __init__(self):
        context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
        self.rule_1 = rule_engine.Rule('main_genre == "" and platform == "" ',context = context)
        self.rule_2 = rule_engine.Rule('main_genre != "" and platform == "" ',context = context)
        self.rule_3 = rule_engine.Rule('main_genre == "" and platform != "" ',context = context)
        self.rule_4 = rule_engine.Rule('main_genre != "" and platform != "" ',context = context)
        context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
        self.rule_5 = rule_engine.Rule('main_genres_length == 0 and platforms_length != 0 ',context = context)
        self.rule_6 = rule_engine.Rule('main_genres_length != 0 and platforms_length == 0 ',context = context)
        self.rule_7 = rule_engine.Rule('main_genres_length == 0 and platforms_length == 0 ',context = context)
        self.rule_8 = rule_engine.Rule('main_genres_length != 0 and platforms_length != 0 ',context = context)
        context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
        self.rule_9 = rule_engine.Rule('recommendation_num > 20',context = context)
        self.rule_10 = rule_engine.Rule('results_length > 60',context = context)
        self.rule_11 = rule_engine.Rule('recommendation_num > results_length',context = context)

    def __getInitialRecommendation(self,conn,main_genre,platform):

        class Condition(object):
            def __init__(self,main_genre,platform):
                self.main_genre = main_genre
                self.platform = platform
        
        condition = Condition(main_genre,platform)
        game_data = 0

        if self.rule_1.matches(condition):
            game_data = pd.read_sql('select * from GameDetail',conn)

        if self.rule_2.matches(condition):
            game_data = pd.read_sql("select * from GameDetail where mainGenre= '"+main_genre+"'",conn)

        if self.rule_3.matches(condition):
            game_data = pd.read_sql("select * from GameDetail where platform='"+platform+"'",conn)

        if self.rule_4.matches(condition):
            game_data = pd.read_sql("select * from GameDetail where mainGenre= '"+main_genre+"' and platform= '"+platform+"'",conn)

        return game_data

    def __results2json(self,results,conn):

        json_object = 0
        for i in range(0,len(results)):
            dataframe = pd.read_sql('select * from GameDetail where gameId='+str(results[i].id),conn)
            if i==0:
                json_object = dataframe
            else:
                json_object = json_object.append(dataframe,ignore_index=True)

        return json_object.to_json(orient='records')

    def __recommendationResultsFilter(self,game_datas,recommendation_num):

        class Condition(object):
            def __init__(self,recommendation_num,results_length):
                self.recommendation_num = recommendation_num
                self.results_length = results_length
        
        results = []
        for i in range(0,len(game_datas)):
            game_data = game_datas[i]
            for j in range(0,game_data.shape[0]):
                results.append(self.__RecommendationResult(int(game_data['gameId'][j]),game_data['score'][j]))

        results = sorted(results,key=lambda x:x.score,reverse = True)

        conditon = Condition(recommendation_num,len(results))

        if self.rule_9.matches(conditon):
            recommendation_num = 20

        if self.rule_10.matches(conditon):
            results = results[0:60]
        
        if self.rule_11.matches(conditon):
            return self.__results2json(results)
        
        new_results = []
        gap = len(results)/recommendation_num
        for i in range(0,recommendation_num):
            start = int(i*gap + 0.5)
            end = int((i+1)*gap + 0.5)
            new_results.append(results[random.randint(start,end-1)])

        return new_results

    def getRecommendation(self,conn,platforms,main_genres,recommendation_num):

        class Condition(object):
            def __init__(self,main_genres_length,platforms_length):
                self.main_genres_length = main_genres_length
                self.platforms_length = platforms_length

        condition = Condition(len(main_genres),len(platforms))

        game_datas = []

        if self.rule_5.matches((condition)):
            for i in range(0,len(platforms)):
                game_data = self.__getInitialRecommendation(conn,'',platforms[i])
                if ~game_data.empty:
                    game_datas.append(game_data)

        if self.rule_6.matches((condition)):
            for i in range(0,len(main_genres)):
                game_data = self.__getInitialRecommendation(conn,main_genres[i],'')
                if ~game_data.empty:
                    game_datas.append(game_data)

        if self.rule_7.matches((condition)):
            game_datas.append(self.__getInitialRecommendation(conn,'',''))

        if self.rule_8.matches((condition)):
            for i in range(0,len(platforms)):
                for j in range(0,len(main_genres)):
                    game_data = self.__getInitialRecommendation(conn,main_genres[j],platforms[i])
                    if ~game_data.empty:
                        game_datas.append(game_data)

        results = self.__recommendationResultsFilter(game_datas,recommendation_num)

        json_object =  self.__results2json(results,conn) 
        return json_object