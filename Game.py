import random, time

curShell,turn,plrCuff,dealCuff = 0,0,0,0
shells,plrInv,dealInv = [],[0]*8,[0]*8
playerEnergy,dealerEnergy = 4,4
damage = 1
dealEmpty,plrEmpty = 8,8
knownShell = -1

def loadSG():
    global curShell,knownShell,turn,plrCuff,dealCuff
    live,blank = 0,0
    plrCuff,dealCuff,turn = 0,0,0

    for _ in range(random.randint(5,7)):
        shell = random.randint(0,1)
        shells.append(shell)
        if shell==0:
            blank+=1
        else:
            live+=1
    curShell = 0
    knownShell = -1
    print(f"{live} LIVE ROUNDS. {blank} BLANKS.")
    time.sleep(1)
    giveItems()

def giveItems():
    global plrInv,dealInv,inv,dealEmpty,plrEmpty
    print("YOU AND DEALER'S ITEMS ARE RESET")
    time.sleep(1.2)

    plrInv,dealInv = [0]*8,[0]*8
    dealEmpty,plrEmpty = 8,8

    itemCount = random.randint(random.randint(2,3),4)
    for _ in range(itemCount):
        tryGive(0,random.randint(1,5))
        time.sleep(0.8)
        tryGive(1,random.randint(1,5))
        time.sleep(0.8)

def tryGive(who,what):
    global plrInv,dealInv,plrEmpty,dealEmpty
    if who == 0 and plrEmpty>0:
        doGive(0,what)
        match what:
            case 1:
                print("YOU GOT A HANDSAW.")
            case 2:
                print("YOU GOT A MAGNIFYING GLASS.")
            case 3:
                print("YOU GOT A CIGARETTE.")
            case 4:
                print("YOU GOT HANDCUFFS.")
            case 5:
                print("YOU GOT A BEER.")
    elif who == 1 and dealEmpty>0:
        doGive(1,what)
        match what:
            case 1:
                print("DEALER GOT A HANDSAW.")
            case 2:
                print("DEALER GOT A MAGNIFYING GLASS.")
            case 3:
                print("DEALER GOT A CIGARETTE.")
            case 4:
                print("DEALER GOT HANDCUFFS.")
            case 5:
                print("DEALER GOT A BEER.")
        
def doGive(who,what):
    global plrEmpty,dealEmpty,plrInv,dealInv
    if who==0:
        plrEmpty+=1
        plrInv[findEmptySlot(0)] = what
    else:
        dealEmpty+=1
        dealInv[findEmptySlot(1)] = what

def findEmptySlot(who):
    empty = -1
    if who == 0:
        for i,item in enumerate(plrInv):
            if item == 0:
                empty = i  
    else:
        for i,item in enumerate(dealInv):
            if item == 0:
                empty = i
    if empty != -1:
        return empty
    else:
        print("lmao this is not meant to happen wtf")
        return 0
    
def findDealerItem(what):
    wanted = -1
    for i,item in enumerate(dealInv):
        if item == what:
            wanted = i
    return wanted

