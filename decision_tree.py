"""
Python code generated through Amua
Model name: Reproductive Health Access in Nigeria
Model type: Decision Tree
Simulation type: Cohort
"""

import math
import numpy as np

# Construct a node
class Node:
    "Tree Node class"
    name=""
    prob=0
    costCost=0
    costEfectiveness=0
    payoffCost=0
    payoffEfectiveness=0
    expectedCost=0
    expectedEfectiveness=0

    def __init__(self, nodeType):
        self.nodeType=nodeType #The node types are 0=Decision, 1=Chance, 2=Terminal
        self.children=[]       #List of children
    def addNode(self, name, nodeType, prob, costCost, costEfectiveness, payoffCost, payoffEfectiveness):
        child=Node(nodeType)
        child.name=name
        child.nodeType=nodeType
        child.prob=prob
        child.costCost=costCost
        child.costEfectiveness=costEfectiveness
        child.payoffCost=payoffCost
        child.payoffEfectiveness=payoffEfectiveness
        self.children.append(child)
        return(child)


#Recursively roll back tree
def runTree(curNode):
    #Get expected value of node
    numChildren=len(curNode.children)
    if(numChildren==0): 
        curNode.expectedCost=curNode.payoffCost+curNode.costCost
        curNode.expectedEfectiveness=curNode.payoffEfectiveness+curNode.costEfectiveness
    #Get expected value of children
    else: 
        curNode.expectedCost=curNode.costCost
        curNode.expectedEfectiveness=curNode.costEfectiveness
        for child in curNode.children:
            runTree(child)
            curNode.expectedCost+=(child.prob*child.expectedCost)
            curNode.expectedEfectiveness+=(child.prob*child.expectedEfectiveness)
    return;

#Recursively display results
def displayResults(curNode):
    for child in curNode.children:
        print(child.name,child.expectedCost,child.expectedEfectiveness,sep="	")
        displayResults(child)
    return;

#Define parameters with value and distribution
qEctopic=0.87 #Expression: Unif(0.74, 1.0, ~)
qIndAbort=0.96 #Expression: Unif(0.92, 1.0, ~)
qComp=0.88 #Expression: Unif(0.76, 1.0, ~)
qMiscarriage=0.94 #Expression: Unif(0.88, 1.0, ~)
qUnintendedBirth=0.74 #Expression: Unif(0.48, 1.0, ~)
qStillBirth=0.9199999999999999 #Expression: Unif(0.84, 1.0, ~)
pSQno=0.533 #Expression: Beta (15504.97, 13585.03, ~) 
pSQtrad=0.13 #Expression: Beta (3781.7, 25308.3, ~) 
pSQshort=0.09 #Expression: Beta (2618.1, 26471.9, ~) 
pSQlong=0.247 #Expression: Beta (7185.23, 21904.77, ~) 
pAllShort=0.267 #Expression: Beta (7767.03, 21322.97, ~) 
pAllLong=0.733 #Expression: Beta (21322.97, 7767.03, ~)
pFail_Trad=0.17501148369315572 #Expression: Beta (7239, 34124, ~)
pFail_Short=0.06300316708169136 #Expression: Beta (2606, 38757, ~) 
pFail_Long=0.029011435340763485 #Expression: Beta (1200, 40163, ~) 
pEctopic=0.011122460560662809 #Expression: Beta (98, 8713, ~) 
pIndAbort=0.5589999741744561 #Expression: Beta (5151566, 4064116,~) 
pComp=0.39799995268933974 #Expression: Beta (3667841, 5547841, ~) 
pMiscarriage=0.12000001736171018 #Expression: Beta (1105882, 8109800, ~)
pStillBirth=0.08514492753623189 #Expression: Beta (94, 1010, ~) 
cEctopic=1044.052248 #Expression: Gamma (118.266, 8.828, ~) 
cIndAbort=312.0 #Expression: Gamma (16, 19.5, ~) 
cComp=141.0 #Expression: Gamma (16, 8.8125, ~) 
cMiscarriage=415.0 #Expression: Gamma (16, 25.9375, ~) 
cBirth=24.0 #Expression: Gamma (16, 1.5, ~) 
cStillBirth=30.0 #Expression: Gamma (16, 1.875, ~) 
qNoPregnancy=1.0 #Expression: 1.0
pHalfNo=0.267 #Expression: Beta (7767.03, 21322.97, ~) 
pHalfTrad=0.13 #Expression: Beta (3781.7, 25308.3, ~) 
pHalfShort=0.161 #Expression: Beta (4683.49, 24406.51, ~) 
pHalfLong=0.442 #Expression: Beta (12857.78, 16232.22, ~) 
cIntAll=6.48 #Expression: Gamma (16, 0.405, ~) 
cIntHalf=5.74 #Expression: Gamma (16, 0.35875, ~) 
pShort_Long=0.247 #Expression: Beta (7185.23, 21904.77, ~) 
cIntShort=3.72 #Expression: Gamma (16, 0.2325, ~) 
pCont=0.31 #Expression: Beta (2856861.42, 6358820.58, ~) 

