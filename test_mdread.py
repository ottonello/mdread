import importlib.machinery
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).parent
loader = importlib.machinery.SourceFileLoader("mdread", str(HERE / "mdread"))
spec = importlib.util.spec_from_loader("mdread", loader)
mdread = importlib.util.module_from_spec(spec)
loader.exec_module(mdread)

SAMPLE = "# One\n\ntext\n\n## Two\n\n```python\nprint(1)\n```\n"


@pytest.mark.asyncio
async def test_toc_toggle():
    app = mdread.MdRead(SAMPLE, None)
    async with app.run_test() as pilot:
        v = app.viewer
        assert v.show_table_of_contents
        await pilot.press("t")
        assert not v.show_table_of_contents
        await pilot.press("t")
        assert v.show_table_of_contents
