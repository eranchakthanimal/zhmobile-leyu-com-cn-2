from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    description: str
    tags: List[str] = field(default_factory=list)
    url: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "description": self.description,
            "tags": self.tags,
            "url": self.url,
            "created_at": self.created_at,
        }

    def formatted_output(self, include_url: bool = True) -> str:
        lines = [
            f"关键词：{self.keyword}",
            f"描述：{self.description}",
            f"标签：{', '.join(self.tags) if self.tags else '无'}",
        ]
        if include_url and self.url:
            lines.append(f"关联链接：{self.url}")
        lines.append(f"创建时间：{self.created_at}")
        return "\n".join(lines)


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag.lower() in [t.lower() for t in n.tags]]

    def list_all_formatted(self, include_url: bool = True) -> str:
        if not self.notes:
            return "暂无笔记记录。"
        separator = "\n" + "-" * 40 + "\n"
        return separator.join(note.formatted_output(include_url) for note in self.notes)

    def to_dict_list(self) -> List[dict]:
        return [note.to_dict() for note in self.notes]


def build_sample_collection() -> KeywordNoteCollection:
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="乐鱼体育",
        description="乐鱼体育是一家综合体育赛事平台，提供多种竞技项目实时数据与资讯。",
        tags=["体育", "赛事", "资讯"],
        url="https://zhmobile-leyu.com.cn",
    )

    note2 = KeywordNote(
        keyword="篮球直播",
        description="提供NBA、CBA等国内外篮球赛事直播与回放服务。",
        tags=["篮球", "直播", "体育"],
        url="https://zhmobile-leyu.com.cn",
    )

    note3 = KeywordNote(
        keyword="足球比分",
        description="实时更新全球足球赛事比分，覆盖五大联赛及杯赛。",
        tags=["足球", "比分", "体育"],
    )

    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)
    return collection


if __name__ == "__main__":
    sample = build_sample_collection()
    print("=== 全部笔记 ===")
    print(sample.list_all_formatted())
    print("\n=== 搜索关键词 '乐鱼体育' ===")
    for note in sample.find_by_keyword("乐鱼体育"):
        print(note.formatted_output())
    print("\n=== 搜索标签 '体育' ===")
    for note in sample.find_by_tag("体育"):
        print(note.formatted_output())