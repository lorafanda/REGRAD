import sys
import psychopy
from psychopy import visual
from psychopy import core
from psychopy import event
from psychopy import gui
from psychopy import sound
import numpy as np
from datetime import datetime
import os.path
import os
from pyo import *
 
psychopy.prefs.hardware['audioLib'] = ['PTB', 'sounddevice','pyo','pygame']

############TO CHANGE##############

R=40 #Radius of Circles, pixels
Center=[[-230,100],[0,100],[230,100],[-230,-100],[0,-100],[230,-100]] # Centers of circles 2 x 3

# Define Paths
folder_path = os.path.dirname(os.path.abspath(__file__))
SoundFile= os.path.join(folder_path,'Go.wav') #Here is the file with the start sound
SoundFile_End= os.path.join(folder_path,'Yay_sound.wav') #Here is the file with the end of each condition
Respath= 'Results'

# Define Colors
green = [-1,0.8,-1]
red = [1,-1,-1]
gray = [0.03,0.03,0.03]
Color=[[gray,gray,gray],[gray,gray,gray]]


def make_circles_big(mywin,R,Color,Center):
    # Function for adjusting the size and color of the 6 pin positions
    Xdpl=int(round(R))
    CircleCenter=Center
    tmp=visual.Circle(mywin,radius=R)
    tmp.setLineColor(Color)
    tmp.setFillColor(Color)
    tmp.pos=CircleCenter
    tmp.draw()


def CirclesPresentation(mywin,R,Colors,Center):
    # Function for displacing the circles, calling make_circles_big
    fix=visual.TextStim(win=mywin,text="+",pos=[0,0], color=[1,1,1])
    fix.draw()
    Color.flatten()
    for i,c in enumerate(Center):
        make_circles_big(mywin,R,Color[i],c)


def onetrial(mywin,R,Center,Color,FileName,TrialNumber, TrialName):
    # function that runs one full trial. Is called after initialization is completed
    
    ## Cleaning and initialization of events
    Clock=core.Clock()
    event.clearEvents(eventType=None)
    Exit=False

    ## Window 1: View Target And Flanker colors
    # Set pins
    CirclesPresentation(mywin, R, Color, Center)
    # Set text
    ParticipantSide=visual.TextStim(win=mywin,text="",color=[1,1,1],pos=[-300,0],anchorHoriz='center',height=30) #Position could be the center of the box that is displayed but not sure
    IntResultsText=visual.TextStim(win=mywin,text="",color=[1,1,1],pos=[0,-200],anchorHoriz='center',height=20) #Position could be the center of the box that is displayed but not sure
    IntResultsText.setText(TrialName + ': ' + str(TrialNumber+1)+'/'+str(80)+'\nPress SPACE to play "GO"') #Here we can change the text to appear on the screen
    IntResultsText.draw() 
    ParticipantSide.setText('Participant\nSide')
    ParticipantSide.draw()
    # Displays all - this shows the info above on the screen (where mywin has been called/used)
    mywin.flip()
    # Collecting "space" keyboard presses and time of press
    while True:
        if len(event.getKeys(keyList=['space']))>0:
            tnow=datetime.now() #This takes the date and time of the moment (thus timestamp)
            timenow = ':'.join([str(tnow.hour),str(tnow.minute),str(tnow.second)])
            timenow = '.'.join([timenow,str(tnow.microsecond)])
            break
    
    ## Window 2: Waiting for participant to complete the tiral. View pressing options
    ParticipantResponse=visual.TextStim(win=mywin,text="",color=[1,1,1],pos=[0,0],anchorHoriz='center',height=30)
    Sound = sound.Sound(SoundFile,volume=Volume) #SoundFile used to start the trial
    Sound.play()
    ParticipantResponse.setText('Wait for Participant to complete trial \n\n\n Press 0 if bad trial. \n Press Space to Continue. \n Press Q to quit')
    ParticipantResponse.setSize(100)
    ParticipantResponse.draw()
    # Displays all
    mywin.flip()
    # Collecting keyboard presses; 'q' = quit; '0'=bad event; 'space' = correct;
    while True:
        if len(event.getKeys(keyList='q'))>0:
            Exit=True
            break
        if Exit:
            break
        if len(event.getKeys(keyList=['num_0','0']))>0: #bad trials, that are stacked at the end
            Correctness = -1
            break        
        if len(event.getKeys(keyList=['space']))>0: #good trials, thus we continue to the next trial
            Correctness = 1
            break
    
    ## Save trial information below: 
    with open(FileName,"a") as FileData:
        txt=[TrialName,str(TrialNumber+1),str(timenow),str(Correctness)]
        FileData.write(",".join(txt))
        FileData.write('\n')

    return Correctness


