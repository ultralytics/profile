import cProfile
import pstats
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Profiler:
    """Profiles any Python command or script execution."""

    def profile_command(self, command: List[str]) -> Tuple[Dict, str]:
        """Profile command execution and return timing data."""
        if self._is_python_command(command):
            return self._profile_python_command(command)
        else:
            return self._profile_bash_command(command)

    def _is_python_command(self, command: List[str]) -> bool:
        """Check if command runs Python code."""
        if not command:
            return False
        
        # Direct python calls
        if command[0] in ['python', 'python3'] or command[0].endswith('python'):
            return True
        
        # Python scripts
        if len(command) == 1 and Path(command[0]).suffix == '.py':
            return True
            
        # Common Python tools that can be profiled
        python_tools = ['yolo', 'pip', 'pytest', 'black', 'flake8']
        return command[0] in python_tools

    def _profile_python_command(self, command: List[str]) -> Tuple[Dict, str]:
        """Profile Python command execution."""
        with tempfile.NamedTemporaryFile(suffix='.stats', delete=False) as tmp:
            stats_file = tmp.name

        try:
            # Build cProfile command
            if command[0] in ['python', 'python3'] or command[0].endswith('python'):
                profile_cmd = [command[0], '-m', 'cProfile', '-o', stats_file] + command[1:]
            else:
                # For tools like yolo, use python -m cProfile -m tool
                profile_cmd = [sys.executable, '-m', 'cProfile', '-o', stats_file, '-m'] + command

            result = subprocess.run(profile_cmd, capture_output=True, text=True, timeout=300)
            output = f"Exit code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

            # Load profile stats
            if Path(stats_file).exists():
                stats = pstats.Stats(stats_file)
                timings = self._extract_timing_data(stats)
            else:
                timings = {}

        except Exception as e:
            output = f"Error: {e}"
            timings = {}
        finally:
            # Clean up
            if Path(stats_file).exists():
                Path(stats_file).unlink()

        return timings, output

    def _profile_bash_command(self, command: List[str]) -> Tuple[Dict, str]:
        """Profile bash command execution with timing."""
        import time
        
        start_time = time.time()
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=300)
            end_time = time.time()
            
            output = f"Exit code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            timings = {
                f"{' '.join(command)}:total_execution:0": {
                    "cumulative_time": end_time - start_time,
                    "total_time": end_time - start_time,
                    "call_count": 1,
                    "avg_time": end_time - start_time,
                    "filename": "bash_command"
                }
            }
        except subprocess.TimeoutExpired:
            output = "Command execution timed out"
            timings = {}
        except Exception as e:
            output = f"Error executing command: {e}"
            timings = {}
            
        return timings, output

    def _extract_timing_data(self, stats: pstats.Stats) -> Dict:
        """Extract timing data from pstats.Stats object."""
        timings = {}

        for func_info, (call_count, _, total_time, cumulative_time, _) in stats.stats.items():
            filename, line_num, func_name = func_info
            
            # Skip built-in functions unless significant time
            if filename.startswith('<') and cumulative_time < 0.001:
                continue
                
            key = f"{Path(filename).name}:{func_name}:{line_num}"
            timings[key] = {
                "cumulative_time": cumulative_time,
                "total_time": total_time,
                "call_count": call_count,
                "avg_time": cumulative_time / call_count if call_count > 0 else 0,
                "filename": filename,
            }

        return dict(sorted(timings.items(), key=lambda x: x[1]["cumulative_time"], reverse=True))

    def analyze_performance(self, timings: Dict, output: str, top_n: int = 10):
        """Analyze and report performance bottlenecks."""
        print(f"=== Execution Results ===\n{output}\n")
        
        if not timings:
            print("No timing data available")
            return

        print(f"=== Performance Analysis ===")

        # Top functions by cumulative time
        print(f"\n⏱️  TOP {top_n} SLOWEST FUNCTIONS:")
        print(f"{'Function':<50} {'Time':<10} {'Calls':<8} {'Avg':<10}")
        print("-" * 80)

        for i, (func_key, data) in enumerate(timings.items()):
            if i >= top_n:
                break
            print(f"{func_key:<50} {data['cumulative_time']:<10.4f} {data['call_count']:<8} {data['avg_time']:<10.6f}")

        # Most called functions
        most_called = sorted(timings.items(), key=lambda x: x[1]["call_count"], reverse=True)[:top_n]
        print(f"\n🔥 MOST CALLED FUNCTIONS:")
        print(f"{'Function':<50} {'Calls':<8} {'Time':<10} {'Avg':<10}")
        print("-" * 80)

        for func_key, data in most_called:
            print(f"{func_key:<50} {data['call_count']:<8} {data['total_time']:<10.4f} {data['avg_time']:<10.6f}")


def profile_command(command: str, top_n: int = 10) -> Dict:
    """Profile any command and display results."""
    profiler = Profiler()
    cmd_list = command.split() if isinstance(command, str) else command
    
    timings, output = profiler.profile_command(cmd_list)
    profiler.analyze_performance(timings, output, top_n)
    
    return timings
