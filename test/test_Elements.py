# -*- coding: utf-8 -*-
"""

Created on Fri May 31 17:07:40 2013

@author: Paolo Cozzi <paolo.cozzi@tecnoparco.it>

"""

import sys
import unittest

from numpy.numarray import mlab

sys.path.append("..")

import GClib
import GClib.Elements

class test_CalcClass(unittest.TestCase):
    def setUp(self):
        """A test case to verify class assignment"""
        
        self.GClevels = ((31, "L1"),
                         (37, "L1"),
                         (37.1, "L2"),
                         (40, "L2"),
                         (41, "L2"),
                         (41.1, "H1"),
                         (46, "H1"),
                         (46.1, "H2"),
                         (53, "H2"),
                         (53.1, "H3"),
                         (70, "H3")
                        )

    def test_CalcClass(self):
        """Testing class assignment"""
        
        for GClevel, Class in self.GClevels:
            result = GClib.Elements.CalcClass(GClevel)
            self.assertEqual(result, Class)

class test_Element(unittest.TestCase):
    def setUp(self):
        """Testing Element instantiation"""
        
        self._test_Element = GClib.Elements.Element()
        
    def test_SetSize(self):
        """Testing Element SetSize"""
        
        #testing setting start and no end and viceversa
        self.assertRaises(GClib.Elements.ElementError, self._test_Element.SetSize, None, 100000)
        self.assertRaises(GClib.Elements.ElementError, self._test_Element.SetSize, 100000, None)
        
        #cal SetSize and verify dimensions and start, end coordinates
        start = 100000
        end = 500000
        size = end-start
        
        #Normal SetSize call
        self._test_Element.SetSize(start,end)
        self.assertEqual(self._test_Element.start, start)
        self.assertEqual(self._test_Element.end, end)
        self.assertEqual(self._test_Element.size, size)
        
        #Verify coordinate inversion
        self._test_Element.SetSize(end, start)
        self.assertEqual(self._test_Element.start, start)
        self.assertEqual(self._test_Element.end, end)
        self.assertEqual(self._test_Element.size, size)

class test_Gap(unittest.TestCase):
    def setUp(self):
        """Testing Gap instantiation"""
        
        self._test_Gap = GClib.Elements.Gap()
        
    def test_SetSize(self):
        """Testing Gap SetSize"""
        
        #testing setting start and no end and viceversa
        self.assertRaises(GClib.Elements.ElementError, self._test_Gap.SetSize, None, 100000)
        self.assertRaises(GClib.Elements.ElementError, self._test_Gap.SetSize, 100000, None)
        
        #cal SetSize and verify dimensions and start, end coordinates
        start = 100000
        end = 500000
        size = end-start
        
        #Normal SetSize call
        self._test_Gap.SetSize(start,end)
        self.assertEqual(self._test_Gap.start, start)
        self.assertEqual(self._test_Gap.end, end)
        self.assertEqual(self._test_Gap.size, size)
        
        #Verify coordinate inversion
        self._test_Gap.SetSize(end, start)
        self.assertEqual(self._test_Gap.start, start)
        self.assertEqual(self._test_Gap.end, end)
        self.assertEqual(self._test_Gap.size, size)

class test_Window(unittest.TestCase):
    def setUp(self):
        """Testing Window instatiation"""
        
        self.GClevels = ((31, "L1"),
                         (37, "L1"),
                         (37.1, "L2"),
                         (40, "L2"),
                         (41, "L2"),
                         (41.1, "H1"),
                         (46, "H1"),
                         (46.1, "H2"),
                         (53, "H2"),
                         (53.1, "H3"),
                         (70, "H3")
                        )
        
        self._test_Window = GClib.Elements.Window()
        
    def test_SetSize(self):
        """Testing window SetSize"""
        
        #testing setting start and no end and viceversa
        self.assertRaises(GClib.Elements.ElementError, self._test_Window.SetSize, None, 100000)
        self.assertRaises(GClib.Elements.ElementError, self._test_Window.SetSize, 100000, None)
        
        #cal SetSize and verify dimensions and start, end coordinates
        start = 100000
        end = 500000
        size = end-start
        
        #Normal SetSize call
        self._test_Window.SetSize(start,end)
        self.assertEqual(self._test_Window.start, start)
        self.assertEqual(self._test_Window.end, end)
        self.assertEqual(self._test_Window.size, size)
        
        #Verify coordinate inversion
        self._test_Window.SetSize(end, start)
        self.assertEqual(self._test_Window.start, start)
        self.assertEqual(self._test_Window.end, end)
        self.assertEqual(self._test_Window.size, size)
        
    def test_SetGClevel(self):
        """Testing SetGClevel (assigning GC class)"""
        
        for GClevel, Class in self.GClevels:
            self._test_Window.SetGClevel(GClevel)
            self.assertEqual(self._test_Window.Class, Class)

