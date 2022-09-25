from typing import Type

from word4univer import SubjectInfo, Lab

import UniverLabs


class Labs:
    __subjects = [
        UniverLabs.Subjects.OIB,
        UniverLabs.Subjects.Izobrazhenia,
    ]

    __labs = [
        UniverLabs.Labs.OIB.Laba6
    ]

    @staticmethod
    def get_subjects() -> list[SubjectInfo]:
        return Labs.__subjects

    @staticmethod
    def get_subject(index: int = 0) -> SubjectInfo:
        return Labs.__subjects[index]

    @staticmethod
    def get_labs(subject_id: int) -> list[Type[Lab]]:
        return [lab for lab in Labs.__labs if lab.info.subject.name == Labs.__subjects[subject_id].name]
