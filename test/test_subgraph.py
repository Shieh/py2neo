#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2015, Nigel Small
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


from py2neo import Subgraph, Node, Path, Relationship
from test.util import Py2neoTestCase


class SubgraphTestCase(Py2neoTestCase):
        
    def test_empty_subgraph(self):
        s = Subgraph()
        assert len(s) == 0
        assert s.order == 0
        assert s.size == 0
        assert not s.__bool__()
        assert not s.__nonzero__()
        assert "" not in s
        assert not s.bound
        
    def test_subgraph_with_single_node(self):
        a = Node(name="Alice")
        s = Subgraph(a)
        assert len(s) == 0
        assert s.order == 1
        assert s.size == 0
        assert not s.__bool__()
        assert not s.__nonzero__()
        assert list(s) == []
        assert a in s
        assert Node() not in s
        assert not s.bound
        
    def test_subgraph_with_single_relationship(self):
        r = Relationship({"name": "Alice"}, "KNOWS", {"name": "Bob"})
        s = Subgraph(r)
        assert len(s) == 1
        assert s.order == 2
        assert s.size == 1
        assert s.__bool__()
        assert s.__nonzero__()
        assert list(s) == [r]
        assert r in s
        assert Relationship({}, "", {}) not in s
        assert not s.bound
        
    def test_subgraph_with_single_path(self):
        s = Subgraph(Path({"name": "Alice"}, "KNOWS", {"name": "Bob"}))
        assert len(s) == 1
        assert s.order == 2
        assert s.size == 1
        assert s.__bool__()
        assert s.__nonzero__()
        assert not s.bound
        
    def test_subgraph_from_other_subgraph(self):
        s = Subgraph(Path({"name": "Alice"}, "KNOWS", {"name": "Bob"}))
        t = Subgraph(s)
        assert len(t) == 1
        assert t.order == 2
        assert t.size == 1
        assert s.__bool__()
        assert s.__nonzero__()
        assert not s.bound
        
    def test_subgraph_equality(self):
        alice = Node("Person", name="Alice")
        bob = Node("Person", name="Bob")
        s1 = Subgraph(Path(alice, "KNOWS", bob))
        s2 = Subgraph(Path(alice, "KNOWS", bob))
        assert s1 == s2
        assert hash(s1) == hash(s2)
        
    def test_subgraph_inequality(self):
        s1 = Subgraph(Path({"name": "Alice"}, "KNOWS", {"name": "Bob"}))
        s2 = Subgraph(Path({"name": "Alice"}, "KNOWS", {"name": "Robert"}))
        assert s1 != s2
        assert s1 != ""
        
    def test_converting_cypher_results_to_subgraph(self):
        r = self.cypher.execute(
            "CREATE (a {name:'Alice'})-[ab:KNOWS]->(b {name:'Bob'}) RETURN a, ab, b")
        a, ab, b = r[0]
        s = r.to_subgraph()
        assert s.graph is self.graph
        assert s.service_root is self.graph.service_root
        assert len(s) == 1
        assert s.order == 2
        assert s.size == 1
        assert a in s
        assert ab in s
        assert b in s
        assert s.bound
        assert self.graph.exists(s)
        self.graph.delete(ab)
        assert not self.graph.exists(s)
        s.unbind()
        assert not s.bound
        s.unbind()
        assert not s.bound
    
    def test_subgraph_add(self):
        s = Subgraph()
        assert len(s) == 0
        assert s.order == 0
        assert s.size == 0
        assert not s.__bool__()
        assert not s.__nonzero__()
        assert not s.bound
        s.add(Path({"name": "Alice"}, "KNOWS", {"name": "Bob"}))
        assert len(s) == 1
        assert s.order == 2
        assert s.size == 1
        assert s.__bool__()
        assert s.__nonzero__()
        assert not s.bound

    def test_subgraph_repr(self):
        alice = Node("Person", name="Alice")
        subgraph = Subgraph(alice)
        assert repr(subgraph) == "<Subgraph order=1 size=0>"