def doTurn():
    global turn,shells,curShell,playerEnergy,dealerEnergy,plrCuff,dealCuff,damage,knownShell
    time.sleep(1)
    if(curShell>len(shells)-1):
        print("THE SHOTGUN IS EMPTY. DEALER IS LOADING IT AGAIN.")
        loadSG()
    match turn:
        case 0:
            if plrCuff==1: 
                plrCuff = 0
                turn = 1
                print("YOU ARE CUFFED. YOUR TURN IS SKIPPED.")
                doTurn()
                return
            action = input("YOUR TURN. TYPE 1 TO SHOOT SELF. TYPE 2 TO SHOOT DEALER. TYPE 3 TO USE ITEM. ")
            match int(action):
                case 1:
                    if(shells[curShell]==0):
                        curShell+=1
                        print("YOU SURVIVE AND SKIP DEALER'S TURN.")
                        if damage == 2:
                            time.sleep(0.6)
                            damage = 1
                            print("THE END OF THE SHOTGUN REGROWS")
                        doTurn()
                    else:
                        playerEnergy-=damage
                        curShell+=1
                        if playerEnergy>0:
                            print(f"YOU WERE BLASTED. ENERGY LEFT: {playerEnergy}")
                            turn = 1
                            if damage == 2:
                                time.sleep(0.6)
                                damage = 1
                                print("THE END OF THE SHOTGUN REGROWS")
                            doTurn()
                        else:
                            print("YOU ARE DEAD, DEALER WINS")
                case 2:
                    if(shells[curShell]==0):
                        curShell+=1
                        print("DEALER SURVIVES.")
                        if damage == 2:
                            time.sleep(0.6)
                            damage = 1
                            print("THE END OF THE SHOTGUN REGROWS")
                        turn = 1
                        doTurn()
                    else:
                        dealerEnergy-=damage
                        curShell+=1
                        if dealerEnergy>0:
                            print(f"DEALER WAS BLASTED. ENERGY LEFT: {dealerEnergy}")
                            turn = 1
                            if damage == 2:
                                time.sleep(0.6)
                                damage = 1
                                print("THE END OF THE SHOTGUN REGROWS")
                            doTurn()
                        else:
                            print("CONGRATS, YOU WIN!")
                case 3:
                    if not plrInv:
                        print("YOU DON'T HAVE ANY ITEMS.")
                        doTurn()
                    else:
                        print("YOUR ITEMS ARE:")
                        for i,item in enumerate(plrInv):
                            match item:
                                case 1:
                                    print(f"{i+1}. HANDSAW: MAKES SHOTGUN DO DOUBLE DAMAGE.")
                                case 2:
                                    print(f"{i+1}. MAGNIFYING GLASS: SHOWS YOU THE CURRENT ROUND IN THE CHAMBER.")
                                case 3:
                                    print(f"{i+1}. CIGARETTE: REGAIN ONE ENERGY.")
                                case 4:
                                    print(f"{i+1}. HANDCUFFS: DEALER SKIPS THE NEXT TURN.")
                                case 5:
                                    print(f"{i+1}. BEER: UNLOADS THE CURRENT ROUND IN THE CHAMBER.")
                                case 0:
                                    print(f"{i+1}. EMPTY ITEM SLOT")
                        itemInd = input("WHAT ITEM SLOT WOULD YOU LIKE TO USE? ")
                        plrItem = plrInv[int(itemInd)-1]
                        if(plrItem!=0):
                            plrInv[int(itemInd)-1] = 0
                        match plrItem:
                            case 0:
                                print("THAT SLOT IS EMPTY.")
                                doTurn()
                            case 1:
                                print("YOU SAW OFF THE END OF THE SHOTGUN. DAMAGE IS DOUBLED.")
                                damage = 2
                                doTurn()
                            case 2:
                                if(shells[curShell]==0):
                                    print("CURRENT SHELL IS EMPTY.")
                                else:
                                    print("CURRENT SHELL IS LIVE.")
                                doTurn()
                            case 3:
                                playerEnergy+=1
                                print(f"YOU SMOKE A CIGARETTE. CURRENT ENERGY: {playerEnergy}")
                                doTurn()
                            case 4:
                                print(f"THE DEALER CUFFS THEMSELF. DEALER'S NEXT TURN IS SKIPPED.")
                                dealCuff = 1
                                doTurn()
                            case 5:
                                if(shells[curShell]==0):
                                    print("YOU UNLOAD A BLANK SHELL")
                                else:
                                    print("YOU UNLOAD A LIVE SHELL")
                                doTurn()
        case 1:
            if dealCuff == 1:
                dealCuff = 0
                turn = 0
                print("DEALER IS CUFFED. THEIR TURN IS SKIPPED")
                doTurn()
                return
            
            if curShell == len(shells) - 1:
                knownShell = shells[curShell]

            action = random.randint(1,random.randint(2,3))
            if knownShell == 1:
                if findDealerItem(1) != -1:
                    action = 3
                else:
                    action = 2
            elif knownShell == 0:
                if findDealerItem(5) != -1 and random.randint(1,3)==1:
                    action = 3
                else:
                    action = 1
            match int(action):
                case 1:
                    print("DEALER SHOOTS THEMSELF.")
                    time.sleep(0.5)
                    if(shells[curShell]==0):
                        curShell+=1
                        knownShell = -1
                        print("DEALER SURVIVES AND SKIPS YOUR TURN.")
                        if damage == 2:
                            time.sleep(0.6)
                            damage = 1
                            print("THE END OF THE SHOTGUN REGROWS")
                        doTurn()
                    else:
                        dealerEnergy-=damage
                        curShell+=1
                        knownShell = -1
                        if dealerEnergy>0:
                            print(f"DEALER WAS BLASTED. ENERGY LEFT: {dealerEnergy}")
                            turn = 0
                            if damage == 2:
                                time.sleep(0.6)
                                damage = 1
                                print("THE END OF THE SHOTGUN REGROWS")
                            doTurn()
                        else:
                            print("CONGRATS, YOU WIN!")
                case 2:
                    print("DEALER SHOOTS YOU.")
                    time.sleep(0.5)
                    if(shells[curShell]==0):
                        curShell+=1
                        knownShell = -1
                        print("YOU SURVIVE.")
                        turn = 0
                        if damage == 2:
                            time.sleep(0.6)
                            damage = 1
                            print("THE END OF THE SHOTGUN REGROWS")
                        doTurn()
                    else:
                        playerEnergy-=damage
                        curShell+=1
                        knownShell = -1
                        if playerEnergy>0:
                            print(f"YOU ARE BLASTED. ENERGY LEFT: {playerEnergy}")
                            turn = 0
                            if damage == 2:
                                time.sleep(0.6)
                                damage = 1
                                print("THE END OF THE SHOTGUN REGROWS")
                            doTurn()
                        else:
                            print("YOU ARE DEAD, DEALER WINS.")
                case 3:
                    if not dealInv:
                        doTurn()
                    else:
                        itemInd = -1
                        if knownShell == 1:
                            if random.randint(1,3) != 1:
                                if findDealerItem(1) != -1:
                                    itemInd = findDealerItem(1)
                            else:
                                if findDealerItem(4) != -1:
                                    itemInd = findDealerItem(4)
                        elif dealerEnergy < playerEnergy:
                            if findDealerItem(3) != -1:
                                itemInd = findDealerItem(3)
                        elif knownShell == 0 and random.randint(1,2) == 1:
                            if findDealerItem(5) != -1:
                                itemInd = findDealerItem(5)
                        if(itemInd == -1):
                            doTurn()
                            return
                        plrItem = plrInv[itemInd]
                        if(plrItem!=0):
                            dealInv[int(itemInd)] = 0
                        match plrItem:
                            case 0:
                                doTurn()
                            case 1:
                                print("DEALER SAWS OFF THE END OF THE SHOTGUN. DAMAGE IS DOUBLED.")
                                damage = 2
                                doTurn()
                            case 2:
                                print("DEALER CHECKS CURRENT SHELL WITH MAGNIFYING GLASS.")
                                knownShell = shells[curShell]
                                doTurn()
                            case 3:
                                dealerEnergy+=1
                                print(f"DEALER SMOKES A CIGARETTE. CURRENT ENERGY: {dealerEnergy}")
                                doTurn()
                            case 4:
                                print(f"DEALER CUFFS YOU. YOUR NEXT TURN IS SKIPPED.")
                                plrCuff = 1
                                doTurn()
                            case 5:
                                print("DEALER TAKES A SIP OF BEER.")
                                time.sleep(0.8)
                                if(shells[curShell]==0):
                                    print("DEALER UNLOADS A BLANK SHELL")
                                else:
                                    print("DEALER UNLOADS A LIVE SHELL")
                                doTurn()

loadSG()
time.sleep(0.5)
doTurn()
