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

"""Classes for natural deduction systems."""

from pylogics.syntax.base import Formula, FalseFormula, And, Or, Not, Implies
from pylogics.deduction.base import AbstractDeductionSystem
from pylogics.exceptions import PylogicsError

from enum import Enum

class NaturalDeductionRule(Enum):
    """Enumeration of natural deduction rules."""

    and_e1 = "and_e1"   
    and_e2 = "and_e2"   
    and_i = "and_i"     
    assumption = "assumption"
    bot_e = "bot_e"
    copy = "copy"       
    dneg_e = "dneg_e"   
    dneg_i = "dneg_i"   
    impl_e = "impl_e"   
    impl_i = "impl_i"   
    MT = "MT"
    neg_e = "neg_e"
    neg_i = "neg_i"
    or_e = "or_e"
    or_i1 = "or_i1"
    or_i2 = "or_i2"
    premise = "premise"

class NaturalDeductionProof(list):
    pass

class NaturalDeduction(AbstractDeductionSystem):
    """Natural Deduction System."""

    def proof(self, proof: list):
        proof_nf = NaturalDeductionProof()        
        while proof:
            row, content, *proof = proof
            if isinstance(content, Formula):
                justification, *proof = proof
                proof_nf.append((row, content, justification))
            elif isinstance(content, list):                
                proof_nf.append((row, self.proof([row] + content), NaturalDeductionRule.assumption))
        return proof_nf

    def check(self, proof: list, sound = {}) -> bool:
        """Check a given proof according to natural deduction rules."""
        # raise PylogicsError(
        #     f"proof '{proof}' cannot be processed by {self.check.__name__}"  # type: ignore
        # )

        check_justiﬁcation = {
            NaturalDeductionRule.and_e1:self._check_justiﬁcation_and_e1,
            NaturalDeductionRule.and_e2:self._check_justiﬁcation_and_e2,
            NaturalDeductionRule.and_i:self._check_justiﬁcation_and_i,
            NaturalDeductionRule.bot_e:self._check_justiﬁcation_bot_e,
            NaturalDeductionRule.copy:self._check_justiﬁcation_copy,
            NaturalDeductionRule.dneg_e:self._check_justiﬁcation_dneg_e,
            NaturalDeductionRule.dneg_i:self._check_justiﬁcation_dneg_i,
            NaturalDeductionRule.impl_e:self._check_justiﬁcation_impl_e,
            NaturalDeductionRule.impl_i:self._check_justiﬁcation_impl_i,
            NaturalDeductionRule.MT:self._check_justiﬁcation_MT,
            NaturalDeductionRule.neg_e:self._check_justiﬁcation_neg_e,
            NaturalDeductionRule.neg_i:self._check_justiﬁcation_neg_i,
            NaturalDeductionRule.or_e:self._check_justiﬁcation_or_e,
            NaturalDeductionRule.or_i1:self._check_justiﬁcation_or_i1,
            NaturalDeductionRule.or_i2:self._check_justiﬁcation_or_i2,
            NaturalDeductionRule.premise:self._check_justiﬁcation_premise, 
            NaturalDeductionRule.assumption:self._check_justiﬁcation_assumption, 
        }

        for row, content, justiﬁcation in proof:
            if isinstance(content, Formula):
                rule = justiﬁcation[0]
                args = [sound[i] for i in justiﬁcation[1:] if i in sound]
                if rule not in check_justiﬁcation:
                    return False
                if check_justiﬁcation[rule](content, *args) == False:
                    return False
            elif isinstance(content, list):
                if self.check(content, {i:sound[i] for i in sound}) == False:
                    return False
            else:
                return False            
            sound[row] = content            
        return True


    def _check_justiﬁcation_and_e1(self, formula, *args):
        """Check if the deduction is valid according to and-elimination (1) rule."""        
        return str(formula) == str(args[0].operands[0])

    def _check_justiﬁcation_and_e2(self, formula, *args):
        """Check if the deduction is valid according to and-elimination (2) rule."""        
        return str(formula) == str(args[0].operands[1])

    def _check_justiﬁcation_and_i(self, formula, *args):
        """Check if the deduction is valid according to and-introduction rule."""        
        return str(formula) == str(args[0] & args[1])

    def _check_justification_assumption(self, formula, *args):
        """Check if the deduction is valid according to assumption rule"""
        return True
    
    def _check_justification_bot_e(self, formula, *args):
        """Check if the deduction is valid according to absurd-elimination rule"""
        return args[0] == FalseFormula()

    def _check_justification_copy(self, formula, *args):
        """Check if the deduction is valid according to copy rule"""
        return str(formula) == str(args[0])

    def _check_justification_dneg_e(self, formula, *args):
        """Check if the deduction is valid according to double negation-elimination rule"""
        return str(~~formula) == str(args[0])

    def _check_justification_dneg_i(self, formula, *args):
        """Check if the deduction is valid according to double negation-introduction rule"""
        return str(formula) == str(~~args[0])

    def _check_justification_impl_e(self, formula, *args):
        """Check if the deduction is valid according to implies-elimination rule"""
        return str(args[0] >> formula) == str(args[1]) 

    def _check_justification_impl_i(self, formula, *args):
        """Check if the deduction is valid according to implies-introduction rule"""
        phi = args[0][ 0][1]
        psi = args[0][-1][1]
        return str(formula) == str(phi >> psi)

    def _check_justification_MT(self, formula, *args):
        """Check if the deduction is valid according to modus tollens rule"""
        return str(formula.argument >> args[1].argument) == str(args[0])

    def _check_justification_neg_e(self, formula, *args):
        """Check if the deduction is valid according to negation-elimination rule"""
        return str(~args[0]) == str(args[1]) and formula == FalseFormula()

    def _check_justification_neg_i(self, formula, *args):
        """Check if the deduction is valid according to negation-introduction rule"""        
        phi = args[0][ 0][1]
        psi = args[0][-1][1]
        return (psi == FalseFormula()) and (str(formula) == str(~phi))

    def _check_justification_or_e(self, formula, *args):
        """Check if the deduction is valid according to or-elimination rule"""
        phi_or_psi = args[0]
        phi, chi_1 = args[1][0][1], args[1][-1][1]        
        psi, chi_2 = args[2][0][1], args[2][-1][1]
        return (str(phi_or_psi) == str(phi | psi)) and (str(formula) == str(chi_1)) and (str(formula) == str(chi_2))

    def _check_justification_or_i1(self, formula, *args):
        """Check if the deduction is valid according to or-introduction 1 rule"""
        return str(formula.operands[0]) == str(args[0])

    def _check_justification_or_i2(self, formula, *args):
        """Check if the deduction is valid according to or-introduction 2 rule"""
        return str(formula.operands[1]) == str(args[0])

    def _check_justification_premise(self, formula, *args):
        """Check if the deduction is valid according to premise rule"""
        return True


    

        

