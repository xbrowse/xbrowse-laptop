storage_mode = 'mongo'
db_host = 'localhost'
db_port = 27017
db_name = 'xbrowse_popfreq'
reference_populations = [
    {
        'slug': 'esp_ea',
        'file_type': 'esp_vcf_dir',
        'dir_path': '/home/vagrant/ESP6500SI.snps_indels.vcf/',
        'counts_key': 'esp_ea',
    },
    {
        'slug': 'esp_aa',
        'file_type': 'esp_vcf_dir',
        'dir_path': '/home/vagrant/ESP6500SI.snps_indels.vcf/',
        'counts_key': 'esp_aa',
    },    
]
