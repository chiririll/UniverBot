import json
import os

from Word4Univer import Lab, StudentInfo, Path, TitlePages, LabInfo
from Word4Univer.Word.rels import Image

from .... import Subjects
from . import threads


def get_file(path: str = "") -> str:
    return os.path.join(os.path.dirname(__file__), path)


class Laba6(Lab):

    info = LabInfo(
        name="Лабораторная работа",
        index=6,
        theme="Оценка рисков информационной безопасности по базовым угрозам в сетевой информационной системе",
        subject=Subjects.OIB
    )

    def add_input(self, key: str, value) -> None:
        pass

    def __init__(self, student: StudentInfo, **params):
        with open(get_file("variants.json"), 'r') as f:
            tasks = json.load(f)

        self.task = tasks.get(str(student.variant))

        self.th = []    # Thread type -> PC id -> Thread item
        self.cth = []   # Thread type -> PC id
        self.cthr = []  # PC id
        self.r = []     # PC id
        self.cr = 0

        params['word_params'] = {
            'style': "tstu",
            'parts_folder': get_file("OIB/Laba_6/docparts")
        }

        super().__init__(self.info, student, style=Path.get_src("styles/tstu.xml"))

    def run(self):
        TitlePages.tstu(self.document)
        self.theory()

        self.part_1()
        self.part_2()
        self.part_3()
        self.part_4()
        self.part_5()

    def theory(self):
        style = {
            'width': 266,
            'height': 230
        }
        image = Image(get_file("src/image1.emf"), style=style)
        image.id = self.document.add_relation(image)

        context = {
            'threads': threads.threads,
            'thread_classes': threads.thread_classes,
            'criticality': self.task,
            'image': image
        }
        self.document.add_step('theory', **context)

    def part_1(self):
        def count_th() -> list:
            th = []
            for thread_type in range(len(threads.threads)):
                thread_type_list = []
                for pc in range(len(threads.threads[thread_type])):
                    pc_list = []
                    for item_val in threads.threads[thread_type][pc]:
                        pc_list.append((item_val / 100) * (self.task[thread_type][pc] / 100))
                    thread_type_list.append(pc_list)
                th.append(thread_type_list)
            return th

        self.th = count_th()

        style = {
            'width': 141,
            'height': 48
        }

        context = {
            'func_1': Image(get_file("src/part_1/func_1.wmf"), "p1f1", style),
            'func_2': Image(get_file("src/part_1/func_2.wmf"), "p1f2", style),
            'func_3': Image(get_file("src/part_1/func_3.wmf"), "p1f3", style),

            'thread_classes': threads.thread_classes,
            'th': self.th
        }

        context['func_1'].id = self.document.add_relation(context['func_1'])
        context['func_2'].id = self.document.add_relation(context['func_2'])
        context['func_3'].id = self.document.add_relation(context['func_3'])

        self.document.add_step('part_1', **context)

    def part_2(self):
        def count_cth() -> list:
            cth = []
            for thread_type in self.th:
                thread_type_list = []
                for pc in thread_type:
                    mult = 1
                    for item in pc:
                        mult *= 1 - item
                    thread_type_list.append(1 - mult)
                cth.append(thread_type_list)
            return cth

        self.cth = count_cth()

        style = {
            'width': 179,
            'height': 48
        }

        context = {
            'func_1': Image(get_file("src/part_2/func_1.wmf"), "p2f1", style),
            'func_2': Image(get_file("src/part_2/func_2.wmf"), "p2f2", style),
            'func_3': Image(get_file("src/part_2/func_3.wmf"), "p2f3", style),

            'thread_classes': threads.thread_classes,
            'cth': self.cth
        }

        context['func_1'].id = self.document.add_relation(context['func_1'])
        context['func_2'].id = self.document.add_relation(context['func_2'])
        context['func_3'].id = self.document.add_relation(context['func_3'])

        self.document.add_step('part_2', **context)

    def part_3(self):
        def count_cthr() -> list:
            cthr = [1] * len(threads.threads[0])
            for thread_type in self.cth:
                for i, pc in enumerate(thread_type):
                    cthr[i] *= 1 - pc
            return list(map(lambda x: 1 - x, cthr))

        self.cthr = count_cthr()

        style = {
            'width': 179,
            'height': 55
        }

        context = {
            'func': Image(get_file("src/part_3/func.wmf"), "p3f", style),
            'cthr': self.cthr
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_3', **context)

    def part_4(self):
        def count_r() -> list:
            return [cthr * threads.d[i] for i, cthr in enumerate(self.cthr)]

        self.r = count_r()

        style = {
            'width': 103,
            'height': 20
        }

        context = {
            'func': Image(get_file("src/part_4/func.wmf"), "p4f", style),
            'r': self.r
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_4', **context)

    def part_5(self):
        def count_cr() -> int:
            cr = 1
            for r_i in self.r:
                cr *= 1 - r_i / 100
            return (1 - cr) * 100

        self.cr = count_cr()

        style = {
            'width': 204,
            'height': 60
        }

        context = {
            'func': Image(get_file("src/part_5/func.wmf"), "p5f", style),
            'r': self.r,
            'cr': self.cr
        }

        context['func'].id = self.document.add_relation(context['func'])

        self.document.add_step('part_5', **context)
