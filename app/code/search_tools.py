from typing import List, Any


class SearchTool:
    def __init__(self, index):
        self.index = index

    def search(self, query: str) -> List[Any]:
        """
        Perform a text-based search on the data engineering notes index.

        Args:
            query (str): The search query string.

        Returns:
            List[Any]: A list of up to 5 matching notes.
        """
        return self.index.search(query, num_results=5)