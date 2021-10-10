"""Mixins for the CMS NanoAOD schema"""
import awkward
import numpy as np
from coffea.nanoevents.methods import base, vector, candidate
import warnings

behavior = {}
behavior.update(base.behavior)
# vector behavior is included in candidate behavior
behavior.update(candidate.behavior)


class _NanoAODEvents(behavior["NanoEvents"]):
    def __repr__(self):
        return f"<event {self.year}:{self.run}:{self.luminosityBlock}:{self.event}>"


behavior["NanoEvents"] = _NanoAODEvents


def _set_repr_name(classname):
    def namefcn(self):
        return classname

    behavior[("__typestr__", classname)] = classname[0].lower() + classname[1:]
    behavior[classname].__repr__ = namefcn


@awkward.mixin_class(behavior)
class UHH2YearStringCollection(base.NanoCollection):
    _years = [
        "2016v2", "2016v3", "2017v1", "2017v2", "2018",
        "UL16preVFP", "UL16postVFP", "UL17", "UL18"
    ]

    def _year_matches(self,pattern):
        def decode(a):
            print(a)
            # print(a == 'UL17')
            # barray  = bytearray(list(a))
            # return np.array([barray.decode('utf-8')])
            print(a)
            return pattern in a
        # return self.to_numpy() == pattern
        # np_decode = np.vectorize(decode,signature='(n)->(m)')
        np_decode = np.vectorize(decode)
        string_array = np_decode(self).flatten()
        print(string_array)
        return string_array
        # sarray = 
        # return awkward.any(awkward.all(string_array == _year) for _year in self._years if pattern in _year)

    @property
    def isUL(self):
        return self._year_matches("UL")

    @property
    def is16(self):
        return self._year_matches("16")

    @property
    def is17(self):
        return self._year_matches("17")

    @property
    def is18(self):
        return self._year_matches("18")
        
_set_repr_name("UHH2YearStringCollection")

@awkward.mixin_class(behavior)
class Jet(vector.PtEtaPhiELorentzVector, base.NanoCollection):
    """UHH2 AK4 jet object"""
    
    _keys = ['btag_DeepCSV_probb', 'btag_DeepCSV_probbb', 'btag_DeepFlavour_probb', 'btag_DeepFlavour_probbb', 'btag_DeepFlavour_probc', 'btag_DeepFlavour_probg', 'btag_DeepFlavour_problepb', 'btag_DeepFlavour_probuds', 'caches', 'charge', 'chargedEmEnergyFraction', 'chargedHadronEnergyFraction', 'chargedMultiplicity', 'electronMultiplicity', 'energy', 'eta', 'fields', 'genjet_index', 'hadronFlavour', 'jetArea', 'layout', 'lepton_keys', 'minDeltaRToL1Jet', 'muonEnergyFraction', 'muonMultiplicity', 'nbytes', 'neutralEmEnergyFraction', 'neutralHadronEnergyFraction', 'neutralHadronPuppiMultiplicity', 'neutralMultiplicity', 'neutralPuppiMultiplicity', 'numba_type', 'numberOfDaughters', 'partonFlavour', 'pdgId', 'pfcand_indexs', 'phi', 'photonEnergyFraction', 'photonMultiplicity', 'photonPuppiMultiplicity', 'pileupID', 'pt', 'puppiMultiplicity']
    
    
    def btag(self,algo='DeepJet',wp='supertight'):
        _btag_algorithms = {
            'DeepCSV':{
                'probs':['btag_DeepCSV_probb', 'btag_DeepCSV_probbb'],
                'wp':{
                    'supertight':0.0,
                }
            },
            'DeepJet':{
                'probs':['btag_DeepFlavour_probb', 'btag_DeepFlavour_probbb', 'btag_DeepFlavour_problepb'],
                'wp':{
                    'supertight':0.0,
                }
            }
        }
        btag_score = self[_btag_algorithms[algo]['probs'][0]]
        for prob in _btag_algorithms[algo]['probs'][1:]:
            btag_score += self[prob]
    
        return btag_score < _btag_algorithms[algo]['wp'][wp]
    
_set_repr_name("Jet")



@awkward.mixin_class(behavior)
class FatJet(vector.PtEtaPhiELorentzVector, base.NanoCollection):
    """UHH2 AK8 jet objet"""

    @property
    def subjets(self):
        warnings.warn("You tried to access the subjets of UHH2s TopJets. This is a bit problematic right now.")

    def _safe_nsub(self,numerator,denominator):
        return awkward.where(self[denominator]>0,self[numerator]/self[denominator],-1.)
        
    @property
    def tau21(self):
        return self._safe_nsub('tau2','tau1')
    
    @property
    def tau32(self):
        return self._safe_nsub('tau3','tau2')

    @property
    def tau21_groomed(self):
        return self._safe_nsub('tau2_groomed','tau1_groomed')

    @property
    def tau32_groomed(self):
        return self._safe_nsub('tau3_groomed','tau2_groomed')

    @property
    def particlenetmass(self):
        return self['ParticleNetMassRegressionJetTags_mass']

    @property
    def n2b1(self):
        return self['ecfN2_beta1']

    @property
    def n2b2(self):
        return self['ecfN2_beta2']

    @property
    def n3b1(self):
        return self['ecfN3_beta1']

    @property
    def n3b2(self):
        return self['ecfN3_beta2']

_set_repr_name("FatJet")


@awkward.mixin_class(behavior)
class Beamspot(vector.ThreeVector,base.NanoCollection):
    pass

_set_repr_name("Beamspot")

@awkward.mixin_class(behavior)
class PrimaryVertex(vector.ThreeVector,base.NanoCollection):
    pass

_set_repr_name("PrimaryVertex")

@awkward.mixin_class(behavior)
class Particle(vector.PtEtaPhiELorentzVector,base.NanoCollection):
    pass

_set_repr_name("Particle")



# @awkward.mixin_class(behavior)
# class TriggerBits(base.NanoCollection):
    
#     @property
#     def get(self, name):
#         return self._events()[name]

__all__ = [
    "Jet",
    "FatJet",
    "Particle",
    "Beamspot",
    "PrimaryVertex",
    "UHH2YearStringCollection",
    "TriggerBits",
]
