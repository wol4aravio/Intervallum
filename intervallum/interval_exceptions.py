class IntervalExceptions:
    class WrongBoundsException(Exception):
        def __init__(self, received_lb: float, received_ub: float):
            super().__init__(f"Improper interval [{received_lb}; {received_ub}]")

    class OperationIsNotDefined(Exception):
        def __init__(self, operation: str, i: "Interval"):
            super().__init__(f"Can not perform operation {operation}({i})")
