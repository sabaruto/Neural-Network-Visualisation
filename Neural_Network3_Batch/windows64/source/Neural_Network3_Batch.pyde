layoutMatrix = []
layoutValues = []
plainMatrix = []
Bias = []
Synapse = []

class Matrix:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.Values = []
        for i in range(self.row):
            self.Values.append([])
            for j in range(self.col):
                self.Values[i].append(random(-1, 1))
    def Add(self, num):
        MatrixNew = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] += num
        return MatrixNew
    
    def Multiply(self, num):
        MatrixNew = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] = self.Values[i][j]*num
        return MatrixNew
    def AddMatrix(self, matrix):
        MatrixNew = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] = self.Values[i][j] + matrix.Values[i][j]
        return MatrixNew
    
    def MinusMatrix(self, matrix):
        MatrixNew = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] = self.Values[i][j] - matrix.Values[i][j]
        return MatrixNew
    def DotMatrix(self, matrix):
        MatrixNew = 0
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] = self.Values[i][j]*matrix.Values[i][j]
        return MatrixNew
    
    def MultiplyMatrix(self, matrix):
        MatrixNew = Matrix(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][j] = self.Values[i][j]*matrix.Values[i][j]
        return MatrixNew
    
    def MultMatrix(self, matrix):
        MatrixNew = Matrix(self.row, matrix.col)
        temp = 0
        for i in range(self.row):
            for j in range(matrix.col):
                for k in range(self.col):
                    temp += self.Values[i][k]*matrix.Values[k][j]
                MatrixNew.Values[i][j] = temp
                temp = 0
        return MatrixNew
        
    def T(self):
        MatrixNew = Matrix(self.col, self.row)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[j][i] = self.Values[i][j]
        return MatrixNew
    
    def Shrink(self):
        MatrixNew = Matrix(self.row, 1)
        for i in range(self.row):
            for j in range(self.col):
                MatrixNew.Values[i][0] += self.Values[i][j]
        return MatrixNew

class neuron:
    def __init__(self, x, y, Value):
        self.x = x;
        self.y = y;
        self.Value = Value;
        ellipse(self.x, self.y, 20, 20)
    def Draw(self):
        ellipse(self.x, self.y, 20, 20)
        textFont(f, 8)
        fill(0)
        textAlign(CENTER)
        text(self.Value,self.x, self.y+3)

# def DataRule(RuleSize, Size):
#     AnsOutput = createWriter("Ans.txt")
#     DatOutput = createWriter("Data.txt")
#     wrong = False
#     Data = []
#     Answer = []
#     temp = 0
#     for i in range(Size):
#         Data.append([])
#         Answer.append([])
#         for j in range(RuleSize):
#             Data[i].append(int(round(random(1))))
#     for i in range(len(Data)):
#         if sum(Data[i]) > RuleSize/2:
#             Answer[i].append(1)
#             Answer[i].append(0)
#         else:
#             Answer[i].append(0)
#             Answer[i].append(1)
#     AnsOutput.print(Answer)
#     DatOutput.print(Data)
#     AnsOutput.close()
#     DatOutput.close()

def DataReader(document):
    dataInput = createReader(document)
    Data = dataInput.readLine()
    dataList = []
    datapoint = 0
    for data in range(len(Data)):
        if Data[data] == '[' and (data > 0):
            dataList.append([])
        elif Data[data] == ']':
            datapoint += 1
        elif Data[data] == '0':
            dataList[datapoint].append(0)
        elif Data[data] == '1':
            dataList[datapoint].append(1)
    return dataList

def Arrange(layout):
    global layoutMatrix, layoutValues, plainMatrix, Bias, f, Synapse
    for i in range(len(layout)):
        layoutMatrix.append([])
        plainMatrix.append(Matrix(layout[i], 1))
        layoutValues.append(Matrix(layout[i], 1))
        Bias.append(Matrix(layout[i], 1))
        for j in range(layout[i]):
            layoutValues[i].Values[j][0] = random(-5, 5)
            Bias[i].Values[j][0] = random(-5, 5)
            if layout[i] == 1:
                layoutMatrix[i].append(neuron((600/(len(layout)-1))*i+60, 240, layoutValues[i].Values[j][0]))
            else:
                layoutMatrix[i].append(neuron((600/(len(layout)-1))*i+60, (400/(layout[i]-1))*j+40, layoutValues[i].Values[j][0]))
    for i in range(len(layout)-1):
        Synapse.append(Matrix(layout[i+1], layout[i]))
    
def DrawLines():
    for i in range(len(Synapse)):
        for j in range(Synapse[i].col):
            for k in range(Synapse[i].row):
                colorMode(HSB, 1)
                stroke(1/(1+exp(Synapse[i].Values[k][j])), 0.5, 0.5)
                line(layoutMatrix[i][j].x, layoutMatrix[i][j].y, layoutMatrix[i+1][k].x, layoutMatrix[i+1][k].y)
                colorMode(RGB, 255)
    
    
