from pathlib import Path

from django.test.runner import DiscoverRunner


class ProjectDiscoverRunner(DiscoverRunner):
    """Discover tests from the repository root, not its hyphenated folder name."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_level = str(Path(__file__).resolve().parent.parent)

    def build_suite(self, test_labels=None, **kwargs):
        return super().build_suite(test_labels or ['apps', 'config'], **kwargs)
