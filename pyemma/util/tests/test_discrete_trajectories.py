
# This file is part of PyEMMA.
#
# Copyright (c) 2015, 2014 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


r"""This module contains unit tests for the trajectory module

.. moduleauthor:: B.Trendelkamp-Schroer <benjamin DOT trendelkamp-schroer AT fu-berlin DOT de>

"""

from __future__ import absolute_import

import sys
import os
import sys
import unittest
import pkg_resources
import numpy as np


import pyemma.util.discrete_trajectories as dt

testpath = pkg_resources.resource_filename(__name__, 'data') + os.path.sep


class TestReadDiscreteTrajectory(unittest.TestCase):

    def setUp(self):
        self.filename = testpath +'dtraj.dat'

    def tearDown(self):
        pass

    def test_read_discrete_trajectory(self):
        dtraj_np=np.loadtxt(self.filename, dtype=int)
        dtraj=dt.read_discrete_trajectory(self.filename)
        self.assertTrue(np.all(dtraj_np==dtraj))

class TestWriteDiscreteTrajectory(unittest.TestCase):
    def setUp(self):
        self.filename=testpath +'out_dtraj.dat'
        self.dtraj=np.arange(10000)

    def tearDown(self):
        os.remove(self.filename)

    def test_write_discrete_trajectory(self):
        dt.write_discrete_trajectory(self.filename, self.dtraj)
        dtraj_n=np.loadtxt(self.filename)
        self.assertTrue(np.all(dtraj_n==self.dtraj))

class TestLoadDiscreteTrajectory(unittest.TestCase):

    def setUp(self):
        self.filename=testpath +'dtraj.npy'

    def tearDown(self):
        pass

    def test_load_discrete_trajectory(self):
        dtraj_n=np.load(self.filename)
        dtraj=dt.load_discrete_trajectory(self.filename)
        self.assertTrue(np.all(dtraj_n==dtraj))

class TestSaveDiscreteTrajectory(unittest.TestCase):

    def setUp(self):
        self.filename=testpath +'out_dtraj.npy'
        self.dtraj=np.arange(10000)

    def tearDown(self):
        os.remove(self.filename)

    def test_save_discrete_trajectory(self):
        dt.save_discrete_trajectory(self.filename, self.dtraj)
        dtraj_n=np.load(self.filename)
        self.assertTrue(np.all(dtraj_n==self.dtraj))

class TestDiscreteTrajectoryStatistics(unittest.TestCase):

    def test_count_1(self):
        S = np.array([0, 0, 0, 0, 0, 0])
        H = np.array([6])
        assert(dt.number_of_states(S) == 1)
        assert(dt.number_of_states(S, only_used=True) == 1)
        assert(np.allclose(dt.count_states(S),H))

    def test_count_2(self):
        S = np.array([1, 1, 1, 1, 1, 1])
        H = np.array([0,6])
        assert(dt.number_of_states(S) == 2)
        assert(dt.number_of_states(S, only_used=True) == 1)
        assert(np.allclose(dt.count_states(S),H))

    def test_count_3(self):
        S1 = np.array([0, 1, 2, 3, 4])
        S2 = np.array([2, 2, 2, 2, 6])
        H = np.array([1, 1, 5, 1, 1, 0, 1])
        assert(dt.number_of_states([S1,S2]) == 7)
        assert(dt.number_of_states([S1,S2], only_used=True) == 6)
        assert(np.allclose(dt.count_states([S1,S2]),H))

    def test_count_big(self):
        import pyemma.datasets
        dtraj = pyemma.datasets.load_2well_discrete().dtraj_T100K_dt10
        dt.number_of_states(dtraj)
        dt.count_states(dtraj)


