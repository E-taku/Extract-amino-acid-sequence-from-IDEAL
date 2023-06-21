import re

def extractSeqs(ideal_data_path: str):
    aminoSeqs = []
    with open(ideal_data_path) as f:
        for s_line in f:
            if re.search('ideal:IID[0-9]+ <sequence> "[A-Z]+"', s_line) is not None:
                idx_seq = re.findall(r'(IID\d+).*"(\w+)"', s_line)
                aminoSeqs.append(idx_seq)
    return aminoSeqs

def writeSeqsToFile(writeFilePath: str, aminoSeqs: list):
    with open("./data/idealAminoSeqs.txt", "w") as f:
        for l in aminoSeqs:
            acc_number = l[0][0]
            aminoSeq = l[0][1]
            f.write(acc_number + " " + aminoSeq + "\n")

ideal_data_path = './data/ideal-v3.ttl'
writeFilePath = './data/idealAminoSeqs.txt'
aminoSeqs = extractSeqs(ideal_data_path)
writeSeqsToFile(ideal_data_path, aminoSeqs)