def sigmoid(x):
    MatrixNew = Matrix(x.row, x.col)
    for i in range(len(x.Values)):
        for j in range(len(x.Values[i])):
            MatrixNew.Values[i][j] = 1/(1+exp(-x.Values[i][j]))
    return MatrixNew

def sigmoidDiff(x):
    MatrixNew = Matrix(x.row, x.col)
    for i in range(len(x.Values)):
        for j in range(len(x.Values[i])):
            MatrixNew.Values[i][j] = exp(-x.Values[i][j])/sq(1+exp(-x.Values[i][j]))
    return MatrixNew

def ValuesToNodes():
    for i in range(len(layoutMatrix)):
        for j in range(len(layoutMatrix[i])):
            layoutMatrix[i][j].Value = layoutValues[i].Values[j][0]

def Calculate(Input):
    for i in range(len(layoutMatrix[0])):
        layoutMatrix[0][i].Value = Input[i]
        layoutValues[0].Values[i][0] = layoutMatrix[0][i].Value
    for i in range(len(layoutMatrix)-1):
        plainMatrix[i+1] = Synapse[i].MultMatrix(layoutValues[i]).AddMatrix(Bias[i+1])
        layoutValues[i+1] = sigmoid(plainMatrix[i+1])
    ValuesToNodes()
    return layoutValues[len(layoutValues)-1]

def Backpropograte(Input, Output, rate, batch):
    global x
    dZ = []
    dNode = []
    dBias = []
    TBias = []
    dSynapse = []
    TSynapse = []
    error = []
    cost = 0
    if batch > len(Input):
        batch = len(Input)
    for i in range(len(layoutValues)):
        dZ.append(layoutValues[i].Multiply(0))
        dNode.append(layoutValues[i].Multiply(0))
        dBias.append(layoutValues[i].Multiply(0))
        TBias.append(layoutValues[i].Multiply(0))
        if i != 0:
            dSynapse.append(Synapse[i-1].Multiply(0))
            TSynapse.append(Synapse[i-1].Multiply(0))
    for i in range(batch):
        for j in range(len(layoutValues[len(layoutMatrix)-1].Values)):
            Val = Calculate(Input[x]).Values[j][0]-Output[x][j]
            cost += sq(Val)/batch
        x = (x+1)%len(Input)
    x = (x-batch)%len(Input)
    for i in range(batch):
        for j in range(len(layoutValues[len(layoutMatrix)-1].Values)):
            Val = Calculate(Input[x]).Values[j][0]-Output[x][j]
            if i == 0:
                error.append([Val])
            else:
                error[j][0] = Val
        for j in range(len(layoutValues)):
            iter = len(layoutValues)-1-j
            if j == 0:
                dNode[iter].Values = error
            else:
                dNode[iter] = Synapse[iter].T().MultMatrix(dBias[iter+1])
            dZ[iter] = sigmoidDiff(plainMatrix[iter])
            dBias[iter] = dZ[iter].MultiplyMatrix(dNode[iter])
            TBias[iter] = TBias[iter].AddMatrix(dBias[iter])
            if iter != 0:
                dSynapse[iter-1] = dBias[iter].MultMatrix(layoutValues[iter-1].T())
                TSynapse[iter-1] = TSynapse[iter-1].AddMatrix(dSynapse[iter-1])
        x = (x+1)%len(Input)
    for i in range(len(layoutValues)):
        Bias[i] = Bias[i].MinusMatrix(TBias[i].Multiply(rate*cost/batch))
        if i != 0:
            Synapse[i-1] = Synapse[i-1].MinusMatrix(TSynapse[i-1].Multiply(rate*cost/batch))
            temp = []
    textFont(f,16)
    text(cost, 720/2, 460)
    #text(aveErr, 720/2, 475)
def setup():
    global f, Synapse, layoutValues, plainMatrix, running, Data, Ans, x
    x = 0
    running = True
    size(720, 480)
    frameRate(60)
    f = createFont("Arial", 16)
    Data = DataReader("data/Data.txt")
    Ans = DataReader("data/Ans.txt")
    Arrange([len(Data[0]), 5, 4, len(Ans[0])])
    DrawLines()
    
def draw():
    global Data, Ans
    background(50)
    Backpropograte(Data,Ans, 1, 50)
    data = [Data,Ans]
    r = int(round(random(len(data[0])-1)))
    Calculate(data[0][r])
    DrawLines()
    for i in range(len(layoutMatrix)):
        for j in range(len(layoutMatrix[i])):
            fill(255-Bias[i].Values[j][0])
            layoutMatrix[i][j].Draw()
    
def mousePressed():
    global running
    if running == True:
        running = False
        noLoop()
    else:
        running = True
        loop()
