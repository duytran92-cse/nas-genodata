import json, operator
from collections import Counter
from application.models import Variation, Gene
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from application.modules.variation import components as variation_components
from application.modules.gene import components as gene_components

class Command(BaseCommand):
    def process(self, params = {}):
        keys = ['synonyms', 'name', 'is_somatic', 'minor_allele_frequency', 'evidence_attributes', 'ancestral_allele', 'minor_allele_count', 'clinic_significance', 'minor_allele', 'effects', 'chromosome', 'publications', 'genotype_frequency', 'hgvs', 'allele', 'allele_frequency', 'associated_disease', 'attribute', 'var_type', 'var_property', 'var_disease', 'reversed', 'gwas-effects', '1000-genomes', 'disgenet-diseases', 'genename', 'allele_string', 'consequence_types', 'ensembl-id', 'name', 'vcf_U5', 'vcf_ASS', 'vcf_DSS', 'vcf_INT', 'vcf_R3', 'vcf_R5', 'vcf_OTH', 'vcf_CFL', 'vcf_ASP', 'vcf_MUT', 'vcf_VLD', 'vcf_G5A', 'vcf_G5', 'vcf_HD', 'vcf_GNO', 'vcf_KGPhase1', 'vcf_KGPhase3', 'vcf_CDA', 'vcf_LSD', 'vcf_MTP', 'vcf_OM', 'vcf_NOC', 'vcf_WTD', 'vcf_NOV', 'vcf_CAF', 'vcf_COMMON', 'vcf_CLNHGVS', 'vcf_CLNALLE', 'vcf_CLNSRC', 'vcf_CLNORIGIN', 'vcf_CLNSRCID', 'vcf_CLNSIG', 'vcf_CLNDSDB', 'vcf_CLNDSDBID', 'vcf_CLNDBN', 'vcf_CLNREVSTAT', 'vcf_CLNACC', 'vcf_REF', 'vcf_ALT', 'vcf_RS', 'vcf_RSPOS', 'vcf_RV', 'vcf_VP', 'vcf_GENEINFO', 'vcf_dbSNPBuildID', 'vcf_SAO', 'vcf_SSR', 'vcf_WGT', 'vcf_VC', 'vcf_PM', 'vcf_TPA', 'vcf_PMC', 'vcf_S3D', 'vcf_SLO', 'vcf_NSF', 'vcf_NSM', 'vcf_NSN', 'vcf_REF', 'vcf_SYN', 'vcf_U3']
        rsnumbers = []
        manager = variation_components.DataManager()
        for r in Variation.objects.all():
            try:
                vol = manager.get(r.code)
                if vol is None:
                    continue
                for k in vol.keys():
                    if k in keys and vol[k].get('value', '') not in ['', None]:
                        print "[Value]", vol[k].get('value', '')
                        rsnumbers.append(r.code)
            except Exception as e:
                pass
        print "[RSNUMBER] Top 10"
        x = Counter(rsnumbers)
        print sorted(x.items(), key=operator.itemgetter(0))[:10]


        keys = ['geneid','chromosome','start','end','num_exon','protein_product','description','associated_disease','synonyms','publications','havana_gene','biotype','is_reversed','ctdbase-diseases','disgenet-diseases','id','name']
        genes = []
        manager = gene_components.DataManager()
        for r in Gene.objects.all():
            try:
                vol = manager.get(r.code)
                if vol is None:
                    continue
                for k in vol.keys():
                    if k in keys and vol[k].get('value', '') not in ['', None]:
                        print "[Value]", vol[k].get('value', '')
                        genes.append(r.code)
            except Exception as e:
                pass
        print "[GENE] Top 10"
        x = Counter(genes)
        print sorted(x.items(), key=operator.itemgetter(0))[:10]