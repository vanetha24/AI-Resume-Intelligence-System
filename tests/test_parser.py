from pathlib import Path

from src.parser import (
    extract_resume_text,
    extract_text_from_pdf,
    extract_text_from_docx
)


def test_parser_module_imports():

    assert callable(
        extract_resume_text
    )

    assert callable(
        extract_text_from_pdf
    )

    assert callable(
        extract_text_from_docx
    )


def test_unsupported_file_format():

    fake_file = Path(
        "example.txt"
    )

    try:

        extract_resume_text(
            str(fake_file)
        )

        assert False, (
            "Expected ValueError "
            "for unsupported file format"
        )

    except ValueError as error:

        assert (
            "Unsupported file format"
            in str(error)
        )