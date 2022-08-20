import pygame
import sqlite3


class HighScoreTable:
    
    def create_game_table(self):
        with sqlite3.connect('game_table.db') as con:
            cur = con.cursor()
            cur.execute(f'''CREATE TABLE IF NOT EXISTS game_score
            ( name TEXT NOT NULL,
            score INTEGER NOT NULL);''')
    
    def update_table(self, name, score):
        with sqlite3.connect('game_table.db') as con:
            cur = con.cursor()
            cur.execute(f'''INSERT INTO game_score (name, score) 
            VALUES ('{name}',{score});''')
    
    def show_top_10_hero(self):
        with sqlite3.connect('game_table.db') as con:
            cur = con.cursor()
            list_name = cur.execute('''
            SELECT name, score 
            FROM game_score
            ORDER BY score DESC
            LIMIT 10;''').fetchall()
        
        return list_name
