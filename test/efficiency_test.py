#/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011-2014, Nigel Small
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


import logging

from py2neo import Graph


class TestHandler(logging.Handler):

    def __init__(self, counter, level):
        super(TestHandler, self).__init__(level)
        self.counter = counter
        self.counter.responses = []

    def emit(self, record):
        if record.msg.startswith("<<<"):
            self.counter.responses.append(record.args)


class HTTPCounter(object):

    handler = None
    logger = logging.getLogger("httpstream")
    responses = []

    def __enter__(self):
        self.handler = TestHandler(self, logging.INFO)
        self.logger.addHandler(self.handler)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handler = None

    @property
    def response_count(self):
        return len(self.responses)


def test_repeated_graph_creation_needs_no_extra_responses():
    graph = Graph()
    _ = graph.neo4j_version
    with HTTPCounter() as counter:
        _ = Graph()
        assert counter.response_count == 0


def test_merge_needs_one_response(graph):
    if not graph.supports_node_labels:
        return
    _ = graph.neo4j_version
    with HTTPCounter() as counter:
        count = 0
        for node in graph.merge("Person", "name", "Alice"):
            assert "Person" in node.labels
            assert node.properties["name"] == "Alice"
            count += 1
        assert counter.response_count == 1


def test_find_needs_one_response(graph):
    if not graph.supports_node_labels:
        return
    _ = graph.neo4j_version
    graph.merge("Person", "name", "Alice")
    with HTTPCounter() as counter:
        count = 0
        for node in graph.find("Person", "name", "Alice"):
            assert "Person" in node.labels
            assert node.properties["name"] == "Alice"
            count += 1
        assert counter.response_count == 1
