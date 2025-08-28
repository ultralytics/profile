import pytest
from ultralytics_profile import profile_command, Profiler


def test_profile_command():
    """Test basic profiling functionality."""
    timings = profile_command("python -c 'print(42)'")
    assert isinstance(timings, dict)


def test_profiler_class():
    """Test Profiler class."""
    profiler = Profiler()
    timings, output = profiler.profile_command(["python", "-c", "print('test')"])
    assert isinstance(timings, dict)
    assert "Exit code: 0" in output


def test_python_command_detection():
    """Test Python command detection."""
    profiler = Profiler()
    assert profiler._is_python_command(["python", "script.py"])
    assert profiler._is_python_command(["yolo", "predict"])
    assert not profiler._is_python_command(["ls", "-la"])


def test_bash_command():
    """Test bash command profiling."""
    profiler = Profiler()
    timings, output = profiler.profile_command(["echo", "test"])
    assert isinstance(timings, dict)
    assert "test" in output
