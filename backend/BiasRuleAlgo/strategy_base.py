from typing import List
from dataclasses import dataclass
import abc


@dataclass
class BiasStrategyOutput:
    """
    BiasStrategyOutput is a dataclass that represents the output of a bias strategy evaluation.
    """

    strategy: str
    score: int
    evidence: List[str]


class BiasStrategy(abc.ABC):
    """
    Base Class for all strategies for the RBA.
    """

    @abc.abstractmethod
    def analyse(self, text: str) -> BiasStrategyOutput:
        """
        Analyse the given text and return a BiasStrategyOutput object.

        Args:
            text (str): The text to be analysed.
        """
