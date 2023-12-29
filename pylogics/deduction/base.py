# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Base classes for pylogics deduction systems."""
from abc import ABC, abstractmethod

class AbstractDeductionSystem(ABC):
    """Base class for all the deduction systems."""

    @abstractmethod
    def Proof(proof) -> bool:
        """Build a proof according to the deduction system."""

    @abstractmethod
    def check(proof) -> bool:
        """Check a given proof according to the deduction system rules."""
