# -*- coding: utf-8 -*-
"""
IEC 62320-1 Sentence Module.

This module implements classes for representing, generating [and parsing]
IEC 62320-1:2015 compliant sentences.

@author: Jan Safar

Copyright 2024 GLA Research and Development Directorate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
# =============================================================================
# %% Import Statements
# =============================================================================
# Built-in Modules ------------------------------------------------------------

# Third-party Modules ---------------------------------------------------------

# Local Modules ---------------------------------------------------------------
from iec_61162.part_1.sentences import iec_checksum
from iec_61162.part_1.sentences import ais_msg_bs_to_vdm_sentences

# =============================================================================
# %% Helper Functions
# =============================================================================

# =============================================================================
# %% Sentence Definitions
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

class BCGSentence:
    """
    AIS BCG Sentence: Base Station configuration, general command.

    """
    formatter_code = "BCG"

    def __init__(
            self,
            unique_id,
            tx_power_a=None,
            tx_power_b=None,
            vdl_retries=None,
            vdl_repeat=None,
            ratdma_control=None,
            utc_source=None,
            ads_interval=None,
            talker_id="AB",
            rx_channel_a=2087,
            rx_channel_b=2088,
            tx_channel_a=2087,
            tx_channel_b=2088,
            sentence_status="C"):
        # TODO: Implement input parameter value checking
        self.unique_id = unique_id
        self.rx_channel_a = rx_channel_a
        self.rx_channel_b = rx_channel_b
        self.tx_channel_a = tx_channel_a
        self.tx_channel_b = tx_channel_b
        self.tx_power_a = tx_power_a
        self.tx_power_b = tx_power_b
        self.vdl_retries = vdl_retries
        self.vdl_repeat = vdl_repeat
        self.ratdma_control = ratdma_control
        self.utc_source = utc_source
        self.ads_interval = ads_interval
        self.talker_id = talker_id
        self.sentence_status = sentence_status

    @property
    def string(self):
        """
        Returns
        -------
        s : str
            Sentence string, formatted as per IEC 62320-1.

        """
        s = "${:s}{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}".format(
            self.talker_id,
            self.formatter_code,
            self.unique_id or "",
            "" if self.rx_channel_a is None else str(self.rx_channel_a),
            "" if self.rx_channel_b is None else str(self.rx_channel_b),
            "" if self.tx_channel_a is None else str(self.tx_channel_a),
            "" if self.tx_channel_b is None else str(self.tx_channel_b),
            "" if self.tx_power_a is None else str(self.tx_power_a),
            "" if self.tx_power_b is None else str(self.tx_power_b),
            "" if self.vdl_retries is None else str(self.vdl_retries),
            "" if self.vdl_repeat is None else str(self.vdl_repeat),
            "" if self.ratdma_control is None else str(self.ratdma_control),
            self.utc_source or "",
            "" if self.ads_interval is None else "{:.1f}".format(self.ads_interval),
            self.talker_id,
            self.sentence_status)

        checksum = iec_checksum(s)
        s += "*" + "{:>02X}".format(checksum) + "\r\n"

        return s

# =============================================================================
# %% Sentence Generation
# =============================================================================
class SentenceGenerator:
    """
    IEC 62320-1 Sentence Generator.

    For multi-sentence messages, the generator automatically assigns
    an appropriate Sequential ID.

    Parameters
    ----------
    talker_id : str, optional
        Talker ID. The default is "AI".

    """
    def __init__(self, talker_id="AI"):
        self.talker_id = talker_id

        self.vdm_sequential_id = 0

    def generate_tsa_vdm(
            self,
            msg_bs,
            channel,
            unique_id="",
            utc_hhmm="",
            start_slot="",
            priority=2):
        """
        Generate a TSA-VDM sentence sequence encapsulating an AIS message.

        Parameters
        ----------
        msg_bs : bitstring.BitStream
            AIS message bitstream, formatted as per Rec. ITU-R M.1371.
        channel : str
            Channel selection:

            - 'A': AIS 1
            - 'B': AIS 2.
        unique_id : str, optional
            Base station's unique ID. Maximum of 15 characters.
            The default is "".
        utc_hhmm : str, optional
            UTC frame hour and minute of the requested transmission.
            The default is "".
        start_slot : str, optional
            Start slot number of the requested transmission. The default is "".
        priority : int, optional
            Transmission priority (0-2). Lower number corresponds to higher
            priority. The default is 2.

        Returns
        -------
        list of lists of TSASentence and VDMSentence objects
            Contiguous sentences of the same type are grouped in separate lists.

            For example:

            [[TSA Sentence], [VDM Sentence 1 of 2, VDM Sentence 2 of 2]].

            Note: The nested list structure is used by the IEC 61162-450 layer
            to set the grouping control parameter code 'g' in IEC messages.

        """
        # Generate the TSA Sentence
        tsa_sentence = TSASentence(
            vdm_link=self.vdm_sequential_id,
            channel=channel,
            talker_id=self.talker_id)

        # Generate the VDM Sentence(s)
        vdm_sentences = ais_msg_bs_to_vdm_sentences(
            msg_bs=msg_bs,
            sequential_id=self.vdm_sequential_id,
            channel=channel,
            talker_id=self.talker_id)

        # Correction: It appears that the VDM sequential ID should be increased
        # even for single-sentence messages
        # If this is a multi-sentence message, increase the sequential ID
        # if len(vdm_sentences) > 1:
        self.vdm_sequential_id = (self.vdm_sequential_id + 1) % 10

        return [[tsa_sentence]] + [vdm_sentences]

    def generate_vdm(
            self,
            msg_bs,
            channel):
        """
        Generate a VDM sentence sequence encapsulating an AIS message.

        Parameters
        ----------
        msg_bs : bitstring.BitStream
            AIS message bitstream, formatted as per Rec. ITU-R M.1371.
        channel : str
            Channel selection:

            - 'A': AIS 1
            - 'B': AIS 2.

        Returns
        -------
        list of lists of VDMSentence objects

            For example:

            [[VDM Sentence 1 of 2, VDM Sentence 2 of 2]].

            Note: The nested list structure is used by the IEC 61162-450 layer
            to set the grouping control parameter code 'g' in IEC messages.

        """
        # Generate the VDM Sentence(s)
        vdm_sentences = ais_msg_bs_to_vdm_sentences(
            msg_bs=msg_bs,
            sequential_id=self.vdm_sequential_id,
            channel=channel,
            talker_id=self.talker_id)

        # If this is a multi-sentence message, increase the sequential ID
        if len(vdm_sentences) > 1:
            self.vdm_sequential_id = (self.vdm_sequential_id + 1) % 10

        return [vdm_sentences]


# =============================================================================
# %% Sentence Parsing
# =============================================================================


# =============================================================================
# %% Quick & Dirty Testing
# =============================================================================
if __name__=='__main__':
    from bitstring import BitStream

    # Sample BCG Sentence
    bcg_sentence = BCGSentence(
        unique_id="BASE1",
        tx_power_a=0,
        tx_power_b=1,
        vdl_retries=2,
        vdl_repeat=0,
        ratdma_control=1,
        utc_source="I",
        ads_interval=60)

    print(bcg_sentence.string)

    # Sample data
    ais_msg_bs = BitStream("0x123456789ABCDEF"*15)

    # Initialise a Sentence Generator
    sg = SentenceGenerator()

    # Generate some sentences
    sentence_groups = sg.generate_tsa_vdm(ais_msg_bs, channel="A")

    for group in sentence_groups:
        for sentence in group:
            print(sentence.string)

    # Generate some more
    sentence_groups = sg.generate_vdm(ais_msg_bs, channel="A")

    for group in sentence_groups:
        for sentence in group:
            print(sentence.string)
