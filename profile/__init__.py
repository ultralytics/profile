"""Profile - A tool for profiling any Python code or command."""

__version__ = "0.1.0"

from .profiler import Profiler, profile_command

__all__ = ["Profiler", "profile_command"]
