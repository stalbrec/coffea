from coffea.nanoevents.schemas.base import BaseSchema,zip_forms,nest_jagged_forms
    

class UHH2NtupleSchema(BaseSchema):
    """UHH2-Ntuple schema
    
    First test to get a basic schema to read UHH2 Ntuples
    """

    _special_singletons = {
        'genInfo':{
            'm_binningValues':'NanoCollection',
            'm_weights':'NanoCollection',
            'm_systweights':'NanoCollection',
        }
    }
    
    _custom_three_vector = {
        'beamspot':['beamspot_x0','beamspot_y0','beamspot_z0']
    }
    
    _mixins = {
        # 'year':'UHH2YearStringCollection',
        'beamspot':'Beamspot',

        #reco small-R jets
        'jetsAk4Puppi':'Jet',
        'jetsAk4CHS':'Jet',

        #reco large-R 
        'jetsAk8PuppiSubstructure_SoftDropPuppi':'FatJet',
        'jetsAk8CHSSubstructure_SoftDropCHS':'FatJet',
        'jetsAk8Puppi':'FatJet',
        'jetsAk8CHS':'FatJet',

        #reco variable-R jets
        'hotvrPuppi':'FatJet',
        'xconePuppi':'FatJet',
        'xconeCHS':'FatJet',

        #Gen(Top-)Jets
        'slimmedGenJets':'Jets',
        'genjetsAk8SubstructureSoftDrop':'FatJet',
        'genjetsAk8Substructure':'FatJet',
        'slimmedGenJetsAK8':'FatJet',
        'genXCone33TopJets':'FatJet',
        'hotvrGen':'FatJet',
        
        #slimmedMETS
        'slimmedMETs_GenMET':'MissingET',
        'slimmedMETsPuppi':'MissingET',        
        'slimmedMETs':'MissingET',
        
        
        'triggerResults':'TriggerBits',

        'offlineSlimmedPrimaryVertices':'PrimaryVertex',


        'GenParticles':'Particle',
        'PFParticles':'Particle',

        'slimmedMuonsUSER':'Particle',
        'slimmedElectronsUSER':'Particle',
        'slimmedPhotonsUSER':'Particle',
        
    }


    _rename  = {
        'jetsAk8PuppiSubstructure_SoftDropPuppi':'jetsAk8PuppiSubstructure',
        'jetsAk8CHSSubstructure_SoftDropCHS':'jetsAk8CHSSubstructure',
        'slimmedMuonsUSER':'Muons',
        'slimmedElectronsUSER':'Electrons',
        'slimmedPhotonsUSER':'Photons',

        'slimmedMETs_GenMET':'genMET',
        'slimmedMETsPuppi':'METPuppi',        
        'slimmedMETs':'MET',

    }
    
    def __init__(self,base_form):
        super().__init__(base_form)
        
        self._form['contents'] = self._build_collections(self._form['contents'])
        
    def _build_collections(self, branch_forms):

        collections = set(b.split('/')[0] for b in branch_forms)

        for c,sub_cs in self._custom_three_vector.items():
            collections.add(c)
            for sub_c in sub_cs:
                collections.remove(sub_c)

        output = {}
        def subbranch_name(b):
            name = ''
            if('.' in b):
                name = b.split('.')[-1]
            else:
                name = b.split('/')[-1]
            if(name.startswith('m_')):
                name = name[2:]
            return name


        for name in collections:
            oname = self._rename.get(name,name)

            mixin = self._mixins.get(name,'NanoCollection')

            if(name in self._custom_three_vector.keys()):
                xi = ['x','y','z']
                output[oname] = zip_forms(
                    {xi[i]: branch_forms[bname] for i,bname in enumerate(self._custom_three_vector[name])},
                    name,record_name=mixin
                )
            elif(any(name+'/' in b for b in  branch_forms)):
                    
                output[oname] = zip_forms(
                    {
                        subbranch_name(k): branch_forms[k]
                        for k in branch_forms
                        if (k.startswith(f"{name}/")
                            and k.replace(f'{name}/','') not in self._special_singletons.get(name,{})) # we need to split some collections, since they are a mix of NumpyArrays and ListOffsetArrays
                    },name,record_name = mixin)
                
            else:
                output[oname] = branch_forms[name]
                #How can one get simple singletons to have custom mixin, without breaking everything? Attempt #1 below..is not the way
                # if(name in self.mixins):
                #     # output[name].setdefault('parameters',{})
                #     # output[name]["parameters"].update({'__record__':mixin,'__array__':mixin,"collection_name":name}
                #     output[name]["parameters"].update({'__record__':mixin,"collection_name":name})

        for name in self._special_singletons.keys():
            for branch,mixin in self._special_singletons[name].items():
                branch_name = f"{name}/{branch}"
                oname = subbranch_name(branch_name)
                output[oname] = branch_forms[branch_name]
        return output

    @property
    def behavior(self):
        """Behaviors necessary to implement this schema"""
        from coffea.nanoevents.methods import uhh2,nanoaod
        # first load mixins from nanoaod and THEN overwrite with custom UHH2 ones since I used same names !!!
        merged_behaviors = nanoaod.behavior
        merged_behaviors.update(uhh2.behavior)
        return merged_behaviors
            
