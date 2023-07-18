import random
from copy import deepcopy
from operator import attrgetter


class Process:
    def __init__(self,PID,requierement) -> None:
        self.PID = PID
        #the requierement is a % of processor's power
        self.requierement = requierement
        
class Processor:
    def __init__(self,ID) -> None:
        self.ID = ID
        self.currentLoad = 0
        self.totalLoad = 0
        self.queue = []
        self.steps = 0
        
    def loadProcess(self,process):
        self.currentLoad += process.requierement
        self.totalLoad += process.requierement
        self.queue.append(process)

    def getBiggestProcess(self):
        process = max(self.queue,key=attrgetter("requierement"))
        return process
        
    def askForBelowTreshold(self,treshold,setOfProcessors,proc,selfIndexInProcessQueue):
        #array that holds shuffeled processes' index just to make sure that current proc doesn't ask processor y two times
        askOrder = [x for x in range(0,len(setOfProcessors))]
        random.shuffle(askOrder)
        for x in askOrder:
            self.steps+=1
            tempProcChoice = setOfProcessors[x]
            if tempProcChoice.currentLoad < treshold and x != selfIndexInProcessQueue:
                tempProcChoice.loadProcess(proc)
                return True
        return False
    
    def askForAboveTreshold(self,treshold,setOfProcessors):
        #array that holds shuffeled processes' index just to make sure that current proc doesn't ask processor y two times
        askOrder = [x for x in range(0,len(setOfProcessors))]
        random.shuffle(askOrder)
        for x in askOrder:
            self.steps+=1
            tempProcChoice = setOfProcessors[x]
            if tempProcChoice.currentLoad > treshold and tempProcChoice!=self :
                return tempProcChoice
        return False
    
    def sendToDifferentProcessor(self, process, processor):
        processor.loadProcess(process)
        self.currentLoad -= process.requierement
        self.queue.remove(process)
        self.steps+=1
        processor.steps+=1
        
