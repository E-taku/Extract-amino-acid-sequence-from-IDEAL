import re
import os
import bisect

def extractSeqs(ideal_data_path: str):
    aminoSeqs = []
    with open(ideal_data_path) as f:
        for s_line in f:
            if re.search('ideal:IID[0-9]+ <sequence> "[A-Z]+"', s_line) is not None:
                idx_seq = re.findall(r'(IID\d+).*"(\w+)"', s_line)
                aminoSeqs.append(idx_seq)
    return aminoSeqs

# remove all amino acids
def writeSeqsToFile(writeFilePath: str, aminoSeqs: list):
    with open("./data/idealAminoSeqs.txt", "w") as f:
        for l in aminoSeqs:
            acc_number = l[0][0]
            aminoSeq = l[0][1]
            f.write(acc_number + " " + aminoSeq + "\n")

def writeSeqsCutByLengthToFile(residuesNum: int):
    allAminoSeqsInfo = []
    maxSeqLength = 0
    with open("./data/idealAminoSeqs.txt", "r") as f:
        for s_line in f:
            acc, aminoSeq = s_line.rstrip().split()
            allAminoSeqsInfo.append([acc, aminoSeq])
            maxSeqLength = max(maxSeqLength, len(aminoSeq))

    cutLengthList = [i * residuesNum for i in range((maxSeqLength // residuesNum)+2)]
    for acc, seq in allAminoSeqsInfo:
        seqLenfth = len(seq)
        idx = bisect.bisect_left(cutLengthList, seqLenfth)
        dirname = "./data/every{}/".format(residuesNum)
        if not(os.path.exists(dirname)):
            os.mkdir(dirname)
        # bisect_leftなので左準拠
        dirname = "./data/every{}/{}~{}/".format(residuesNum, cutLengthList[idx-1], cutLengthList[idx])
        if not(os.path.exists(dirname)):
            os.mkdir(dirname)
        filePath = "{}{}~{}.txt".format(dirname, cutLengthList[idx-1], cutLengthList[idx])
        with open(filePath, mode='a') as f:
            f.write(acc + " " + seq + "\n")
    return allAminoSeqsInfo

ideal_data_path = './data/ideal-v3.ttl'
writeFilePath = './data/idealAminoSeqs.txt'
aminoSeqs = extractSeqs(ideal_data_path)
writeSeqsToFile(ideal_data_path, aminoSeqs)
writeSeqsCutByLengthToFile(100)
