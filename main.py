import random

def printifyInstruction(instr, mcs):
    """
    Construct a preaty representation of the instruction in memory.
    mcs -> 'maximum characters span'
    """
    return "({0:{3}d}, {1:{3}d}, {2:{3}d})".format(instr['A'], instr['B'], instr['C'], mcs)

class Orbis:
    def __init__(self, gSize):
        self.pc = 0
        self.instructions = []
        self.gsize = gSize

        for i in range(gSize * 3):
            if (i % 3) != 2:
                # We are either on operand A or operand B initialization branch.
                self.instructions.append(random.randrange(0, gSize * 3))
            else:
                # We are on the address C initialization branch.
                self.instructions.append(random.randrange(0, gSize) * 3)

    def shock(self):
        self.pc = 0
        for g in range(self.gsize):
            print "Evaluating gene {0} ...".format(self.pc / 3)
            ta = self.instructions[g * 3]
            tb = self.instructions[g * 3 + 1]
            tc = self.instructions[g * 3 + 2]
           
            cstem = self.instructions[tb] - self.instructions[ta]
            if (tb % 3) == 2:
                # We will affect the jump part of a gene. Make sure it remains consistent with the rest of the genes
                cvtor = cstem % 3
                prevtc = self.instructions[tb]
                if cvtor == 0:
                    # The current value is a valid gene address. It's Ok to use it
                    self.instructions[tb] = cstem  % (self.gsize * 3)
                elif cvtor == 1:
                    # The current value is closer to the lower side
                    self.instructions[tb] = (cstem - 1) % (self.gsize * 3)
                else:
                    # The current value is closer to the upper side
                    self.instructions[tb] = (cstem + 1)  % (self.gsize * 3)
            else:
                # We are in the data domain. Just ensure that the resulting numerals are bounded to the current information domain
                self.instructions[tb] = cstem % (self.gsize * 3)

            if self.instructions[tb] >= self.gsize * 3:
                raise IndexError("Invalid C address generated! Previous C value was {0} while cvtor was {1}".format(prevtc, cvtor))    

            if self.instructions[tb] <= tc:
                self.pc = tc
            else:
                self.pc = self.pc + 3

    def getInstruction(self, addr):
        if addr >= (self.gsize * 3) or (addr % 3) != 0:
            raise Exception("The address supplied is not valid!")
        
        return {'A': self.instructions[addr], 'B': self.instructions[addr + 1], 'C': self.instructions[addr + 2]}

    def __str__(self):
        orbisPrintString = ""
        instrRealAddress = 0
        maxGeneCharPrintCount = len(str(len(self.instructions)))

        for i in range(self.gsize):
            orbisPrintString = orbisPrintString + '{0:{3}d}. [{1:{3}d}] {2}\n'.format(i, i * 3, printifyInstruction(self.getInstruction(i * 3), maxGeneCharPrintCount), maxGeneCharPrintCount)
            instrRealAddress += 3
        return orbisPrintString

if __name__ == "__main__":
    x = Orbis(256)
    print 'Original orbis: \n', x
    print 'Shocking the world...'
    for i in range(100):
        print "Shock nr. {0} ...".format(i)
        try:
            x.shock()
        except IndexError as e:
            print "IndexError message received! World evaluation halted."
            print "Exception message: {0}".format(e.args)
            print x
            exit()
        print x
        
