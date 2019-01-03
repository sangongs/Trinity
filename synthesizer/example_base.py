from typing import Callable, NamedTuple, List, Any
from .synthesizer import Synthesizer
from interpreter import Interpreter
from enumerator import Enumerator
from .result import ok, bad

Example = NamedTuple('Example', [
    ('input', List[Any]),
    ('output', Any)])


class ExampleSynthesizer(Synthesizer):
    _examples: List[Example]
    _equal_output: Callable[[Any, Any], bool]

    def __init__(self,
                 enumerator: Enumerator,
                 interpreter: Interpreter,
                 examples: List[Example],
                 equal_output: Callable[[Any, Any], bool] = lambda x, y: x == y):
        super().__init__(enumerator, interpreter)
        if len(examples) == 0:
            raise ValueError(
                'ExampleSynthesizer cannot take an empty list of examples')
        self._examples = examples
        self._equal_output = equal_output

    def get_failed_examples(self, prog):
        '''
        Test the program on all examples provided.
        Return a list of failed examples.
        '''
        return list(filter(
            lambda x: not self._equal_output(
                self.interpreter.eval(prog, x.input), x.output),
            self._examples
        ))

    def analyze(self, prog):
        '''
        This basic version of analyze() merely interpret the AST and see if it conforms to our examples
        '''
        failed_examples = self.get_failed_examples(prog)
        if len(failed_examples) == 0:
            return ok()
        else:
            return bad(why=None)
