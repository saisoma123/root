import unittest

import ROOT

RNTupleModel = ROOT.Experimental.RNTupleModel
RNTupleReader = ROOT.Experimental.RNTupleReader
RNTupleWriter = ROOT.Experimental.RNTupleWriter

class RNTupleBasics(unittest.TestCase):
    """Basic tests of using RNTuple from Python"""

    def test_write_read(self):
        """Can write and read a basic RNTuple."""

        model = RNTupleModel.Create()
        model.MakeField["int"]("f")
        writer = RNTupleWriter.Recreate(model, "ntpl", "test_ntuple_py_write_read.root")
        entry = writer.CreateEntry()
        entry["f"] = 42
        writer.Fill(entry)
        del writer

        reader = RNTupleReader.Open("ntpl", "test_ntuple_py_write_read.root")
        self.assertEqual(reader.GetNEntries(), 1)
        entry = reader.GetModel().CreateEntry()
        reader.LoadEntry(0, entry)
        self.assertEqual(entry["f"], 42)