class System:
    def __init__(self) -> None:
        self.processors = []
        self.processQueue = []

    def addProcessor(self,Processor):
        self.processors.append(Processor)

    def addProcessToQueue(self,process):
        self.processQueue.append(process)

    #DONE
    def strategyOne(self,tresholdP,process):
        """
        when process appears on process x, x checks randomly selected processor y for its current load Y
        if the load Y<treshold P, then
        """
    #for process in self.processQueue:
        #pick random processor
        procPick = self.processors[random.randint(0,len(self.processors)-1)]
        #check this processor for its treshold
        if(not procPick.askForBelowTreshold(
                                            tresholdP,
                                            self.processors,
                                            process,
                                            self.processors.index(procPick))):
            procPick.loadProcess(process)
            procPick.steps += 1

    #DONE
    def strategyTwo(self,tresholdP,process):
        """
        when process appears on process x, check if x's load exceeds the treshold p. If it does, search for random processor y
        with load < treshold p, load for y
        """
    #for process in self.processQueue:
        #pick random processor
        procPick = self.processors[random.randint(0,len(self.processors)-1)]
        if procPick.currentLoad>tresholdP:
            if(not procPick.askForBelowTreshold(tresholdP,
                                                self.processors,
                                                process,
                                                self.processors.index(procPick))):
                procPick.loadProcess(process)
        else:
            procPick.loadProcess(process)
            procPick.steps += 1
    
    #IN PROGRESS
    def strategyThree(self, tresholdR,process):
        """
        when process appears on process x, we check whether x.load < tresholdR. If it is, we ask
        (in random order) processors for their current load, and if a processor y.load > tresholdR,
        then x takes some of y's tasks 
        (i'd assume that x would just take the process with the biggest requierement)
        """
        # for process in self.processQueue:
        #     #pick random processor
        procPick = self.processors[random.randint(0,len(self.processors)-1)]
        if (procPick.currentLoad < tresholdR):
            #search for processor with lower load than treshold R
            secondProc = procPick.askForAboveTreshold(tresholdR, self.processors)
            #if there is none that have load < tresholdR, then load it up to x
            if(secondProc!=False):
                secondProc.sendToDifferentProcessor(secondProc.getBiggestProcess(),procPick)
            else:
                procPick.loadProcess(process)
                procPick.steps += 1
        else:
            procPick.loadProcess(process)
            procPick.steps += 1

    def simulate(self, strategy, tresholdP, tresholdR):

        if(strategy=="S1"):
            #while there are processes to be added
            while len(self.processQueue) != 0:
                #load up the process into the set of Processes using picked strategy
                process = self.processQueue.pop(0)

                self.strategyOne(tresholdP, process)
                #simulate the flow of time:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0
                
            #after the processes were cleaned out, but there are some loaded into the processors
            while (sum([x.currentLoad for x in self.processors])) != 0:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0

        elif(strategy=="S2"):
            #while there are processes to be added
            while len(self.processQueue) != 0:
                #load up the process into the set of Processes using picked strategy
                process = self.processQueue.pop(0)
                self.strategyTwo(tresholdP, process)
                #simulate the flow of time:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0
            #after the processes were cleaned out, but there are some loaded into the processors
            while (sum([x.currentLoad for x in self.processors])) != 0:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0
                        
        elif(strategy=="S3"):
            #while there are processes to be added
            while len(self.processQueue) != 0:
                #load up the process into the set of Processes using picked strategy
                process = self.processQueue.pop(0)
                self.strategyThree(tresholdR, process)
                #simulate the flow of time:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0
            #after the processes were cleaned out, but there are some loaded into the processors
            while (sum([x.currentLoad for x in self.processors])) != 0:
                for processor in self.processors:
                    processor.currentLoad -= 6
                    if processor.currentLoad < 0:
                        processor.currentLoad = 0
    
    def printProcessorsData(self,n):
        print(22*"-","STRATEGY ",n,22*"-")
        for processor in self.processors: print("PID:",processor.ID," "*(3-len(str(processor.ID))),"| Load: ",processor.currentLoad," | nOfProcesses: ",len(processor.queue)," "*(3-len(str(len(processor.queue)))),"| Steps: ",processor.steps)
        averageOfSteps = sum([x.steps for x in self.processors])/len(self.processors)
        print("\nAverage number of load queries and process migrations (moves): ",averageOfSteps)
        ACL = sum([x.totalLoad for x in self.processors])/len(self.processors)
        print("Average CPU Load (ACL): ",ACL)
            
if(__name__=="__main__"):
    
    #create Processors
    n = int(input("The ammount of processors (choose in range 50-100): "))
    simulationS1 = System()
    #fill the simulation with processors
    [simulationS1.addProcessor(Processor(x)) for x in range(0,int(n))]
    #fill the simulation with processes (task for the processes to go load)
    [simulationS1.addProcessToQueue(Process(x,random.randint(8, 16))) for x in range(0,n*10)]
    #create copies of an initial simulation to simulate strategies 2 and 3
    simulationS2 = deepcopy(simulationS1)
    simulationS3 = deepcopy(simulationS1)

    #input the data
    tresholdP = int(input("Input the treshold P range(40-100): "))
    tresholdR = int(input("Input the treshold R range(40-100): "))

    simulationS1.simulate("S1", tresholdP, tresholdR)
    simulationS2.simulate("S2", tresholdP, tresholdR)
    simulationS3.simulate("S3", tresholdP, tresholdR)
    
    #presenting the final data

    simulationS1.printProcessorsData(1)
    simulationS2.printProcessorsData(2)
    simulationS3.printProcessorsData(3)
    
    """
    For simulating the flow of time - there is no need to substract from currently picked process,
    instead - just substract from the current load, since the ending data doesn't take the load of each process, but the 
    current load of each processor.
    That will also help with calculating the average - no process will be pop'ed, so there is no problem doing the final division or something idk
    """