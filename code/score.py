import pygame

class Score:
    def __init__(self):
        self.__score = 0
        self.__limit = 1000
        self.__multiplier_condition = False
    
    def get_score(self):
        return self.__score
    
    def set_score(self, amount):
        self.__score += amount

        if self.__score < 0:
            self.__score = 0

    def reset_limit(self):
        self.__limit = 1000

    def multiplier_condition(self):
        if self.__score >= self.__limit:
            self.__multiplier_condition = True
            self.__limit += 1000
            return self.__multiplier_condition
        else:
            self.__multiplier_condition = False
            return self.__multiplier_condition