class TestIndexStates(unittest.TestCase):

    def test_subset_error(self):
        dtraj =[0,1,2,3,2,1,0]
        # should be a ValueError because this is not a subset
        with self.assertRaises(ValueError):
            dt.index_states(dtraj, subset=[3,4,5])

    def test_onetraj(self):
        dtraj =[0,1,2,3,2,1,0]
        # should be a ValueError because this is not a subset
        res = dt.index_states(dtraj)
        expected = [np.array([[0,0],[0,6]]),np.array([[0,1],[0,5]]),np.array([[0,2],[0,4]]),np.array([[0,3]])]
        assert(len(res) == len(expected))
        for i in range(len(res)):
            assert(res[i].shape == expected[i].shape)
            assert(np.alltrue(res[i] == expected[i]))

    def test_onetraj_sub(self):
        dtraj =[0,1,2,3,2,1,0]
        # should be a ValueError because this is not a subset
        res = dt.index_states(dtraj, subset=[2,3])
        expected = [np.array([[0,2],[0,4]]),np.array([[0,3]])]
        assert(len(res) == len(expected))
        for i in range(len(res)):
            assert(res[i].shape == expected[i].shape)
            assert(np.alltrue(res[i] == expected[i]))

    def test_twotraj(self):
        dtrajs = [[0,1,2,3,2,1,0], [3,4,5]]
        # should be a ValueError because this is not a subset
        res = dt.index_states(dtrajs)
        expected = [np.array([[0,0],[0,6]]),np.array([[0,1],[0,5]]),np.array([[0,2],[0,4]]),np.array([[0,3],[1,0]]),np.array([[1,1]]),np.array([[1,2]])]
        assert(len(res) == len(expected))
        for i in range(len(res)):
            assert(res[i].shape == expected[i].shape)
            assert(np.alltrue(res[i] == expected[i]))

    def test_big(self):
        import pyemma.datasets
        dtraj = pyemma.datasets.load_2well_discrete().dtraj_T100K_dt10
        # just run these to see if there's any exception
        dt.index_states(dtraj)


class TestSampleIndexes(unittest.TestCase):

    def test_sample_by_sequence(self):
        dtraj =[0,1,2,3,2,1,0]
        idx = dt.index_states(dtraj)
        seq = [0,1,1,1,0,0,0,0,1,1]
        sidx = dt.sample_indexes_by_sequence(idx, seq)
        assert(np.alltrue(sidx.shape == (len(seq),2)))
        for t in range(sidx.shape[0]):
            assert(sidx[t,0] == 0) # did we pick the right traj?
            assert(dtraj[sidx[t,1]] == seq[t]) # did we pick the right states?

    def test_sample_by_state_replace(self):
        dtraj =[0,1,2,3,2,1,0]
        idx = dt.index_states(dtraj)
        sidx = dt.sample_indexes_by_state(idx, 5)
        for i in range(4):
            assert(sidx[i].shape[0] == 5)
            for t in range(sidx[i].shape[0]):
                assert(dtraj[sidx[i][t,1]] == i)

    def test_sample_by_state_replace_subset(self):
        dtraj =[0,1,2,3,2,1,0]
        idx = dt.index_states(dtraj)
        subset = [1,2]
        sidx = dt.sample_indexes_by_state(idx, 5, subset=subset)
        for i in range(len(subset)):
            assert(sidx[i].shape[0] == 5)
            for t in range(sidx[i].shape[0]):
                assert(dtraj[sidx[i][t,1]] == subset[i])