class test_Isochore(unittest.TestCase):
    def setUp(self):
        """testing Isochore instantiation"""
        
        #Starting an Isochore element from a Window Element
        window = GClib.Elements.Window(start=200000, end=300000, GClevel=38)
        self._test_Isochore = GClib.Elements.Isochore(window=window)
        
    def test_AddWindow(self):
        """Testing adding window to an isochore"""
        
        #test Adding only a Window element
        element = GClib.Elements.Element(start=0,end=100000)
        gap = GClib.Elements.Gap(start=0,end=100000)
        isochore = GClib.Elements.Isochore(window=GClib.Elements.Window(start=200000, end=300000, GClevel=38))
        
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, element)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, gap)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, isochore)
        
        #Adding a simple window
        window = GClib.Elements.Window(start=300000, end=400000, GClevel=40)
        self._test_Isochore.AddWindow(window)
        self.assertEqual(self._test_Isochore.GClevels, [38,40])
        self.assertEqual(self._test_Isochore.start, 200000)
        self.assertEqual(self._test_Isochore.end, 400000)
        self.assertEqual(self._test_Isochore.avg_GClevel, mlab.mean([38,40]))
        self.assertEqual(self._test_Isochore.stddev_GClevel, mlab.std([38,40]))
        
        #Adding a window before this element (why one can do this?)
        window = GClib.Elements.Window(start=100000, end=200000, GClevel=39)
        self._test_Isochore.AddWindow(window)
        self.assertEqual(self._test_Isochore.GClevels, [38,40, 39])
        self.assertEqual(self._test_Isochore.start, 100000)
        self.assertEqual(self._test_Isochore.end, 400000)
        self.assertEqual(self._test_Isochore.avg_GClevel, mlab.mean([38,40,39]))
        self.assertEqual(self._test_Isochore.stddev_GClevel, mlab.std([38,40,39]))
        
        #Adding a non contiguous window
        window = GClib.Elements.Window(start=500000, end=600000, GClevel=39)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, window)
        
        #Adding a windows already in this isochore
        window = GClib.Elements.Window(start=100000, end=400000, GClevel=38)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, window)
        window = GClib.Elements.Window(start=250000, end=400000, GClevel=38)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, window)
        window = GClib.Elements.Window(start=0, end=150000, GClevel=38)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddWindow, window)
        
    def test_AddIsochore(self):
        """Testing adding isochore to current one"""
        
        #test Adding only a isochore element
        element = GClib.Elements.Element(start=0,end=100000)
        gap = GClib.Elements.Gap(start=0,end=100000)
        window = GClib.Elements.Window(start=200000, end=300000, GClevel=38)
        
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, element)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, gap)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, window)
        
        #defining an Isochore
        window = GClib.Elements.Window(start=300000, end=400000, GClevel=40)
        self._test_Isochore.AddWindow(window)
        
        window = GClib.Elements.Window(start=100000, end=200000, GClevel=39)
        self._test_Isochore.AddWindow(window)
        
        #Creating a new Isochore
        window = GClib.Elements.Window(start=400000, end=500000, GClevel=39)
        isochore = GClib.Elements.Isochore(window)
        window = GClib.Elements.Window(start=500000, end=600000, GClevel=38)
        isochore.AddWindow(window)
        window = GClib.Elements.Window(start=600000, end=700000, GClevel=40)
        isochore.AddWindow(window)
        
        #Add the new Isochore and verify values
        self._test_Isochore.AddIsochore(isochore)
        self.assertEqual(self._test_Isochore.GClevels, [38,40, 39, 39, 38, 40])
        self.assertEqual(self._test_Isochore.start, 100000)
        self.assertEqual(self._test_Isochore.end, 700000)
        self.assertEqual(self._test_Isochore.avg_GClevel, mlab.mean([38,40,39, 39, 38, 40]))
        self.assertEqual(self._test_Isochore.stddev_GClevel, mlab.std([38,40,39, 39, 38, 40]))
        
        #Adding a non contiguous isochore
        window = GClib.Elements.Window(start=1000000, end=1100000, GClevel=39)
        isochore = GClib.Elements.Isochore(window)
        window = GClib.Elements.Window(start=1100000, end=1200000, GClevel=39)
        isochore.AddWindow(window)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, isochore)

        #Adding and Isochore already in this Isochore
        window = GClib.Elements.Window(start=200000, end=300000, GClevel=38)
        isochore = GClib.Elements.Isochore(window)
        window = GClib.Elements.Window(start=300000, end=400000, GClevel=40)
        isochore.AddWindow(window)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, isochore)
        
        window = GClib.Elements.Window(start=0, end=100000, GClevel=38)
        isochore = GClib.Elements.Isochore(window)
        window = GClib.Elements.Window(start=100000, end=200000, GClevel=40)
        isochore.AddWindow(window)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, isochore)
        
        window = GClib.Elements.Window(start=600000, end=700000, GClevel=38)
        isochore = GClib.Elements.Isochore(window)
        window = GClib.Elements.Window(start=700000, end=800000, GClevel=40)
        isochore.AddWindow(window)
        self.assertRaises(GClib.Elements.IsochoreError, self._test_Isochore.AddIsochore, isochore)


if __name__ == "__main__":
    unittest.main()
