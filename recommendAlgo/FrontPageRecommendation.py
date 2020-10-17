from recommendAlgo import ContentRecommendation as cr
from recommendAlgo import InitializationRecommendation as ir

class FrontPageRecommendation:

    #ir: getRecommendation(self,conn,recommendation_num)
    #cookieR: getCookieRecommendation(self,conn,game_id_lst,tfidf_path,cv_path)
    def getRecommendation(self,conn,game_id_lst,rec_num,tfidf_path,cv_path):
        if(len(game_id_lst) < rec_num):
            print("return ir")
            return ir.InitializationRecommendation().getRecommendation(conn,rec_num)
        else:
            print("return cookie cr")
            return cr.ContentRecommendation().getCookieRecommendation(conn, game_id_lst, rec_num,
                "./recommendAlgo/Model/tfidf_model.txt",     #tfidf_path
                "./recommendAlgo/Model/cv_model.txt")     #cv_path
