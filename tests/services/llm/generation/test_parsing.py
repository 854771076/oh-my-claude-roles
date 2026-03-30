from src.models import RoleMeta
from src.services.llm.generation.nodes import parse_response

test_role = RoleMeta(
    name="test-role",
    display_name="Test Role",
    description="Test role description",
    category="test",
    version="1.0.0",
    source_hash="abc123",
    source_path="test.md",
)


def test_correct_format_multiple_files():
    content = """
## 文件名: first-command.md

Content of first file.

## 文件名: second-command.md

Content of second file.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 2
    assert components[0].filename == "first-command.md"
    assert components[1].filename == "second-command.md"
    assert "Content of first file" in components[0].content


def test_content_on_same_line_as_filename():
    content = """
## 文件名: test-command.md Here is some extra content that shouldn't be here
This is the actual content.
"""
    components = parse_response("commands", content, test_role)
    # Should clean to just "test-command.md-Here-is-some-extra-content..."
    # OR when it still gets too long, should fallback to test-role.md
    assert len(components) == 1
    # Either we get fallback to test-role.md (ends with .md), or we get the long filename
    # which doesn't end with .md but still captures correct content
    assert "This is the actual content" in components[0].content
    assert "/" not in components[0].filename


def test_filename_with_invalid_characters():
    content = """
## 文件名: my/file:name*.md

File content here.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 1
    # Invalid characters removed: "myfilename.md"
    assert "filename.md" in components[0].filename
    assert "File content here" in components[0].content


def test_filename_with_spaces_converted_to_dashes():
    content = """
## 文件名: my test file.md

Content here.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 1
    assert components[0].filename == "my-test-file.md"


def test_content_captured_as_filename():
    # This is the bug we fixed - LLM didn't put filename on its own line
    # Make it long enough to definitely exceed the 50 character threshold
    content = """
## 文件名: This is the entire first paragraph describing what we're going to generate that should trigger fallback
And this is the actual file content that should be in the file.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 1
    # After cleaning, if still too long (>50), should fallback to default
    assert components[0].filename == "test-role.md"
    assert "And this is the actual file content" in components[0].content


def test_no_filename_header_single_file():
    content = """
This is just the file content with no header at all.
Second line here.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 1
    assert components[0].filename == "test-role.md"
    assert "This is just the file content" in components[0].content


def test_content_before_first_filename():
    content = """
Here is some introduction text before the first file.

## 文件名: first.md
Content one.

## 文件名: second.md
Content two.
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 3
    assert components[1].filename == "first.md"
    assert components[2].filename == "second.md"
    assert "Content one" in components[1].content


def test_empty_filename_falls_back():
    # Entire part is empty after filename header → triggers fallback
    content = """
## 文件名:
"""
    components = parse_response("commands", content, test_role)
    assert len(components) == 1
    assert components[0].filename == "test-role.md"
