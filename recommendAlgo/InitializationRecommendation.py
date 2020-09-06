import pandas as pd
import random

class InitializationRecommendation:

    class __RecommendationResult:

        def __init__(self,id,score):
            self.id = id
            self.score = score

    def getRecommendation(self,conn,recommendation_num):

        game_data = pd.read_sql('select * from GameDetail',conn)
        results = []
        for i in range(0,game_data.shape[0]):
            results.append(self.__RecommendationResult(int(game_data['gameId'][i]),game_data['score'][i]))

        results = sorted(results,key=lambda x:x.score,reverse=True)
        results = results[0:30]

        if(recommendation_num>10):
            recommendation_num = 10

        selected_num = []
        for i in range(0,recommendation_num):
            num = random.randint(0,29)
            while selected_num.__contains__(num):
                num = random.randint(0,29)
            selected_num.append(num)

        json_object = 0
        for i in range(0,recommendation_num):
            dataframe = pd.read_sql('select * from GameDetail where gameId='+str(results[selected_num[i]].id),conn)
            if i==0:
                json_object = dataframe
            else:
                json_object = json_object.append(dataframe,ignore_index=True)

        json_object = json_object.to_json(orient='records')
        
        return json_object