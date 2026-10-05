"""funcraft 的领域异常定义。"""


class FunCraftError(Exception):
    """funcraft 所有自定义异常的基类。"""


class CellBuildNotImplementedError(FunCraftError, NotImplementedError):
    """`Cell` 子类未实现 `_build` 时抛出。

    `Cell.build()` 会委托给子类的 `_build()` 完成实际建造逻辑；直接使用基类
    `Cell`（而不是 `Wall`/`Line`/`River` 等具体子类）时会触发该异常。
    """

    def __init__(self, cell: object) -> None:
        super().__init__(
            f"{type(cell).__name__} 未实现 _build()，无法执行 build()；"
            "请使用 Wall/Line/River 等具体子类，或自行实现 _build()。"
        )
