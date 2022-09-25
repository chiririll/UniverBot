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

    # TODO: add index for more button

    @staticmethod
    def get_subjects(start_index: int = 0) -> list[SubjectInfo]:
        return Labs.__subjects[start_index:]

    @staticmethod
    def get_labs(subject: SubjectInfo = None) -> list[Lab]:
        if subject is None:
            return Labs.__labs

        return [lab for lab in Labs.__labs if lab.get_subject().name == subject.name]
