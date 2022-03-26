ADDA = 1
ADDB = 2
MOVA = 3
MOVB = 4
SUBA = 5
SUBB = 6
CMPA = 7
CMPB = 8
JZ = 9
JNZ = 10


class MicroProcessor:

    def __init__(self):
        # registers
        self.reg_a = 0
        self.reg_b = 0
        # flags
        self.zero = True
        # memory
        self.mem = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # app (program)
        self.app = []
        # program counter
        self.pc = 0

    def move_in_a(self, i):
        self.reg_a = i
        self.zero = True if 0 == self.reg_a else False
        self.pc += 2
        print('Move', i, ' in a, zero flag', self.zero)

    def move_in_b(self, i):
        self.reg_b = i
        self.zero = True if 0 == self.reg_b else False
        self.pc += 2
        print('Move', i, ' in b, zero flag:', self.zero)

    def add_to_a(self, i):
        self.reg_a += i
        self.zero = True if 0 == self.reg_a else False
        self.pc += 2
        print('Add', i, ' to a:', self.reg_a, ', zero flag:', self.zero)

    def add_to_b(self, i):
        self.reg_b += i
        self.zero = True if 0 == self.reg_b else False
        self.pc += 2
        print('Add', i, ' to b:', self.reg_b, ', zero flag:', self.zero)

    def cmp_to_a(self, i):
        self.zero = True if i == self.reg_a else False
        self.pc += 2
        print('Compare', i, ' to a:', self.reg_a, ', zero flag:', self.zero)

    def cmp_to_b(self, i):
        self.zero = True if i == self.reg_b else False
        self.pc += 2
        print('Compare', i, ' to b:', self.reg_b, ', zero flag:', self.zero)

    def jump_zero(self, relative):
        if self.zero:
            self.pc += relative
            # self.pc += 2
            print('Jump', relative, ' to PC:', self.pc, ', zero flag:', self.zero)
        else:
            self.pc += 2

    def jump_non_zero(self, relative):
        if not self.zero:
            self.pc += relative
            # self.pc += 2
            print('Jump', relative, ' to PC:', self.pc, ', zero flag:', self.zero)
        else:
            self.pc += 2

    def info(self):
        # debug info
        # * unpacks the array
        print('Mem:', *self.mem, 'App:', *self.app)
        print('a', self.reg_a, 'b', self.reg_b, 'pc', self.pc, 'zero', self.zero)

    def run(self, app):
        self.app = app
        self.pc = 0  # start at begin
        self.info()

        while 0 <= self.pc < len(self.app):

            instruction = self.app[self.pc]
            argument = self.app[self.pc + 1]

            if instruction == 0:
                pass
            elif instruction == ADDA:
                self.add_to_a(argument)
            elif instruction == ADDB:
                self.add_to_b(argument)
            elif instruction == MOVA:
                self.move_in_a(argument)
            elif instruction == MOVB:
                self.move_in_b(argument)
            elif instruction == SUBA:
                self.add_to_a(-argument)
            elif instruction == SUBB:
                self.add_to_b(-argument)
            elif instruction == CMPA:
                self.cmp_to_a(argument)
            elif instruction == CMPB:
                self.cmp_to_b(argument)
            elif instruction == JZ:
                self.jump_zero(argument)
            elif instruction == JNZ:
                self.jump_non_zero(argument)
            else:
                # NOP
                pass
                self.pc += 2
        self.info()


if __name__ == '__main__':
    up = MicroProcessor()

    # This basically multiplies 5 times 5 into register B
    up.run([
        ADDA, 1,
        ADDB, 5,
        CMPA, 5,
        JNZ, -6
    ])
