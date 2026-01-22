from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class SectionSpec:
    name: str
    keys: List[str]


@dataclass(frozen=True)
class kahoot_to_classroom:

    course: SectionSpec = SectionSpec(
        name="course",
        keys=["course_id"]
    )
    certs: SectionSpec = SectionSpec(
        name="certs",
        keys=["credentials"]
    )
    data: SectionSpec = SectionSpec(
        name="data",
        keys=["student_list"]
    )

    @property
    def required_sections(self) -> List[str]:
        return [self.course.name, self.certs.name, self.data.name]

    @property
    def required_keys(self) -> Dict[str, List[str]]:
        return {
            self.course.name: self.course.keys,
            self.certs.name: self.certs.keys,
            self.data.name: self.data.keys,
        }

    @property
    def student_list_key(self) -> str:
        return self.data.keys[0]
