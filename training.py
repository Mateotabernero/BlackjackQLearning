import math 
import numpy as np 
import random 

# I want to separate the training and the deployment into separate files. For it I should use:
# preferred_moves = train_rl_model()

# Save the preferred_moves array to a file
# import numpy as np
# np.save('preferred_moves.npy', preferred_moves)

# And in the other file:

# Load the preferred_moves array
# preferred_moves = np.load('preferred_moves.npy')


# Vamos a hacer una versión fácil en la que todas las cartas tienen las mismas probabilidades de salir independientemente de lo que haya en la mesa (cuidado que 10 aparece tres veces más) 
# Primero no tiene en cuenta la carta que tenga el otro tipejo. 
# Falta implementar lo de que pueda ser 1 u 11 
# Organise the training in one file and the match in another one to upload it to github 

def give_card():
    return random.choice([1,2,3,4,5,6,7,8,9,10,10,10,10]) 

actions = [0, 1]

states = [i for i in range(22)]

values = [[a for a in actions] for _ in states]
Q = [[0 for _ in actions] for _ in states]

def rewards (x):
    if x == 21:
        return 1 
    elif x >21: 
        return -1 
    else: 
        return 0 

# No descontamos el valor de los rewards (por razones medio obvias xd) 


num_episodes = 10000

epsilon = 0.2
alpha = 0.1

for _ in range(num_episodes) :
    s = give_card() 
    s += give_card() 
    
    running = True 
    
    while  running: 
        
        if (random.random() > epsilon): 
            a = actions[np.argmax(Q[s])]
        else:
            a = random.choice([0, 1])

        if (a == 1):
            new_s = s+ give_card() 
            print(a)
            if new_s > 21:
                Q[s][a] += alpha*(-1-Q[s][a])
                running = False

            else:
                Q[s][a] += alpha*(np.max(Q[new_s]) - Q[s][a])
                s = new_s 
        else: 
            running = False 
    
    # Se acabó la parte de pedir cartas. Ahora van los otros 

    s_1 = give_card() 
    s_1 += give_card() 

    while (s_1 <17):
        s_1 += give_card() 
    # Ya ha jugado la casa (Si ha jugado la casa es porque no hemos)

    if (s_1 > 21):
        R = 1
    elif(s == 21):
        if (s_1 == 21):
            R = 0 
        else:
            R = 0
    else:
        if (s > s_1):
            R = 1
        elif (s < s_1):
            R = -1
        else: 
            R = 0 
    if (s <= 21):
        Q[s][a] += alpha*(R-Q[s][a]) 
        
        
print(Q)
# Now the model is trained we can test it

s = int(input("Starting hand: ")) 

running = True
while running :
    a = np.argmax(Q[s])
    print(a)
    if (a == 1):
        increment = int(input("increment: "))
        s += increment 
        if (s > 21):
            print("I lost! Good game!")
            running = False 
            quit() 
    else:
        running =False

dealer_hand = int(input("What's the dealer's hand?: ")) 
if (dealer_hand > 21):
    print ("I won! ") 
elif (dealer_hand > s):
    print("I lost! Well played!") 
elif (dealer_hand ==s):
    print("It's a draw!")
else:
    print("I won")
