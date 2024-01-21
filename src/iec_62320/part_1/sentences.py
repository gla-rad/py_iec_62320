# -*- coding: utf-8 -*-
"""
IEC 62320-1 Sentences Module.

This module implements classes for representing IEC 61162-1:2015 compliant
sentences.

Created on Thu Jan 11 16:17:08 2018

@author: Jan Safar
"""

# =============================================================================
# %% Import Statements
# =============================================================================
from iec_61162.part_1.sentences import iec_checksum

# =============================================================================
# %% Function Definitions
# =============================================================================

# =============================================================================
# %% Class Definitions
# =============================================================================
class TSASentence:
    """
    AIS TSA Sentence: Transmit slot assignment.

    TODO: Input parameter checking.

    Attributes
    ----------
    vdm_link : int
        VDM link.
    channel : str
        Channel selection ('A' or 'B').
    talker_id : str, optional
        Talker ID. The default is "AI".
    unique_id : str, optional
        Base station's unique ID. Maximum of 15 characters. The default is "".
    utc_hhmm : str, optional
        UTC frame hour and minute of the requested transmission. The default
        is "".
    start_slot : str, optional
        Start slot number of the requested transmission. The default is "".
    priority : int, optional
        Transmission priority (0-2). Lower number corresponds to higher
        priority. The default is 2.

    """
    formatter_code = "TSA"

    def __init__(
            self,
            vdm_link,
            channel,
            talker_id="AI",
            unique_id="",
            utc_hhmm="",
            start_slot="",
            priority=2):
        self.vdm_link = vdm_link
        self.channel = channel
        self.talker_id = talker_id
        self.unique_id = unique_id
        self.utc_hhmm = utc_hhmm
        self.start_slot = start_slot
        self.priority = priority

    @property
    def string(self):
        """
        Returns
        -------
        s : str
            Sentence string, formatted as per IEC 62320-1.

        """
        s = "${:s}{:s},{:s},{:d},{:s},{:s},{:s},{:d}".format(
            self.talker_id,
            self.formatter_code,
            self.unique_id,
            self.vdm_link,
            self.channel,
            self.utc_hhmm,
            self.start_slot,
            self.priority)

        checksum = iec_checksum(s)
        s += "*" + "{:>02X}".format(checksum) + "\r\n"

        return s

# =============================================================================
# %% Quick & Dirty Testing
# =============================================================================
if __name__=='__main__':

    tsa_sentence = TSASentence(vdm_link=0, channel="A")

    print(tsa_sentence.string)
