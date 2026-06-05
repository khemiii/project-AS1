print("Hallo Welt")
print("zweiter versuch")
print("dritter versuch")
print("vierter versuch")
print("fünfter versuch")


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Zufall reproduzierbar machen
np.random.seed(42)
random.seed(42)

# Parameter
gitter_groesse = 30
leere_zellen_anteil = 0.05
schwellenwert = 0.5
max_schritte = 1000

# Initialisierung
gitter = np.random.choice([0, 1, 2], size=(gitter_groesse, gitter_groesse), 
                          p=[leere_zellen_anteil, (1-leere_zellen_anteil)/2, (1-leere_zellen_anteil)/2])

# Funktion zur Prüfung (wie vorher)
def ist_agent_zufrieden(gitter, x, y, schwellenwert):
    typ_des_agenten = gitter[x, y]
    if typ_des_agenten == 0: return True
    gleiche, besetzte = 0, 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < gitter_groesse and 0 <= ny < gitter_groesse:
                if gitter[nx, ny] != 0:
                    besetzte += 1
                    if gitter[nx, ny] == typ_des_agenten: gleiche += 1
    if besetzte == 0: return True
    return (gleiche / besetzte) >= schwellenwert

# Setup für die Animation
fig, ax = plt.subplots()
img = ax.imshow(gitter, cmap='bwr', interpolation='nearest')
ax.set_title("Schelling-Modell: Entstehung von Segregation")

def update(frame):
    """Diese Funktion wird in jedem Schritt aufgerufen"""
    agenten = [(x, y) for x in range(gitter_groesse) for y in range(gitter_groesse) if gitter[x, y] != 0]
    random.shuffle(agenten)
    rote = np.sum(gitter == 1)
    blaue = np.sum(gitter == 2)
    print(f"Schritt {frame}: Rot = {rote}, Blau = {blaue}")
    
    for (x, y) in agenten:
        if not ist_agent_zufrieden(gitter, x, y, schwellenwert):
            leere_zellen = [(i, j) for i in range(gitter_groesse) for j in range(gitter_groesse) if gitter[i, j] == 0]
            if leere_zellen:
                nx, ny = random.choice(leere_zellen)
                gitter[nx, ny] = gitter[x, y]
                gitter[x, y] = 0
                
    img.set_data(gitter)
    return [img]

# Animation starten
ani = animation.FuncAnimation(fig, update, frames=max_schritte, interval=1000, blit=True)
plt.show()


