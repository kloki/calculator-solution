# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""
from concurrent import futures

import grpc

from . import calculator_pb2, calculator_pb2_grpc
from .solver import solve


class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def SolveStream(self, request_iterator, context):
        for calculation in request_iterator:
            print(f"Processing '{calculation.calculation}'")
            solvable, solution = solve(calculation.calculation)
            yield calculator_pb2.Solution(solvable=solvable, solution=solution)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