def createTargetFlankerPositions_randomized():
    # Returns positions (80 times 2x3 position array) and names (80 times 'TxFx' labels)
    # Visualizing Positions:        
    # 1 = Target, 2 = Flanker       __box______
    #                               |0   1   0|
    #     [[0,1,0],[2,0,0]]    =    |2   0   0|
    #                               ```````````
    # 5 repetitions for each position, total 12 positions = 80 trials per eye condition
    # IF more unique trials are added, this function will automatically make 5 copies of each unique trial. Make sure the
    # unique name and position are added to the variables position_list and name_list
    IndexPositions=[]
    CodeNames = []

    # Depth 0:
    T1F1 = np.array([[1,0,0],[2,0,0]]) #1 is target (on 1st position of the top line) and 2 is flanker (on 1st position of the bottom line)
    F1T1 = np.array([[2,0,0],[1,0,0]])
    T3F3 = np.array([[0,0,1],[0,0,2]])
    F3T3 = np.array([[0,0,2],[0,0,1]])
    # T2F2 = # Unused
    # F2T2 = # Unused
    
    # Depth 1:
    T1F2 = np.array([[1,0,0],[0,2,0]])
    F2T1 = np.array([[0,2,0],[1,0,0]])
    T3F2 = np.array([[0,0,1],[0,2,0]])
    F2T3 = np.array([[0,2,0],[0,0,1]])
    # T2F3 # Unused
    # T2F1 # Unused
    # F1T2 # Unused
    # F3T2 # Unused

    # Depth 2:
    T1F3 =  np.array([[1,0,0],[0,0,2]])
    F1T3 =  np.array([[2,0,0],[0,0,1]])
    T3F1 =  np.array([[0,0,1],[2,0,0]])
    F3T1 =  np.array([[0,0,2],[1,0,0]])

    # Trials with no flanker: 
    T1F0 =  np.array([[1,0,0],[0,0,0]])
    F0T3 =  np.array([[0,0,0],[0,0,1]])
    T3F0 =  np.array([[0,0,1],[0,0,0]])
    F0T1 =  np.array([[0,0,0],[1,0,0]])

    # Create list of trial positions and names
    position_list=[T1F1, F1T1, T3F3, F3T3, T1F2, F2T1, T3F2, F2T3, T1F3, F1T3, T3F1, F3T1, T1F0, T3F0, F0T1, F0T3] #this is the list of the unique positions that we use in the whole condition
    name_list=['T1F1', 'F1T1', 'T3F3', 'F3T3', 'T1F2', 'F2T1', 'T3F2', 'F2T3', 'T1F3', 'F1T3', 'T3F1', 'F3T1', 'T1F0', 'T3F0', 'F0T1', 'F0T3'] #names of the unique positions, so that they are displayed in the window and saved in the txt file
    [[IndexPositions.append(i) for i in position_list] for i in range(5)] #the number in range() means the number of repetitions for each unique condition
    [[CodeNames.append(i) for i in name_list] for i in range(5)]
    
    # Randomize both position and name with same order
    NamePositionZip = list(zip(IndexPositions, CodeNames))
    np.random.shuffle(NamePositionZip)
    IndexPositions, CodeNames = zip(*NamePositionZip)

    return IndexPositions, CodeNames


# Experiment begins
Exp=True
while True:
    # Initialize all fields in pop-up window
    DlgInit = gui.Dlg(title="Initialisation")
    DlgInit.addField("Subject Number :" )
    DlgInit.addField("Condition:",choices=["ND", "DO","BI"])
    DlgInit.addField("Age : ")
    DlgInit.addField('Sex:', choices=["M", "F"])
    DlgInit.addField('Handedness:', choices=["R", "L"])
    DlgInit.addField('Amblyopic Eye:', choices=["R", "L"])
    DlgInit.addField('Study Part :', choices=['REV','AMB'])
    DlgInit.addField("Time Point : ", choices=["T1", "T2"])
    DlgInit.addField("Volume (0-1) : ",1)
    DlgInit.show()
    InitialData = DlgInit.data
    if InitialData==['', 'ND','', 'M', 'R', 'REV','T1',1]: # Cancel if Cancel is pressed
        Exp=False
        break
    else:
        SbjNumber=InitialData[0]
        FirstCondition=InitialData[1]
        Age=InitialData[2]
        Sex=InitialData[3]
        Handedness=InitialData[4]
        AmblyopicEye=InitialData[5]
        Study=InitialData[6]
        Timepoint=InitialData[7]
        Volume=InitialData[8]
        FileName=SbjNumber+'_'+FirstCondition+'_'+Timepoint+'_'+Study+'.txt' #Here we can change the file name by modifying the different variables
        FileName=Respath+'/'+FileName
        if os.path.isfile(FileName):
            print('THIS FILE EXITS. DELETE FILE WITH SAME NAME THEN RERUN THE EXPERIMENT')
            break
        else:
            with open(FileName,'w') as FileData:
                FileData.write('STUDY : '+Study+'\n')
                FileData.write('SubjectNumber : '+SbjNumber+'\n')
                FileData.write('Condition : '+FirstCondition+'\n')
                FileData.write('Age : '+Age+'\n')
                FileData.write('Sex : ' +Sex + '\n')
                FileData.write('Handedness : '+Handedness+'\n')
                FileData.write('Amblyopic Eye : ' + AmblyopicEye + '\n')
                FileData.write('Expriment,Subject,TrialName,TrialNumber,Timestamp,ExperimenterResponse')
                FileData.write('\n')
            break
