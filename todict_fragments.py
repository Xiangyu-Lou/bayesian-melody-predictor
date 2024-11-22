import numpy as np
import sys

class Song:
    def __init__(self, name, pitches):
        self._name = name
        self._pitches = [int(p) for p in pitches]

    def __str__(self):
        return f"Name: {self._name}, Pitches: {self._pitches}"

def calculate_probabilities2(data):
    probabilities = []
    for x in range(12):
        temp = [0]*12
        probabilities.append(temp)
    for x in range(len(data)):
        for y in range(len(data[x])-1):
            probabilities[data[x][y]][data[x][y+1]] += 1
    for x in range(len(probabilities)):
        temp_sum = sum(probabilities[x])
        if temp_sum == 0:
            temp_sum = 1
        for y in range(len(probabilities[x])):
            probabilities[x][y] /= temp_sum
    return probabilities

def calculate_probabilities3(data):
    probabilities = []
    for x in range(12):
        temp_x = []
        for y in range(12):
            temp_y = [0]*12
            temp_x.append(temp_y)
        probabilities.append(temp_x)
        
    for x in range(len(data)):
        for y in range(len(data[x])-2):
            probabilities[data[x][y]][data[x][y+1]][data[x][y+2]] += 1
    
    for x in range(len(probabilities)):
        for y in range(len(probabilities[x])):
            temp_sum = sum(probabilities[x][y])
            if temp_sum == 0:
                temp_sum = 1
            for z in range(len(probabilities[x][y])):
                probabilities[x][y][z] /= temp_sum
                
    return probabilities


def calculate_probabilities4(data):
    probabilities = []
    for x in range(12):
        temp_x = []
        for y in range(12):
            temp_y = []
            for z in range(12):
                temp_z = [0]*12
                temp_y.append(temp_z)
            temp_x.append(temp_y)
        probabilities.append(temp_x)
        
    for x in range(len(data)):
        for y in range(len(data[x])-3):
            probabilities[data[x][y]][data[x][y+1]][data[x][y+2]][data[x][y+3]] += 1
    
    for x in range(len(probabilities)):
        for y in range(len(probabilities[x])):
            for z in range(len(probabilities[x][y])):
                temp_sum = sum(probabilities[x][y][z])
                if temp_sum == 0:
                    temp_sum = 1
                for w in range(len(probabilities[x][y][z])):
                    probabilities[x][y][z][w] /= temp_sum
                
    return probabilities

def calculate_probabilities5(data):
    probabilities = []
    for a in range(12):
        temp_a = []
        for b in range(12):
            temp_b = []
            for c in range(12):
                temp_c = []
                for d in range(12):
                    temp_d = [0] * 12
                    temp_c.append(temp_d)
                temp_b.append(temp_c)
            temp_a.append(temp_b)
        probabilities.append(temp_a)
        
    for sequence in data:
        for i in range(len(sequence) - 4):
            a, b, c, d, e = sequence[i], sequence[i+1], sequence[i+2], sequence[i+3], sequence[i+4]
            probabilities[a][b][c][d][e] += 1
    
    for a in range(12):
        for b in range(12):
            for c in range(12):
                for d in range(12):
                    temp_sum = sum(probabilities[a][b][c][d])
                    if temp_sum == 0:
                        temp_sum = 1
                    for e in range(12):
                        probabilities[a][b][c][d][e] /= temp_sum
                        
    return probabilities


def calculate_probabilities6(data):
    probabilities = []
    for a in range(12):
        temp_a = []
        for b in range(12):
            temp_b = []
            for c in range(12):
                temp_c = []
                for d in range(12):
                    temp_d = []
                    for e in range(12):
                        temp_e = [0] * 12
                        temp_d.append(temp_e)
                    temp_c.append(temp_d)
                temp_b.append(temp_c)
            temp_a.append(temp_b)
        probabilities.append(temp_a)
        
    for sequence in data:
        for i in range(len(sequence) - 5):
            a, b, c, d, e, f = sequence[i], sequence[i+1], sequence[i+2], sequence[i+3], sequence[i+4], sequence[i+5]
            probabilities[a][b][c][d][e][f] += 1
    
    for a in range(12):
        for b in range(12):
            for c in range(12):
                for d in range(12):
                    for e in range(12):
                        temp_sum = sum(probabilities[a][b][c][d][e])
                        if temp_sum == 0:
                            temp_sum = 1
                        for f in range(12):
                            probabilities[a][b][c][d][e][f] /= temp_sum
                        
    return probabilities

