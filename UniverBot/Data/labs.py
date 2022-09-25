from Word4Univer import SubjectInfo, Lab


class Labs:
    __subjects = [
        SubjectInfo("Subj 1"),
        SubjectInfo("Subj 2"),
        SubjectInfo("Subj 3"),
        SubjectInfo("Subj 4"),
        SubjectInfo("Subj 5"),
        SubjectInfo("Subj 6"),
        SubjectInfo("Subj 7"),
        SubjectInfo("Subj 8"),
        SubjectInfo("Subj 9"),
        SubjectInfo("Subj 10"),
        SubjectInfo("Subj 11"),
        SubjectInfo("Subj 12"),
        SubjectInfo("Subj 13"),
        SubjectInfo("Subj 14"),
        SubjectInfo("Subj 15"),
        SubjectInfo("Subj 16"),
        SubjectInfo("Subj 17"),
        SubjectInfo("Subj 18"),
        SubjectInfo("Subj 19"),
    ]

    __labs = [

    ]

    @staticmethod
    def get_subjects() -> list[SubjectInfo]:
        return Labs.__subjects

    @staticmethod
    def get_subject(index: int = 0) -> SubjectInfo:
        return Labs.__subjects[index]

    @staticmethod
    def get_labs(subject_id: int) -> list[Lab]:
        return [lab for lab in Labs.__labs if lab.get_subject().name == Labs.__subjects[subject_id].name]
