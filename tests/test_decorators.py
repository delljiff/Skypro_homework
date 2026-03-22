import pytest
from _pytest.capture import CaptureFixture
from pathlib import Path

from src.decorators import log


# ===== ТЕСТ 1: Логирование в консоль при успехе =====
def test_log_console_success(capsys: CaptureFixture[str]) -> None:
    @log()
    def add(a: int, b: int) -> int:
        return a + b

    add(2, 3)
    captured: CaptureFixture[str].CaptureResult = capsys.readouterr()
    assert captured.out.strip() == "add ok"


# ===== ТЕСТ 2: Логирование в консоль при ошибке =====
def test_log_console_error(capsys: CaptureFixture[str]) -> None:
    @log()
    def div(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(10, 0)

    captured: CaptureFixture[str].CaptureResult = capsys.readouterr()
    assert "div error: ZeroDivisionError. Inputs: (10, 0), {}" in captured.out


# ===== ТЕСТ 3: Логирование в файл при успехе =====
def test_log_file_success(tmp_path: Path) -> None:
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a: int, b: int) -> int:
        return a + b

    add(2, 3)

    content: str = log_file.read_text().strip()
    assert content == "add ok"


# ===== ТЕСТ 4: Логирование в файл при ошибке =====
def test_log_file_error(tmp_path: Path) -> None:
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def div(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(10, 0)

    content: str = log_file.read_text().strip()
    assert "div error: ZeroDivisionError. Inputs: (10, 0), {}" in content


# ===== ТЕСТ 5: Несколько вызовов дописываются в файл =====
def test_log_file_append(tmp_path: Path) -> None:
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a: int, b: int) -> int:
        return a + b

    add(1, 2)
    add(3, 4)

    lines: list[str] = log_file.read_text().strip().split("\n")
    assert lines[0] == "add ok"
    assert lines[1] == "add ok"
    assert len(lines) == 2