song_list = []

with open("q1_songs.txt", "r") as f:
    for line in f:
        name, pitches_str = line.strip().split(":")
        pitches_list = [int(p) for p in pitches_str.split(",")]
        temp = Song(name, pitches_list)
        song_list.append(temp)

song_list_pitches = [x._pitches for x in song_list]

probs2 = calculate_probabilities2(song_list_pitches)
probs3 = calculate_probabilities3(song_list_pitches)
probs4 = calculate_probabilities4(song_list_pitches)
probs5 = calculate_probabilities5(song_list_pitches)
probs6 = calculate_probabilities6(song_list_pitches)

for a in range(len(probs2)):
    for b in range(len(probs2[a])):
        if probs2[a][b] == 0.0 and a != 0 and b != 0:
            print("constraint forall(i in 1..n-1)(z[i] = " + str(a) + " -> z[i+1] != " + str(b) +");")

for a in range(len(probs3)):
    for b in range(len(probs3[a])):
        for c in range(len(probs3[a][b])):
            if probs3[a][b][c] == 0.0 and a != 0 and b != 0 and c != 0:
                print("constraint forall(i in 1..n-2)(z[i] = " + str(a) + " /\ z[i+1] = " + str(b) + " -> z[i+2] != " + str(c) +");")


for a in range(len(probs4)):
    for b in range(len(probs4[a])):
        for c in range(len(probs4[a][b])):
            for d in range(len(probs4[a][b][c])):
                if probs4[a][b][c][d] == 0.0 and a != 0 and b != 0 and c != 0 and d != 0:
                    print("constraint forall(i in 1..n-3)(z[i] = " + str(a) + " /\ z[i+1] = " + str(b) + " /\ z[i+2] = " + str(c) + " -> z[i+3] != " + str(d) +");")

for a in range(len(probs5)):
    for b in range(len(probs5[a])):
        for c in range(len(probs5[a][b])):
            for d in range(len(probs5[a][b][c])):
                for e in range(len(probs5[a][b][c][d])):
                    if probs5[a][b][c][d][e] == 0.0 and a != 0 and b != 0 and c != 0 and d != 0 and e != 0:
                        print("constraint forall(i in 1..n-4)(z[i] = " + str(a) + " /\ z[i+1] = " + str(b) + " /\ z[i+2] = " + str(c) + " /\ z[i+3] = " + str(d) + " -> z[i+4] != " + str(e) +");")

for a in range(len(probs6)):
    for b in range(len(probs6[a])):
        for c in range(len(probs6[a][b])):
            for d in range(len(probs6[a][b][c])):
                for e in range(len(probs6[a][b][c][d])):
                    for f in range(len(probs6[a][b][c][d][e])):
                        if probs6[a][b][c][d][e][f] == 0.0 and a != 0 and b != 0 and c != 0 and d != 0 and e != 0 and f != 0:
                            print("constraint forall(i in 1..n-5)(z[i] = " + str(a) + " /\ z[i+1] = " + str(b) + " /\ z[i+2] = " + str(c) + " /\ z[i+3] = " + str(d) + " /\ z[i+4] = " + str(e) + " -> z[i+5] != " + str(f) + ");")



'''
while True:
    input_str = input("Get sequence probability by typing 'NUM1 NUM2 NUM3 NUM4 NUM5 NUM6', or type 'QUIT' to quit: ")

    if (input_str == 'QUIT'):
        sys.exit()

    num1_str, num2_str, num3_str, num4_str = input_str.split()
    num1 = int(num1_str)
    num2 = int(num2_str)
    num3 = int(num3_str)
    num4 = int(num4_str)
    #num5 = int(num5_str)
    #num6 = int(num6_str)

    print("Probability is: " + str(probs4[num1][num2][num3][num4]))
'''
