#!/usr/bin/env python
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


from __future__ import division, unicode_literals

from py2neo.batch.core import Batch


class ReadBatch(Batch):
    """ Generic batch execution facility for data read requests,
    """

    def __init__(self, graph):
        Batch.__init__(self, graph)

    def stream(self):
        for result in self.graph.batch.stream(self):
            yield result.content

    def submit(self):
        return [result.content for result in self.graph.batch.submit(self)]