class TestMilestoneCounting(unittest.TestCase):
    def test_core_sets(self):
        dtrajs = [np.array([0, 0, 2, 0, 0, 3, 0, 5, 5, 5, 0, 0, 6, 8, 4, 1, 2, 0, 3])]
        expected = [np.array([2, 2, 2, 3, 3, 5, 5, 5, 5, 5, 6, 6, 4, 4, 2, 2, 3])]
        core_set = np.arange(2, 7)
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set)
        self.assertEqual(n_cores, 5)
        np.testing.assert_equal(dtrajs_core, expected)

    def test_core_sets_2(self):
        dtrajs = [np.array([0, 0, 2, 1, 2])]
        expected = [np.array([2, 1, 2])]
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set=np.arange(1, 3))
        self.assertEqual(n_cores, 2)
        np.testing.assert_equal(dtrajs_core, expected)

    def test_core_sets_3(self):
        dtrajs = [np.array([2, 0, 1, 1, 2])]
        expected = [np.array([2, 2, 1, 1, 2])]
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set=np.arange(1, 3))
        self.assertEqual(n_cores, 2)
        np.testing.assert_equal(dtrajs_core, expected)

    def test_core_sets_4(self):
        dtrajs = [np.array([2, 0, 0, 2, 0, 2, 0, 2])]
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set=[1, 2])
        self.assertEqual(n_cores, 2)
        np.testing.assert_equal(dtrajs_core, [np.ones_like(dtrajs[0]) * 2])

    def test_core_sets_5(self):
        dtrajs = [np.array([2, 2, 2, 2, 2, 2, 2, 0])]
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set=[2])
        self.assertEqual(n_cores, 1)
        np.testing.assert_equal(dtrajs_core, [np.ones_like(dtrajs[0]) * 2])

    def test_core_set_all_non_negative(self):
        dtrajs = [np.array([-1, 2, -1, 0, 0, 1, -1, 0, 1, 0, 2, -1])]
        expected = [np.array([2,  2, 0, 0, 1,  1, 0, 1, 0, 2, 2])]
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set=None)
        np.testing.assert_equal(offsets, [1])
        np.testing.assert_equal(n_cores, 3)
        np.testing.assert_equal(dtrajs_core, expected)

    def test_core_sets_6(self):
        dtrajs = [np.array([0, 1, 1, 2]), np.array([0, 0, 0])]
        import warnings

        if sys.version_info[0] == 2: # yeah python 2 bugs ftw...
            if hasattr(dt.milestone_counting, '__globals__'):
                if dt.milestone_counting.__globals__.has_key('__warningregistry__'):
                    dt.milestone_counting.__globals__['__warningregistry__'].clear()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", category=UserWarning, append=False)
            dtraj_core, offsets, _ = dt.milestone_counting(dtrajs, core_set=[1, 2])
            assert len(w) == 2
            assert all(issubclass(x.category, UserWarning) for x in w)
            assert "had to be truncated" in str(w[0].message)
            assert "never visited a core set" in str(w[1].message)

    def test_realistic_random(self):
        n_states = 50
        n_traj = 10
        n_cores = 30
        dtrajs = [np.random.randint(0, n_states, size=1000) for _ in range(n_traj)]
        core_set = np.random.choice(np.arange(0, n_states), size=n_cores, replace=False)
        assert np.unique(core_set).size == n_cores
        dtrajs_core, offsets, n_cores = dt.milestone_counting(dtrajs, core_set)

        def naive(dtrajs, core_set):
            import copy
            dtrajs = copy.deepcopy(dtrajs)
            newdiscretetraj = []
            for t, st in enumerate(dtrajs):
                oldmicro = None
                newtraj = []
                for f, micro in enumerate(st):
                    newmicro = None
                    for co in core_set:
                        if micro == co:
                            newmicro = micro
                            oldmicro = micro
                            break
                    if newmicro is None and oldmicro is not None:
                        newtraj.append(oldmicro)
                    elif newmicro is not None:
                        newtraj.append(newmicro)
                    else:
                        pass
                newdiscretetraj.append(np.array(newtraj, dtype=int))

            return newdiscretetraj

        expected = naive(dtrajs, core_set)
        np.testing.assert_equal(dtrajs_core, expected)

    def test_reshift_indices_by_offset_1(self):
        samples = np.array([(0, 1), (0, 3), (1, 42)])
        # we have omitted itraj 1 and shift traj 0 by 2 and 2 by 1.
        # so itraj 1 becomes 2
        offsets = [2, None, 1]
        dt._apply_offsets_to_samples(samples, offsets)
        expected = np.array([(0, 3), (0, 5), (2, 43)])
        np.testing.assert_equal(samples, expected)

    def test_reshift_indices_by_offset_2(self):
        samples = np.array([(0, 1), (0, 3), (1, 42), (2, 3)])
        offsets = [2, None, 1, None, 7, None]
        dt._apply_offsets_to_samples(samples, offsets)
        expected = np.array([(0, 3), (0, 5), (2, 43), (4, 10)])
        np.testing.assert_equal(samples, expected)

if __name__ == "__main__":
    unittest.main()
