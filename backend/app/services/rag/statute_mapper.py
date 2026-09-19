"""
LegalEagle Statute Mapping Engine — Bharatiya Law Alias Subsystem.

Provides bidirectional statutory cross-referencing between historical Indian statutes
and the modern criminal & evidentiary codes (effective July 1, 2024):
  - Indian Penal Code, 1860 (IPC) <-> Bharatiya Nyaya Sanhita, 2023 (BNS)
  - Code of Criminal Procedure, 1973 (CrPC) <-> Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
  - Indian Evidence Act, 1872 (IEA) <-> Bharatiya Sakshya Adhiniyam, 2023 (BSA)
"""

from typing import Dict, List, Optional, Any


class StatuteMapper:
    """Bidirectional Indian Statutory Transition Engine."""

    # IPC <-> BNS Mappings
    IPC_TO_BNS: Dict[str, Dict[str, str]] = {
        "420": {"bns_section": "318", "title": "Cheating and dishonestly inducing delivery of property"},
        "415": {"bns_section": "318", "title": "Cheating"},
        "416": {"bns_section": "319", "title": "Cheating by personation"},
        "417": {"bns_section": "318", "title": "Punishment for cheating"},
        "302": {"bns_section": "103", "title": "Punishment for murder"},
        "300": {"bns_section": "101", "title": "Murder"},
        "299": {"bns_section": "100", "title": "Culpable homicide"},
        "304": {"bns_section": "105", "title": "Punishment for culpable homicide not amounting to murder"},
        "304A": {"bns_section": "106", "title": "Causing death by negligence"},
        "304B": {"bns_section": "80", "title": "Dowry death"},
        "307": {"bns_section": "109", "title": "Attempt to murder"},
        "378": {"bns_section": "303", "title": "Theft"},
        "379": {"bns_section": "303", "title": "Punishment for theft"},
        "383": {"bns_section": "308", "title": "Extortion"},
        "390": {"bns_section": "309", "title": "Robbery"},
        "391": {"bns_section": "310", "title": "Dacoity"},
        "403": {"bns_section": "314", "title": "Dishonest misappropriation of property"},
        "405": {"bns_section": "316", "title": "Criminal breach of trust"},
        "406": {"bns_section": "316", "title": "Punishment for criminal breach of trust"},
        "34": {"bns_section": "3", "title": "Acts done by several persons in furtherance of common intention"},
        "120A": {"bns_section": "61", "title": "Definition of criminal conspiracy"},
        "120B": {"bns_section": "61", "title": "Punishment of criminal conspiracy"},
        "141": {"bns_section": "189", "title": "Unlawful assembly"},
        "319": {"bns_section": "114", "title": "Hurt"},
        "320": {"bns_section": "115", "title": "Grievous hurt"},
        "339": {"bns_section": "126", "title": "Wrongful restraint"},
        "340": {"bns_section": "127", "title": "Wrongful confinement"},
        "351": {"bns_section": "130", "title": "Assault"},
        "354": {"bns_section": "74", "title": "Assault or criminal force to woman with intent to outrage modesty"},
        "375": {"bns_section": "63", "title": "Rape"},
        "376": {"bns_section": "64", "title": "Punishment for rape"},
        "498A": {"bns_section": "85", "title": "Husband or relative of husband subjecting woman to cruelty"},
        "499": {"bns_section": "356", "title": "Defamation"},
        "500": {"bns_section": "356", "title": "Punishment for defamation"},
        "503": {"bns_section": "351", "title": "Criminal intimidation"},
        "506": {"bns_section": "351", "title": "Punishment for criminal intimidation"},
        "511": {"bns_section": "62", "title": "Punishment for attempting to commit offences"},
    }

    # CrPC <-> BNSS Mappings
    CRPC_TO_BNSS: Dict[str, Dict[str, str]] = {
        "154": {"bnss_section": "173", "title": "Information in cognizable cases (First Information Report / FIR)"},
        "41": {"bnss_section": "35", "title": "When police may arrest without warrant"},
        "161": {"bnss_section": "180", "title": "Examination of witnesses by police"},
        "436A": {"bnss_section": "479", "title": "Maximum period for which an undertrial prisoner can be detained"},
        "437": {"bnss_section": "480", "title": "When bail may be taken in case of non-bailable offence (Regular Bail)"},
        "438": {"bnss_section": "482", "title": "Direction for grant of bail to person apprehending arrest (Anticipatory Bail)"},
        "439": {"bnss_section": "483", "title": "Special powers of High Court or Court of Session regarding bail"},
    }

    # IEA <-> BSA Mappings
    IEA_TO_BSA: Dict[str, Dict[str, str]] = {
        "3": {"bsa_section": "2", "title": "Interpretation clause / Definition of Evidence"},
        "25": {"bsa_section": "22", "title": "Confession to police officer not to be proved"},
        "26": {"bsa_section": "23", "title": "Confession by accused while in custody of police not to be proved"},
        "62": {"bsa_section": "57", "title": "Primary evidence"},
        "63": {"bsa_section": "58", "title": "Secondary evidence"},
        "65B": {"bsa_section": "61", "title": "Admissibility of electronic and digital records"},
        "101": {"bsa_section": "104", "title": "Burden of proof"},
    }

    def __init__(self):
        # Build inverse mappings
        self.BNS_TO_IPC: Dict[str, List[str]] = {}
        for ipc, data in self.IPC_TO_BNS.items():
            bns = data["bns_section"]
            self.BNS_TO_IPC.setdefault(bns, []).append(ipc)

        self.BNSS_TO_CRPC: Dict[str, List[str]] = {}
        for crpc, data in self.CRPC_TO_BNSS.items():
            bnss = data["bnss_section"]
            self.BNSS_TO_CRPC.setdefault(bnss, []).append(crpc)

        self.BSA_TO_IEA: Dict[str, List[str]] = {}
        for iea, data in self.IEA_TO_BSA.items():
            bsa = data["bsa_section"]
            self.BSA_TO_IEA.setdefault(bsa, []).append(iea)

    def get_bns_for_ipc(self, ipc_section: str) -> Optional[Dict[str, str]]:
        """Find modern BNS section corresponding to an IPC section."""
        clean_sec = ipc_section.strip().upper()
        if clean_sec in self.IPC_TO_BNS:
            info = self.IPC_TO_BNS[clean_sec]
            return {
                "act": "Bharatiya Nyaya Sanhita",
                "section": info["bns_section"],
                "title": info["title"],
                "mapped_from": f"IPC Section {clean_sec}",
            }
        return None

    def get_ipc_for_bns(self, bns_section: str) -> List[Dict[str, str]]:
        """Find historical IPC section(s) corresponding to a BNS section."""
        clean_sec = bns_section.strip().upper()
        results = []
        if clean_sec in self.BNS_TO_IPC:
            for ipc in self.BNS_TO_IPC[clean_sec]:
                results.append({
                    "act": "Indian Penal Code",
                    "section": ipc,
                    "title": self.IPC_TO_BNS[ipc]["title"],
                    "mapped_from": f"BNS Section {clean_sec}",
                })
        return results

    def get_bnss_for_crpc(self, crpc_section: str) -> Optional[Dict[str, str]]:
        """Find modern BNSS section corresponding to a CrPC section."""
        clean_sec = crpc_section.strip().upper()
        if clean_sec in self.CRPC_TO_BNSS:
            info = self.CRPC_TO_BNSS[clean_sec]
            return {
                "act": "Bharatiya Nagarik Suraksha Sanhita",
                "section": info["bnss_section"],
                "title": info["title"],
                "mapped_from": f"CrPC Section {clean_sec}",
            }
        return None

    def get_bsa_for_iea(self, iea_section: str) -> Optional[Dict[str, str]]:
        """Find modern BSA section corresponding to an Evidence Act section."""
        clean_sec = iea_section.strip().upper()
        if clean_sec in self.IEA_TO_BSA:
            info = self.IEA_TO_BSA[clean_sec]
            return {
                "act": "Bharatiya Sakshya Adhiniyam",
                "section": info["bsa_section"],
                "title": info["title"],
                "mapped_from": f"IEA Section {clean_sec}",
            }
        return None

    def get_equivalents(self, act: str, section: str) -> List[Dict[str, str]]:
        """Generic resolver for any act and section."""
        clean_act = act.strip().upper()
        clean_sec = section.strip().upper()

        if "BNSS" in clean_act or "SURAKSHA" in clean_act:
            results = []
            if clean_sec in self.BNSS_TO_CRPC:
                for crpc in self.BNSS_TO_CRPC[clean_sec]:
                    results.append({
                        "act": "Code of Criminal Procedure",
                        "section": crpc,
                        "title": self.CRPC_TO_BNSS[crpc]["title"],
                        "mapped_from": f"BNSS Section {clean_sec}",
                    })
            return results
        elif "CRPC" in clean_act or "PROCEDURE" in clean_act:
            bnss = self.get_bnss_for_crpc(clean_sec)
            return [bnss] if bnss else []
        elif "BNS" in clean_act or "NYAYA" in clean_act:
            return self.get_ipc_for_bns(clean_sec)
        elif "IPC" in clean_act or "PENAL" in clean_act:
            bns = self.get_bns_for_ipc(clean_sec)
            return [bns] if bns else []
        elif "IEA" in clean_act or "EVIDENCE" in clean_act:
            bsa = self.get_bsa_for_iea(clean_sec)
            return [bsa] if bsa else []
        elif "BSA" in clean_act or "SAKSHYA" in clean_act:
            results = []
            if clean_sec in self.BSA_TO_IEA:
                for iea in self.BSA_TO_IEA[clean_sec]:
                    results.append({
                        "act": "Indian Evidence Act",
                        "section": iea,
                        "title": self.IEA_TO_BSA[iea]["title"],
                        "mapped_from": f"BSA Section {clean_sec}",
                    })
            return results

        return []


# Global instance
statute_mapper = StatuteMapper()
