# Manual de uso do Simulador MVN (Máquina de Von Neumann)

Atualmente, a estrutura mínima para o funcionamento correto do projeto é a seguinte:

```
|-- simulador-mvn
    |-- README.md
    |-- config
    |   |-- instructions.csv
    |-- src
    |   |-- main.py
    |   |-- lib
    |       |-- __init__.py
    |       |-- assembler.py
    |       |-- loader.py
    |       |-- simulator.py
    |       |-- utils.py
    |-- test
        |-- p1.txt
```

Um vídeo ilustrando o uso do simulador está disponível no site https://sites.google.com/view/2020-pcs3216-8993198.


Para inicializar o simulador, basta entrar na pasta src e rodar o programa main.py com *python 3.7.7*.

```
python3 main.py
```

O programa inicializa o objeto SimuladorMVN definido no script src/lib/simulator.py.

O estado inicial do simulador é "off" e os seguintes comandos estão disponíveis para interação com o usuário:

```
Simulador MVN off
to turn on: on
to exit:    exit
to help:    help
:
```

Quando ligamos o simulador com o comando "on", os seguintes comandos estão disponíveis para interação com o usuário:

```
: on
Simulador MVN on
to print internal status:       status
to print table of mnemonics:    mnemonics
to print assembler status:      assembler
to print loader status:         loader
to load a program:              boot
to run the program in memory:   run
to clear:                       clear
to help:                        help
to turn off:                    off
```

O simulador possui como atributos, entre outros, um objeto Assembler e um objeto Loader. O Assembler se encarrega de montar o código objeto. O Loader é responsável pela execução do programa. Atualmente, o Assembler e Loader são absolutos.

Pode-se consultar a tabela de mnemonicos:

```
: mnemonics
Table of mnemonics
{'ADD': {'class': 'instruction',
         'instruction': 'sum',
         'opcode': '03',
         'optype': 'constant',
         'size': 2},
 'BLOC': {'class': 'pseudo',
          'instruction': 'reserve area',
          'opcode': '',
          'optype': 'constant',
          'size': 1},
 'CALL': {'class': 'instruction',
          'instruction': 'call procedure',
          'opcode': '09',
          'optype': 'address',
          'size': 2},
 'DATA': {'class': 'pseudo',
          'instruction': 'fill memory with constant',
          'opcode': '',
          'optype': 'constant',
          'size': 1},
 'DIV': {'class': 'instruction',
         'instruction': 'divide',
         'opcode': '06',
         'optype': 'constant',
         'size': 2},
 'END': {'class': 'pseudo',
         'instruction': 'physical end of the source code',
         'opcode': '',
         'optype': '',
         'size': 1},
 'JUMP': {'class': 'instruction',
          'instruction': 'jump incondicional',
          'opcode': '00',
          'optype': 'address',
          'size': 2},
 'JUMPN': {'class': 'instruction',
           'instruction': 'jump if negative',
           'opcode': '02',
           'optype': 'address',
           'size': 2},
 'JUMPZ': {'class': 'instruction',
           'instruction': 'jump if zero',
           'opcode': '01',
           'optype': 'address',
           'size': 2},
 'LOAD': {'class': 'instruction',
          'instruction': 'load value',
          'opcode': '07',
          'optype': 'address',
          'size': 2},
 'MUL': {'class': 'instruction',
         'instruction': 'multiply',
         'opcode': '05',
         'optype': 'constant',
         'size': 2},
 'ORG': {'class': 'pseudo',
         'instruction': 'new origin',
         'opcode': '',
         'optype': 'address',
         'size': 1},
 'PD': {'class': 'instruction',
        'instruction': 'print acumulator',
        'opcode': '0E',
        'optype': '',
        'size': 1},
 'READ': {'class': 'instruction',
          'instruction': 'read a byte to the acumulator',
          'opcode': '0C',
          'optype': 'constant',
          'size': 1},
 'RTN': {'class': 'instruction',
         'instruction': 'return from procedure',
         'opcode': '0A',
         'optype': 'address',
         'size': 1},
 'STOP': {'class': 'instruction',
          'instruction': 'stop the program',
          'opcode': '0B',
          'optype': '',
          'size': 1},
 'STORE': {'class': 'instruction',
           'instruction': 'store in memory',
           'opcode': '08',
           'optype': 'address',
           'size': 2},
 'SUB': {'class': 'instruction',
         'instruction': 'subtract',
         'opcode': '04',
         'optype': 'constant',
         'size': 2},
 'WRITE': {'class': 'instruction',
           'instruction': 'write with acumulator byte',
           'opcode': '0D',
           'optype': 'address',
           'size': 1}}
```

Para executar um programa na linguagem simbólica que estamos trabalhando, é preciso carregá-lo com o comando boot, e passar o caminho do programa. Por exemplo, para carregar no simulador o programa em test/p1.txt:

```
: boot 
enter program path: ../test/p1.txt
loading program ../test/p1.txt...
```

