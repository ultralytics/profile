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
            # Build cProfile command based on command type
            if command[0] in ['python', 'python3'] or command[0].endswith('python'):
                # Direct python calls: python -m cProfile script.py
                profile_cmd = [command[0], '-m', 'cProfile', '-o', stats_file] + command[1:]
                result = subprocess.run(profile_cmd, capture_output=True, text=True, timeout=300)
            else:
                # CLI tools: Find the actual Python entry point and profile it
                try:
                    # Try to find the script location
                    which_result = subprocess.run(['which', command[0]], capture_output=True, text=True)
                    if which_result.returncode == 0:
                        script_path = which_result.stdout.strip()
                        # Check if it's a Python script
                        with open(script_path, 'r') as f:
                            first_line = f.readline()
                        
                        if 'python' in first_line:
                            # Profile the script directly
                            profile_cmd = [sys.executable, '-m', 'cProfile', '-o', stats_file, script_path] + command[1:]
                        else:
                            # Not a Python script, fall back to subprocess timing
                            return self._profile_bash_command(command)
                    else:
                        # Command not found, fall back to subprocess timing
                        return self._profile_bash_command(command)
                        
                except Exception:
                    # Any error, fall back to subprocess timing
                    return self._profile_bash_command(command)
                    
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
            
            # Skip all built-ins and low-level functions
            if filename.startswith('<') or filename.startswith('~'):
                continue
            
            # Skip imports, module loading, and initialization overhead
            skip_patterns = [
                '<module>', '__import__', '_handle_fromlist', 'get_code', '_find_and_load',
                '_jit_internal', 'lazy', '_dynamo', '_ops', 'triton_kernel', 
                'importlib', 'marshal', 'compile_bytecode', '__build_class__',
                'create_dynamic', 'open_code', 'genexpr'
            ]
            if any(pattern in func_name or pattern in filename for pattern in skip_patterns):
                continue
                
            # Only keep meaningful functions with some execution time
            if cumulative_time < 0.001:
                continue
                
            # Create meaningful function key with module path
            if 'ultralytics' in filename:
                # Extract ultralytics module structure
                parts = filename.split('ultralytics/')[-1].split('/')
                if len(parts) > 1:
                    module_path = '.'.join(parts[:-1])
                    key = f"ultralytics.{module_path}.{Path(filename).stem}:{func_name}:{line_num}"
                else:
                    key = f"ultralytics.{Path(filename).stem}:{func_name}:{line_num}"
            elif 'torch' in filename and 'site-packages' in filename:
                # Only show torch forward/compute functions
                if not any(keyword in func_name.lower() for keyword in 
                          ['forward', '__call__', 'conv', 'relu', 'pool', 'norm', 'activation']):
                    continue
                torch_part = filename.split('torch/')[-1].split('/')[0]
                key = f"torch.{torch_part}.{Path(filename).stem}:{func_name}:{line_num}"
            elif any(pkg in filename for pkg in ['numpy', 'cv2', 'PIL', 'torchvision']):
                # Other important packages doing actual work
                pkg_name = next(pkg for pkg in ['numpy', 'cv2', 'PIL', 'torchvision'] if pkg in filename)
                if cumulative_time < 0.005:  # Higher threshold for external packages
                    continue
                key = f"{pkg_name}.{Path(filename).stem}:{func_name}:{line_num}"
            else:
                # User scripts and other files
                key = f"{Path(filename).stem}:{func_name}:{line_num}"
            
            # Prioritize ultralytics functions
            is_ultralytics = 'ultralytics' in filename
            
            timings[key] = {
                "cumulative_time": cumulative_time,
                "total_time": total_time,
                "call_count": call_count,
                "avg_time": cumulative_time / call_count if call_count > 0 else 0,
                "filename": filename,
                "is_ultralytics": is_ultralytics,
            }

        # Sort by ultralytics functions first, then by cumulative time
        return dict(sorted(timings.items(), 
                          key=lambda x: (not x[1].get("is_ultralytics", False), -x[1]["cumulative_time"])))

    def analyze_performance(self, timings: Dict, output: str, top_n: int = 10):
        """Analyze and report performance bottlenecks."""
        print(f"=== Execution Results ===\n{output}\n")
        
        if not timings:
            print("No timing data available")
            return

        print(f"=== Performance Analysis ===\n")

        # Top functions by cumulative time
        print(f"⏱️  TOP {top_n} SLOWEST FUNCTIONS (Cumulative Time):")
        print(f"{'Function':<60} {'Cum Time':<8} {'Self Time':<8} {'Calls':<6} {'Avg':<8}")
        print("-" * 95)

        for i, (func_key, data) in enumerate(timings.items()):
            if i >= top_n:
                break
            # Truncate long function names
            display_key = func_key if len(func_key) <= 60 else func_key[:57] + "..."
            print(f"{display_key:<60} {data['cumulative_time']:<8.3f} {data['total_time']:<8.3f} {data['call_count']:<6} {data['avg_time']:<8.5f}")

        # Most called functions
        most_called = sorted(timings.items(), key=lambda x: x[1]["call_count"], reverse=True)[:top_n]
        print(f"\n🔥 MOST CALLED FUNCTIONS:")
        print(f"{'Function':<60} {'Calls':<6} {'Self Time':<8} {'Avg':<8}")
        print("-" * 85)

        for func_key, data in most_called:
            display_key = func_key if len(func_key) <= 60 else func_key[:57] + "..."
            print(f"{display_key:<60} {data['call_count']:<6} {data['total_time']:<8.3f} {data['avg_time']:<8.5f}")

        # Functions by self time (time spent in function itself, not subfunctions)
        by_self_time = sorted(timings.items(), key=lambda x: x[1]["total_time"], reverse=True)[:top_n]
        print(f"\n🔍 TOP {top_n} BY SELF TIME (Excluding Subfunctions):")
        print(f"{'Function':<60} {'Self Time':<8} {'Cum Time':<8} {'Calls':<6} {'Self %':<6}")
        print("-" * 95)

        for func_key, data in by_self_time:
            if data['cumulative_time'] > 0:
                self_percent = (data['total_time'] / data['cumulative_time']) * 100
            else:
                self_percent = 0
            display_key = func_key if len(func_key) <= 60 else func_key[:57] + "..."
            print(f"{display_key:<60} {data['total_time']:<8.3f} {data['cumulative_time']:<8.3f} {data['call_count']:<6} {self_percent:<6.1f}")


def profile_command(command: str, top_n: int = 20) -> Dict:
    """Profile any command and display results."""
    profiler = Profiler()
    cmd_list = command.split() if isinstance(command, str) else command
    
    timings, output = profiler.profile_command(cmd_list)
    profiler.analyze_performance(timings, output, top_n)
    
    return timings
