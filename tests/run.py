"""Run Dev Instincts' own tests: one line per test, PASS or FAIL, then why each failure failed.

Called by tools/check.sh. Exits 1 if any test fails or none is found.
"""

import importlib
import inspect
import os
import sys
import traceback
import unittest

sys.dont_write_bytecode = True  # no __pycache__ in the repo
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Garrett's order (Task 6, 2026-11-02); a test file not listed here runs after these.
ORDER = ["test_ledger", "test_stats", "test_sanitizer", "test_sync_check", "test_control",
         "test_readme"]


def sentence(test):
    """A test's name is its docstring's first line, or its method name in words."""
    return test.shortDescription() or str(test).split(" ")[0].removeprefix("test_").replace("_", " ")


def why(err):
    kind, value, tb = err
    if issubclass(kind, AssertionError):
        return str(value)
    here = [f for f in traceback.extract_tb(tb) if f.filename.startswith(HERE)]
    where = f" (at {os.path.basename(here[-1].filename)}:{here[-1].lineno})" if here else ""
    return "".join(traceback.format_exception_only(kind, value)).strip() + where


class Result(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.lines, self.failed = 0, []

    def show(self, status, test, err=None):
        self.lines += 1
        print(f"{status}  {sentence(test)}", flush=True)
        if err is not None:
            self.failed.append((sentence(test), why(err)))

    def addSuccess(self, test):
        super().addSuccess(test)
        self.show("PASS", test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.show("FAIL", test, err)

    def addError(self, test, err):
        super().addError(test, err)
        self.show("FAIL", test, err)

    def addSkip(self, test, reason):
        # No test may skip: a check that doesn't run must not read as passed.
        super().addSkip(test, reason)
        self.show("FAIL", test, (AssertionError, AssertionError(f"skipped: {reason}"), None))


def suite():
    names = sorted((f[:-3] for f in os.listdir(HERE) if f.startswith("test_") and f.endswith(".py")),
                   key=lambda n: (ORDER.index(n) if n in ORDER else len(ORDER), n))
    s = unittest.TestSuite()
    for name in names:
        try:
            module = importlib.import_module(name)
        except Exception as e:  # a file that doesn't load is a failed test, not a crash
            def broken(message=f"{type(e).__name__}: {e}"):
                raise AssertionError(message)
            s.addTest(unittest.FunctionTestCase(broken, description=f"tests/{name}.py loads"))
            continue
        # Classes and their tests in the order they are written.
        for cls in [c for c in vars(module).values()
                    if inspect.isclass(c) and issubclass(c, unittest.TestCase) and c.__module__ == name]:
            for attr in vars(cls):
                if attr.startswith("test_") and callable(getattr(cls, attr)):
                    s.addTest(cls(attr))
    return s


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    result = Result()
    suite().run(result)
    if result.failed:
        print()
        print("Why:")
        for name, reason in result.failed:
            print(f"- {name}:")
            for line in reason.splitlines():
                print(f"    {line}")
    print()
    print(f"{result.lines} tests, {len(result.failed)} failed")
    sys.exit(1 if result.failed or not result.lines else 0)


if __name__ == "__main__":
    main()