if Exp:
        mywin=visual.Window([800,600], pos=[0,0], monitor="default",waitBlanking=True,units="pix",color='black',fullscr=False,allowGUI=True)

        # create all stimulus possibility
        max_num = 6 #number of pegs on the screen
        TF_Positions=range(max_num)
        TF_Color=[green,red]
        Audio=sound.Sound(SoundFile,volume=Volume)

        # Loading the Instruction images
        if FirstCondition=='ND':
            IntroFile= os.path.join(folder_path, 'Slide7.png')
        elif FirstCondition == "BI":
            IntroFile= os.path.join(folder_path,'Slide8.png')
        else:
            IntroFile= os.path.join(folder_path,'Slide6.png')

        # loading the instructions if the image does not depend on the condition
        #IntroFile = os.path.join(folder_path, 'instructionscreen_amblyopic.png')

        # Start trials loop
        IntroFiles = [IntroFile] #,IntroFile2,IntroFile3]
        Conditions = [FirstCondition] # ,SecondCondition,ThirdCondition]
        Exit=False
        for i,condition in enumerate(Conditions):
            if Exit:
                break

            ## This part displays the instructions (each image/slide) - INSTRUCTION DISPLAYING STARTS
            print(os.path.join(folder_path, 'Slide1.png'))

            ReGraDTaskIntro=visual.SimpleImageStim(win=mywin,image=os.path.join(folder_path, 'Slide1.png'))
            ReGraDTaskIntro.draw()
            mywin.flip()

            # Wait for Space press
            while True:
                if len(event.getKeys())>0: break

            ReGraDTaskIntro=visual.SimpleImageStim(win=mywin,image=os.path.join(folder_path, 'Slide2.png'))

            ReGraDTaskIntro.draw()
            mywin.flip()

            # Wait for Space press
            while True:
                if len(event.getKeys())>0: break

            ReGraDTaskIntro=visual.SimpleImageStim(win=mywin,image=os.path.join(folder_path, 'Slide3.png'))
            ReGraDTaskIntro.draw()
            mywin.flip()

            # Wait for Space press
            while True:
                if len(event.getKeys())>0: break
            
            ReGraDTaskIntro=visual.SimpleImageStim(win=mywin,image=os.path.join(folder_path, 'Slide4.png'))
            ReGraDTaskIntro.draw()
            mywin.flip()

            # Wait for Space press
            while True:
                if len(event.getKeys())>0: break

            # Display Introduction  
            Intro=visual.SimpleImageStim(win=mywin,image=IntroFiles[i])
            Intro.draw()
            mywin.flip()

            # Wait for Space press
            while True:
                if len(event.getKeys())>0: break

            ## INSTRUCTION DISPLAYING STOPS

            # looping 80 times
            Accuracy=[]
            TrialPosition,TrialName = createTargetFlankerPositions_randomized()
            for trial_num in range(len(TrialName)):
                with open(FileName,"a") as FileData:
                    FileData.write('%s,%s,'%(Study,SbjNumber))
                Color= np.ndarray([1,6,3], dtype=float)
                ind = 0
                # nested for loop for changing the color of target and flanker pins
                for j in range(np.shape(TrialPosition[trial_num])[0]):
                    for k in range(np.shape(TrialPosition[trial_num])[1]):
                        if TrialPosition[trial_num][j][k]==1: #if a trigger, make green
                            Color[0][ind]= green
                        elif TrialPosition[trial_num][j][k]==2: #if a flanker, make red
                            Color[0][ind]= red
                        else:
                            Color[0][ind]= gray
                        ind=ind+1
                Color=Color[0]
                Correctness=onetrial(mywin,R,Center,Color,FileName,trial_num, TrialName[trial_num])

                # TODO: add for loop to append incorrec trials

                if len(event.getKeys(keyList='q'))>0:
                    Exit=True
                    break
                Accuracy.append(Correctness)
                #This if statement plays the end sound at the end of the condition
                if i==len(TrialName): # if all initial trials have been tried
                    Sound2 = sound.Sound(SoundFile_End,volume=Volume) #S
                    Sound2.play()
                    # mywin.flip()
                    Accuracy=np.array(Accuracy)
                    # sums all correct responses
                    ok=(Accuracy==1).sum()
                    total=len(Accuracy)
                    mywin.flip()

                    while True:
                        if len(event.getKeys(keyList='space'))>0:
                            break
                    Accuracy=[]
            # TODO check if it can be cleaned better
            Accuracy=np.array(Accuracy)
            ok=(Accuracy==1).sum()
            total=len(Accuracy)
            
            while True:
                if len(event.getKeys(keyList='space'))>0:
                    break

            EndScreen=visual.TextStim(win=mywin,text="",color=[1,1,1],pos=[0,0],anchorHoriz='center',height=30)
            Sound2 = sound.Sound(SoundFile_End,volume=Volume) #SoundFile_End
            Sound2.play()
            EndScreen.setText('You are done! Congrats!')
            EndScreen.setSize(100)
            EndScreen.draw()
            mywin.flip()
            core.wait(3)
        mywin.flip()
        core.wait(1)
        mywin.close()