#Define tree
Root=Node(1) #Root decision node
SQ=Root.addNode("SQ",1,0,0,0,0,0)
NoContraception=SQ.addNode("NoContraception",1,pSQno/(pSQno+pSQtrad+pSQshort+pSQlong),0,0,0,0)
EctopicPregnancy2=NoContraception.addNode("EctopicPregnancy2",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic,qEctopic)
InducedAbortion2=NoContraception.addNode("InducedAbortion2",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications2=InducedAbortion2.addNode("Complications2",2,pComp,0,0,cIndAbort+cComp,qIndAbort*qComp)
NoComplications2=InducedAbortion2.addNode("NoComplications2",2,-1,0,0,cIndAbort,qIndAbort)
SpontAbortFetalLoss2=NoContraception.addNode("SpontAbortFetalLoss2",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage,qMiscarriage)
ContinuedPregnancy2=NoContraception.addNode("ContinuedPregnancy2",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth2=ContinuedPregnancy2.addNode("LiveBirth2",2,-1,0,0,cBirth,qUnintendedBirth)
StillBirth2=ContinuedPregnancy2.addNode("StillBirth2",2,pStillBirth,0,0,cStillBirth,qStillBirth)
TraditionalMethods=SQ.addNode("TraditionalMethods",1,pSQtrad/(pSQno+pSQtrad+pSQshort+pSQlong),0,0,0,0)
ContraceptiveFailure1=TraditionalMethods.addNode("ContraceptiveFailure1",1,pFail_Trad,0,0,0,0)
EctopicPregnancy1=ContraceptiveFailure1.addNode("EctopicPregnancy1",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic,qEctopic)
InducedAbortion1=ContraceptiveFailure1.addNode("InducedAbortion1",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications1=InducedAbortion1.addNode("Complications1",2,pComp,0,0,cIndAbort+cComp,qIndAbort*qComp)
NoComplications1=InducedAbortion1.addNode("NoComplications1",2,-1,0,0,cIndAbort,qIndAbort)
SpontAbortFetalLoss1=ContraceptiveFailure1.addNode("SpontAbortFetalLoss1",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage,qMiscarriage)
ContinuedPregnancy1=ContraceptiveFailure1.addNode("ContinuedPregnancy1",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth1=ContinuedPregnancy1.addNode("LiveBirth1",2,-1,0,0,cBirth,qUnintendedBirth)
StillBirth1=ContinuedPregnancy1.addNode("StillBirth1",2,pStillBirth,0,0,cStillBirth,qStillBirth)
NoContraceptiveFailure1=TraditionalMethods.addNode("NoContraceptiveFailure1",2,-1,0,0,0,qNoPregnancy)
Short_minusTermMethods=SQ.addNode("Short_minusTermMethods",1,pSQshort/(pSQno+pSQtrad+pSQshort+pSQlong),0,0,0,0)
ContraceptiveFailure=Short_minusTermMethods.addNode("ContraceptiveFailure",1,pFail_Short,0,0,0,0)
EctopicPregnancy=ContraceptiveFailure.addNode("EctopicPregnancy",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic,qEctopic)
InducedAbortion=ContraceptiveFailure.addNode("InducedAbortion",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications=InducedAbortion.addNode("Complications",2,pComp,0,0,cIndAbort+cComp,qIndAbort*qComp)
NoComplications=InducedAbortion.addNode("NoComplications",2,-1,0,0,cIndAbort,qIndAbort)
SpontAbortFetalLoss=ContraceptiveFailure.addNode("SpontAbortFetalLoss",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage,qMiscarriage)
ContinuedPregnancy=ContraceptiveFailure.addNode("ContinuedPregnancy",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth=ContinuedPregnancy.addNode("LiveBirth",2,-1,0,0,cBirth,qUnintendedBirth)
StillBirth=ContinuedPregnancy.addNode("StillBirth",2,pStillBirth,0,0,cStillBirth,qStillBirth)
NoContraceptiveFailure=Short_minusTermMethods.addNode("NoContraceptiveFailure",2,-1,0,0,0,qNoPregnancy)
Long_minusActingMethods=SQ.addNode("Long_minusActingMethods",1,pSQlong/(pSQno+pSQtrad+pSQshort+pSQlong),0,0,0,0)
ContraceptiveFailure2=Long_minusActingMethods.addNode("ContraceptiveFailure2",1,pFail_Long,0,0,0,0)
EctopicPregnancy3=ContraceptiveFailure2.addNode("EctopicPregnancy3",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic,qEctopic)
InducedAbortion3=ContraceptiveFailure2.addNode("InducedAbortion3",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications3=InducedAbortion3.addNode("Complications3",2,pComp,0,0,cIndAbort+cComp,qIndAbort*qComp)
NoComplications3=InducedAbortion3.addNode("NoComplications3",2,-1,0,0,cIndAbort,qIndAbort)
SpontAbortFetalLoss3=ContraceptiveFailure2.addNode("SpontAbortFetalLoss3",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage,qMiscarriage)
ContinuedPregnancy3=ContraceptiveFailure2.addNode("ContinuedPregnancy3",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth3=ContinuedPregnancy3.addNode("LiveBirth3",2,-1,0,0,cBirth,qUnintendedBirth)
StillBirth3=ContinuedPregnancy3.addNode("StillBirth3",2,pStillBirth,0,0,cStillBirth,qStillBirth)
NoContraceptiveFailure2=Long_minusActingMethods.addNode("NoContraceptiveFailure2",2,-1,0,0,0,qNoPregnancy)
ProvideLong=Root.addNode("ProvideLong",1,0,0,0,0,0)
ContraceptiveFailure6=ProvideLong.addNode("ContraceptiveFailure6",1,pFail_Long,0,0,0,0)
EctopicPregnancy8=ContraceptiveFailure6.addNode("EctopicPregnancy8",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic+cIntAll,qEctopic)
InducedAbortion8=ContraceptiveFailure6.addNode("InducedAbortion8",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications8=InducedAbortion8.addNode("Complications8",2,pComp,0,0,cIndAbort+cComp+cIntAll,qIndAbort*qComp)
NoComplications8=InducedAbortion8.addNode("NoComplications8",2,-1,0,0,cIndAbort+cIntAll,qIndAbort)
SpontAbortFetalLoss8=ContraceptiveFailure6.addNode("SpontAbortFetalLoss8",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage+cIntAll,qMiscarriage)
ContinuedPregnancy8=ContraceptiveFailure6.addNode("ContinuedPregnancy8",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth8=ContinuedPregnancy8.addNode("LiveBirth8",2,-1,0,0,cBirth+cIntAll,qUnintendedBirth)
StillBirth8=ContinuedPregnancy8.addNode("StillBirth8",2,pStillBirth,0,0,cStillBirth+cIntAll,qStillBirth)
NoContraceptiveFailure6=ProvideLong.addNode("NoContraceptiveFailure6",2,-1,0,0,cIntAll,qNoPregnancy)
HalfCoverage=Root.addNode("HalfCoverage",1,0,0,0,0,0)
NoContraception1=HalfCoverage.addNode("NoContraception1",1,pHalfNo/(pHalfNo+pHalfTrad+pHalfShort+pHalfLong),0,0,0,0)
EctopicPregnancy6=NoContraception1.addNode("EctopicPregnancy6",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic+cIntHalf,qEctopic)
InducedAbortion6=NoContraception1.addNode("InducedAbortion6",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications6=InducedAbortion6.addNode("Complications6",2,pComp,0,0,cIndAbort+cComp+cIntHalf,qIndAbort*qComp)
NoComplications6=InducedAbortion6.addNode("NoComplications6",2,-1,0,0,cIndAbort+cIntHalf,qIndAbort)
SpontAbortFetalLoss6=NoContraception1.addNode("SpontAbortFetalLoss6",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage+cIntHalf,qMiscarriage)
ContinuedPregnancy6=NoContraception1.addNode("ContinuedPregnancy6",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth6=ContinuedPregnancy6.addNode("LiveBirth6",2,-1,0,0,cBirth+cIntHalf,qUnintendedBirth)
StillBirth6=ContinuedPregnancy6.addNode("StillBirth6",2,pStillBirth,0,0,cStillBirth+cIntHalf,qStillBirth)
TraditionalMethods1=HalfCoverage.addNode("TraditionalMethods1",1,pHalfTrad/(pHalfNo+pHalfTrad+pHalfShort+pHalfLong),0,0,0,0)
ContraceptiveFailure5=TraditionalMethods1.addNode("ContraceptiveFailure5",1,pFail_Trad,0,0,0,0)
EctopicPregnancy7=ContraceptiveFailure5.addNode("EctopicPregnancy7",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic+cIntHalf,qEctopic)
InducedAbortion7=ContraceptiveFailure5.addNode("InducedAbortion7",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications7=InducedAbortion7.addNode("Complications7",2,pComp,0,0,cIndAbort+cComp+cIntHalf,qIndAbort*qComp)
NoComplications7=InducedAbortion7.addNode("NoComplications7",2,-1,0,0,cIndAbort+cIntHalf,qIndAbort)
SpontAbortFetalLoss7=ContraceptiveFailure5.addNode("SpontAbortFetalLoss7",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage+cIntHalf,qMiscarriage)
ContinuedPregnancy7=ContraceptiveFailure5.addNode("ContinuedPregnancy7",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth7=ContinuedPregnancy7.addNode("LiveBirth7",2,-1,0,0,cBirth+cIntHalf,qUnintendedBirth)
StillBirth7=ContinuedPregnancy7.addNode("StillBirth7",2,pStillBirth,0,0,cStillBirth+cIntHalf,qStillBirth)
NoContraceptiveFailure5=TraditionalMethods1.addNode("NoContraceptiveFailure5",2,-1,0,0,cIntHalf,qNoPregnancy)
Short_minusTermMethods1=HalfCoverage.addNode("Short_minusTermMethods1",1,pHalfShort/(pHalfNo+pHalfTrad+pHalfShort+pHalfLong),0,0,0,0)
ContraceptiveFailure3=Short_minusTermMethods1.addNode("ContraceptiveFailure3",1,pFail_Short,0,0,0,0)
EctopicPregnancy4=ContraceptiveFailure3.addNode("EctopicPregnancy4",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic+cIntHalf,qEctopic)
InducedAbortion4=ContraceptiveFailure3.addNode("InducedAbortion4",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications4=InducedAbortion4.addNode("Complications4",2,pComp,0,0,cIndAbort+cComp+cIntHalf,qIndAbort*qComp)
NoComplications4=InducedAbortion4.addNode("NoComplications4",2,-1,0,0,cIndAbort+cIntHalf,qIndAbort)
SpontAbortFetalLoss4=ContraceptiveFailure3.addNode("SpontAbortFetalLoss4",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage+cIntHalf,qMiscarriage)
ContinuedPregnancy4=ContraceptiveFailure3.addNode("ContinuedPregnancy4",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth4=ContinuedPregnancy4.addNode("LiveBirth4",2,-1,0,0,cBirth+cIntHalf,qUnintendedBirth)
StillBirth4=ContinuedPregnancy4.addNode("StillBirth4",2,pStillBirth,0,0,cStillBirth+cIntHalf,qStillBirth)
NoContraceptiveFailure3=Short_minusTermMethods1.addNode("NoContraceptiveFailure3",2,-1,0,0,cIntHalf,qNoPregnancy)
Long_minusActingMethods1=HalfCoverage.addNode("Long_minusActingMethods1",1,pHalfLong/(pHalfNo+pHalfTrad+pHalfShort+pHalfLong),0,0,0,0)
ContraceptiveFailure4=Long_minusActingMethods1.addNode("ContraceptiveFailure4",1,pFail_Long,0,0,0,0)
EctopicPregnancy5=ContraceptiveFailure4.addNode("EctopicPregnancy5",2,pEctopic,0,0,cEctopic+cIntHalf,qEctopic)
InducedAbortion5=ContraceptiveFailure4.addNode("InducedAbortion5",1,pIndAbort,0,0,0,0)
Complications5=InducedAbortion5.addNode("Complications5",2,pComp,0,0,cIndAbort+cComp+cIntHalf,qIndAbort*qComp)
NoComplications5=InducedAbortion5.addNode("NoComplications5",2,-1,0,0,cIndAbort+cIntHalf,qIndAbort)
SpontAbortFetalLoss5=ContraceptiveFailure4.addNode("SpontAbortFetalLoss5",2,pMiscarriage,0,0,cMiscarriage+cIntHalf,qMiscarriage)
ContinuedPregnancy5=ContraceptiveFailure4.addNode("ContinuedPregnancy5",1,-1,0,0,0,0)
LiveBirth5=ContinuedPregnancy5.addNode("LiveBirth5",2,-1,0,0,cBirth+cIntHalf,qUnintendedBirth)
StillBirth5=ContinuedPregnancy5.addNode("StillBirth5",2,pStillBirth,0,0,cStillBirth+cIntHalf,qStillBirth)
NoContraceptiveFailure4=Long_minusActingMethods1.addNode("NoContraceptiveFailure4",2,-1,0,0,cIntHalf,qNoPregnancy)
ProvideShort=Root.addNode("ProvideShort",1,0,0,0,0,0)
Short_minusTermMethods2=ProvideShort.addNode("Short_minusTermMethods2",1,-1,0,0,0,0)
ContraceptiveFailure7=Short_minusTermMethods2.addNode("ContraceptiveFailure7",1,pFail_Short,0,0,0,0)
EctopicPregnancy9=ContraceptiveFailure7.addNode("EctopicPregnancy9",2,pEctopic,0,0,cEctopic+cIntShort,qEctopic)
InducedAbortion9=ContraceptiveFailure7.addNode("InducedAbortion9",1,pIndAbort,0,0,0,0)
Complications9=InducedAbortion9.addNode("Complications9",2,pComp,0,0,cIndAbort+cComp+cIntShort,qIndAbort*qComp)
NoComplications9=InducedAbortion9.addNode("NoComplications9",2,-1,0,0,cIndAbort+cIntShort,qIndAbort)
SpontAbortFetalLoss9=ContraceptiveFailure7.addNode("SpontAbortFetalLoss9",2,pMiscarriage,0,0,cMiscarriage+cIntShort,qMiscarriage)
ContinuedPregnancy9=ContraceptiveFailure7.addNode("ContinuedPregnancy9",1,-1,0,0,0,0)
LiveBirth9=ContinuedPregnancy9.addNode("LiveBirth9",2,-1,0,0,cBirth+cIntShort,qUnintendedBirth)
StillBirth9=ContinuedPregnancy9.addNode("StillBirth9",2,pStillBirth,0,0,cStillBirth+cIntShort,qStillBirth)
NoContraceptiveFailure7=Short_minusTermMethods2.addNode("NoContraceptiveFailure7",2,-1,0,0,cIntShort,qNoPregnancy)
Long_minusActingMethods2=ProvideShort.addNode("Long_minusActingMethods2",1,pShort_Long,0,0,0,0)
NoContraceptiveFailure8=Long_minusActingMethods2.addNode("NoContraceptiveFailure8",2,-1,0,0,cIntShort,qNoPregnancy)
ContraceptiveFailure8=Long_minusActingMethods2.addNode("ContraceptiveFailure8",1,pFail_Long,0,0,0,0)
EctopicPregnancy10=ContraceptiveFailure8.addNode("EctopicPregnancy10",2,pEctopic/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cEctopic+cIntShort,qEctopic)
InducedAbortion10=ContraceptiveFailure8.addNode("InducedAbortion10",1,pIndAbort/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
Complications10=InducedAbortion10.addNode("Complications10",2,pComp,0,0,cIndAbort+cComp+cIntShort,qIndAbort*qComp)
NoComplications10=InducedAbortion10.addNode("NoComplications10",2,-1,0,0,cIndAbort+cIntShort,qIndAbort)
SpontAbortFetalLoss10=ContraceptiveFailure8.addNode("SpontAbortFetalLoss10",2,pMiscarriage/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,cMiscarriage+cIntShort,qMiscarriage)
ContinuedPregnancy10=ContraceptiveFailure8.addNode("ContinuedPregnancy10",1,pCont/(pEctopic+pIndAbort+pMiscarriage+pCont),0,0,0,0)
LiveBirth10=ContinuedPregnancy10.addNode("LiveBirth10",2,-1,0,0,cBirth+cIntShort,qUnintendedBirth)
StillBirth10=ContinuedPregnancy10.addNode("StillBirth10",2,pStillBirth,0,0,cStillBirth+cIntShort,qStillBirth)

#Define complementary probabilities
NoContraceptiveFailure.prob=1.0-ContraceptiveFailure.prob
LiveBirth.prob=1.0-StillBirth.prob
NoComplications.prob=1.0-Complications.prob
NoComplications1.prob=1.0-Complications1.prob
LiveBirth1.prob=1.0-StillBirth1.prob
NoContraceptiveFailure1.prob=1.0-ContraceptiveFailure1.prob
NoComplications2.prob=1.0-Complications2.prob
LiveBirth2.prob=1.0-StillBirth2.prob
NoComplications3.prob=1.0-Complications3.prob
LiveBirth3.prob=1.0-StillBirth3.prob
NoContraceptiveFailure2.prob=1.0-ContraceptiveFailure2.prob
NoComplications4.prob=1.0-Complications4.prob
LiveBirth4.prob=1.0-StillBirth4.prob
NoContraceptiveFailure3.prob=1.0-ContraceptiveFailure3.prob
NoComplications5.prob=1.0-Complications5.prob
ContinuedPregnancy5.prob=1.0-EctopicPregnancy5.prob-InducedAbortion5.prob-SpontAbortFetalLoss5.prob
LiveBirth5.prob=1.0-StillBirth5.prob
NoContraceptiveFailure4.prob=1.0-ContraceptiveFailure4.prob
NoComplications6.prob=1.0-Complications6.prob
LiveBirth6.prob=1.0-StillBirth6.prob
NoComplications7.prob=1.0-Complications7.prob
LiveBirth7.prob=1.0-StillBirth7.prob
NoContraceptiveFailure5.prob=1.0-ContraceptiveFailure5.prob
NoComplications8.prob=1.0-Complications8.prob
LiveBirth8.prob=1.0-StillBirth8.prob
NoContraceptiveFailure6.prob=1.0-ContraceptiveFailure6.prob
Short_minusTermMethods2.prob=1.0-Long_minusActingMethods2.prob
NoComplications9.prob=1.0-Complications9.prob
ContinuedPregnancy9.prob=1.0-EctopicPregnancy9.prob-InducedAbortion9.prob-SpontAbortFetalLoss9.prob
LiveBirth9.prob=1.0-StillBirth9.prob
NoContraceptiveFailure7.prob=1.0-ContraceptiveFailure7.prob
NoComplications10.prob=1.0-Complications10.prob
LiveBirth10.prob=1.0-StillBirth10.prob
NoContraceptiveFailure8.prob=1.0-ContraceptiveFailure8.prob

#Run tree
runTree(Root)

#Display output for each strategy
for child in Root.children:
    print("Strategy:",child.name)
    print("EV ($):",child.expectedCost,"EV (QALY):",child.expectedEfectiveness)
    print("Children...")
    print("Name	EV($)	EV(QALY)")
    displayResults(child)
    print("") #Blank