Para visualizar o estado do simulador, entre o comando status:

```
: status
Simulator status
state:        program_loaded
ac:           0
ic:           0
simulator_mem:
{500: {'opcode': '07', 'operand': 508},
 502: {'opcode': '0E', 'operand': ''},
 503: {'opcode': '03', 'operand': 3},
 505: {'opcode': '0E', 'operand': ''},
 506: {'opcode': '02', 'operand': 503},
 508: {'opcode': '', 'operand': -10},
 509: {'opcode': '', 'operand': 3},
 'end': 506,
 'origin': 500}
program name: ../test/p1.txt
program:
line 1. :       ORG     500     ; first line of the program
line 2. :       LOAD    X       ; 
line 3. :       PD              ; print acumulator content
line 4. loop:   ADD     Y       ; loop
line 5. :       PD              ; print acumulator content
line 6. :       JUMPN   loop    ; if acumulator is negative, jump to loop
line 7. X:      DATA    -10     ; 
line 8. Y:      DATA    3       ;
line 9. :       END             ; end of the program
```

Pode-se consultar o estado do Assembler com o comando assembler:

```
: assembler
Assembler status
table of symbols:
{'X': {'address': 508, 'at_line': 7, 'defined': True, 'operand': -10},
 'Y': {'address': 509, 'at_line': 8, 'defined': True, 'operand': 3},
 'loop': {'address': 503, 'at_line': 4, 'defined': True, 'operand': 503}}
memory:
{0: {'opcode': '', 'operand': '', 'operand_is_symbol': False},
 500: {'opcode': '07', 'operand': 'X', 'operand_is_symbol': True},
 502: {'opcode': '0E', 'operand': '', 'operand_is_symbol': False},
 503: {'opcode': '03', 'operand': 'Y', 'operand_is_symbol': True},
 505: {'opcode': '0E', 'operand': '', 'operand_is_symbol': False},
 506: {'opcode': '02', 'operand': 'loop', 'operand_is_symbol': True},
 508: {'opcode': '', 'operand': -10, 'operand_is_symbol': False},
 509: {'opcode': '', 'operand': 3, 'operand_is_symbol': False},
 510: {'opcode': '', 'operand': '', 'operand_is_symbol': False}}
object code:
{500: {'opcode': '07', 'operand': 508},
 502: {'opcode': '0E', 'operand': ''},
 503: {'opcode': '03', 'operand': 3},
 505: {'opcode': '0E', 'operand': ''},
 506: {'opcode': '02', 'operand': 503},
 508: {'opcode': '', 'operand': -10},
 509: {'opcode': '', 'operand': 3},
 'end': 506,
 'origin': 500}
```

Pode-se consultar o estado do Loader com o comando loader:

```
: loader
Assembler status
table of symbols:
{'X': {'address': 508, 'at_line': 7, 'defined': True, 'operand': -10},
 'Y': {'address': 509, 'at_line': 8, 'defined': True, 'operand': 3},
 'loop': {'address': 503, 'at_line': 4, 'defined': True, 'operand': 503}}
memory:
{0: {'opcode': '', 'operand': '', 'operand_is_symbol': False},
 500: {'opcode': '07', 'operand': 'X', 'operand_is_symbol': True},
 502: {'opcode': '0E', 'operand': '', 'operand_is_symbol': False},
 503: {'opcode': '03', 'operand': 'Y', 'operand_is_symbol': True},
 505: {'opcode': '0E', 'operand': '', 'operand_is_symbol': False},
 506: {'opcode': '02', 'operand': 'loop', 'operand_is_symbol': True},
 508: {'opcode': '', 'operand': -10, 'operand_is_symbol': False},
 509: {'opcode': '', 'operand': 3, 'operand_is_symbol': False},
 510: {'opcode': '', 'operand': '', 'operand_is_symbol': False}}
object code:
{500: {'opcode': '07', 'operand': 508},
 502: {'opcode': '0E', 'operand': ''},
 503: {'opcode': '03', 'operand': 3},
 505: {'opcode': '0E', 'operand': ''},
 506: {'opcode': '02', 'operand': 503},
 508: {'opcode': '', 'operand': -10},
 509: {'opcode': '', 'operand': 3},
 'end': 506,
 'origin': 500}
------------------------------
: loader
Loader status
memory:
{500: {'opcode': '07', 'operand': 508},
 502: {'opcode': '0E', 'operand': ''},
 503: {'opcode': '03', 'operand': 3},
 505: {'opcode': '0E', 'operand': ''},
 506: {'opcode': '02', 'operand': 503},
 508: {'opcode': '', 'operand': -10},
 509: {'opcode': '', 'operand': 3},
 'end': 506,
 'origin': 500}
```

Para executar o programa, entre o comando run:

```
:run
execute program automatically? (y/n): y
running the program ... 
-10
-7
-4
-1
2
program was executed successfully
```

